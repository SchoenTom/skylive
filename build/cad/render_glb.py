"""
render_glb.py — reusable Blender headless render rig for SkyLive GLBs.
Usage:
  Blender --background --factory-startup --python render_glb.py -- <glb> <out_dir> <prefix> [views]
Produces shaded PNGs (Cycles CPU) from several angles, auto-framed, studio-lit.
views: comma list of iso,front,side,back,top,bottom  (default: iso,front,side)
"""
import bpy, sys, math
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
glb, out_dir, prefix = argv[0], argv[1], argv[2]
views = (argv[3].split(",") if len(argv) > 3 else ["iso", "front", "side"])

# clean slate
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)


# ── PBR material realism: infer a real-material response from each part's base color ──
# The GLB carries per-part colors (from spec's C_* palette). We inspect each material's Base
# Color and set Metallic/Roughness so parts read as real materials instead of flat plastic.
def assign_pbr_materials():
    for mat in bpy.data.materials:
        if not mat.use_nodes or not mat.node_tree:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf is None:
            bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if bsdf is None:
            continue
        bc = bsdf.inputs.get("Base Color")
        if bc is None or bc.is_linked:
            continue
        r, g, b, a = bc.default_value
        mx, mn = max(r, g, b), min(r, g, b)
        sat, val = mx - mn, mx
        if r > 0.6 and g > 0.55 and b < 0.5 and r >= g:          # gold / brass (SMA, XT30, pins)
            metallic, rough = 1.0, 0.18
        elif r > 0.75 and 0.25 < g < 0.62 and b < 0.22:          # orange Wago levers (saturated dielectric)
            metallic, rough = 0.0, 0.5
        elif r > 0.4 and g < 0.28 and b < 0.28:                  # red anodized (VTX / red wire)
            metallic, rough = 0.8, 0.4
        elif b >= r and b > g and sat > 0.12 and val < 0.55:     # battery wrap (dark blue) -> matte, darker
            metallic, rough = 0.0, 0.7
            r, g, b = r * 0.85, g * 0.85, b * 0.85
        elif sat < 0.12:                                         # neutral greys
            if val > 0.78:                                       # PETG shell (light)
                metallic, rough = 0.0, 0.35
            elif val < 0.28:                                     # black plastic (puck, housings, coax)
                metallic, rough = 0.0, 0.45
            else:                                                # anodised alu / steel greys
                metallic, rough = 0.8, 0.4
        else:                                                    # default dielectric (green PCB, etc.)
            metallic, rough = 0.0, 0.5
        bc.default_value = (r, g, b, a)
        if bsdf.inputs.get("Metallic") is not None:
            bsdf.inputs["Metallic"].default_value = metallic
        if bsdf.inputs.get("Roughness") is not None:
            bsdf.inputs["Roughness"].default_value = rough


assign_pbr_materials()

meshes = [o for o in bpy.data.objects if o.type == "MESH"]
if not meshes:
    print(">>>ERR no meshes"); sys.exit(1)

# combined bounding box (world space)
mn = Vector((1e9,)*3); mx = Vector((-1e9,)*3)
for o in meshes:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
center = (mn + mx) / 2
size = (mx - mn)
radius = max(size)

# target empty at center
tgt = bpy.data.objects.new("tgt", None); bpy.context.collection.objects.link(tgt)
tgt.location = center

# camera
cam_data = bpy.data.cameras.new("cam"); cam_data.lens = 55
cam = bpy.data.objects.new("cam", cam_data); bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam
con = cam.constraints.new("TRACK_TO"); con.target = tgt
con.track_axis = "TRACK_NEGATIVE_Z"; con.up_axis = "UP_Y"

# world: soft mid-grey studio
world = bpy.data.worlds.new("w"); bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.02, 0.03, 0.05, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.35

# scale-INDEPENDENT lighting: suns (irradiance independent of scene scale → robust vs mm-as-meters)
def add_sun(rot_deg, energy):
    ld = bpy.data.lights.new("S", "SUN"); ld.energy = energy; ld.angle = math.radians(6)
    lo = bpy.data.objects.new("S", ld); bpy.context.collection.objects.link(lo)
    lo.rotation_euler = [math.radians(a) for a in rot_deg]
    return lo
add_sun((55, 18, 30),   4.0)    # key (warm-ish top-front)
add_sun((70, -28, 200), 1.6)    # fill (opposite, soft)
add_sun((120, 0, 180),  1.3)    # rim/back edge light

# subtle dark ground far below (grounding shadow, HUD-navy)
bpy.ops.mesh.primitive_plane_add(size=radius*40, location=(center.x, center.y, mn.z - radius*0.02))
plane = bpy.context.active_object
pm = bpy.data.materials.new("floor"); pm.use_nodes = True
pm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.015,0.02,0.03,1)
plane.data.materials.append(pm)

# render settings — Cycles CPU
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 128
sc.cycles.use_denoising = True
sc.render.resolution_x = 1600; sc.render.resolution_y = 1200
sc.render.film_transparent = False
try:
    sc.view_settings.view_transform = "AgX"     # better highlight rolloff than Filmic → no blowout
except Exception:
    sc.view_settings.view_transform = "Filmic"
sc.view_settings.exposure = -0.3

dist = radius * 3.2
angles = {
    "iso":    ( 1.0,  -1.0,  0.8),
    "front":  ( 0.0,  -1.4,  0.15),
    "side":   ( 1.4,   0.0,  0.15),
    "back":   ( 0.0,   1.4,  0.2),
    "top":    ( 0.01,  0.0,  1.6),
    "bottom": ( 0.01,  0.0, -1.6),
}
for v in views:
    a = angles.get(v)
    if not a: continue
    cam.location = center + Vector(a).normalized() * dist
    sc.render.filepath = f"{out_dir}/{prefix}_{v}.png"
    bpy.ops.render.render(write_still=True)
    print(f">>>RENDERED {v} -> {sc.render.filepath}")
print(">>>DONE")
