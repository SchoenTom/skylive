# SkyLive Anton 2.0 — Druckanleitung (Labor-fertig)

*Stand 2026-07-05 (Update: Zugentlastung → beidseitiges Schieber-System), alle STLs frisch aus
dem verifizierten CAD (alle Gates grün). 6 Dateien, Riegel 2× drucken → **7 Teile gesamt**.
Ehrlich: CAD-verifiziert, dies ist der ERSTE Fit-Druck — Passungen (Tür, Deckel, Inserts, GoPro,
ZE-Schieber) am Teil prüfen, Werte ggf. rückmelden.*

> **Was sich seit der ersten Freigabe geändert hat (Body + Klappe + Teil 05):**
> **(1) Antennen-ZE = dein T-Prinzip von den Fotos, auf BEIDEN KURZEN Seiten** (Front + Heck,
> oberst, mittig): 2,9er-Schlitz von der Oberkante (Ø3,1-Koax von oben einlegen → Presssitz
> „hebt gut", Rundsitz unten), flaches **T-Stück** deckt den Schlitz und wird am Kopf mit
> **2× M2×8 Zylinderkopf VERTIKAL (Köpfe oben)** verschraubt. Kabel steigt durch die
> T-Kerbe nach oben aus — Omni steht überm Gehäuse. **05a (Kerbe) = Antennenseite ·
> 05b (blind) = verschließt die andere Seite komplett.** Links/rechts frei tauschbar.
> **(2) Akku-Klappe SCHLICHT:** der alte Innen-Schraubboss hätte mit dem Akku kollidiert
> (60+1 Swell endet bei 28,5 — Boss begann bei 26,5; dein Einwand war richtig, jetzt per
> Gate bewiesen frei). Neu: bündige Platte + **Lasche oben mittig** (1× M2 in Wand+Shelf,
> null Innenraum-Anspruch) + 2 Fuß-Nasen. Griffmulde entfällt — die Lasche ist der Griff.

## Material

| Zweck | Material | Warum |
|---|---|---|
| **Morgen (Fit-Prototyp)** | **PETG** | zäh genug für Klick/Zähne, einfach, maßhaltig genug |
| Final (Außeneinsatz) | **ASA** | UV-fest + formstabil bis ~95 °C (VTX-Wärme + Sonne am Helm). **Nie PLA** (erweicht) |

## Slicer-Grundeinstellungen (PETG, 0,4er Düse)

- **Schichthöhe 0,20 mm** · **4 Perimeter** (Schraub-/Klemm-/Zahn-Zonen brauchen Fleisch!)
- **Infill 40 % Gyroid** · Deckschichten 5 oben / 4 unten
- Temperatur nach Filament (typ. PETG 235–245 °C / Bett 75–85 °C)
- **Bauteilkühlung MAX 40–50 %** — PETG-Layerhaftung ist die Festigkeit der GoPro-Zähne!
- Naht: „Hinten" (auf die +Y-Rückseite legen)
- Elefantenfuß-Kompensation 0,15 (bündige Falze!)
- **Keine automatischen Supports** — nur die unten je Teil markierten Zonen (paint-on)

## Ausrichtung je Teil (WICHTIG — Layer-Richtung = Festigkeit)

### 01_body.stl — **AUF DIE RÜCKSEITE (+Y) LEGEN** (die Wand mit den 3 langen Schlitzen nach unten)
**Warum:** So liegen die **GoPro-Zähne HORIZONTAL** → Layerlinien laufen LÄNGS der Zähne →
Biegekraft beim Einclipsen läuft **mit** den Layern statt quer = deutlich bruchfester (dein Punkt!).
Zusätzlich: Kamera-Front zeigt nach oben (sauberste Sichtfläche), der fest verbaute Shelf steht
vertikal (druckt supportfrei), Dach-Öffnung zeigt zur Seite.
- **Support (paint-on) NUR an:** GoPro-Gabel-Unterseite (kragt seitlich aus) · die 3 Eck-Bosse
  (kragen horizontal) · Tür-Falz-Oberkante innen · Kamera-Ösen-Querbohrung ist Ø2,4 → supportfrei ok
- Die 45°-Louver der liegenden Rückseite werden zu Bett-Kontakt-Schlitzen → 5 mm **Brim** um die
  Wand-Auflage, Schlitz-Ränder nach dem Druck kurz entgraten.
- Ehrlicher Trade-off: liegend braucht der Body etwas Support innen — dafür sind Zähne + Klick-
  Nasen der Tür in der starken Richtung. Aufrecht wäre supportärmer, aber Zähne = Layer-gestapelt
  = Sollbruchstelle. **Zähne gewinnen.**

### 02_deckel.stl — **flach, Außenseite nach UNTEN**
Perfekt planar, kein Support. Die 3 Schrauben-Senkungen + das Schalterloch zeigen nach oben
(saubere Bohrungsränder), die Lippe wächst nach oben. Glatte Bett-Oberfläche = Sichtseite.

### 03_akkuklappe.stl — **flach, Außenseite nach UNTEN**
Kein Support. Die Nasen liegen horizontal → Layer längs = stabil beim Einhängen/Kippen.

### 04_xt30_riegel_2x.stl — **2× drucken**, flach (größte Fläche nach unten)
Kein Support. Klein — beide nebeneinander aufs Bett.

### 05a_ze_t_stueck_KABEL.stl + 05b_ze_t_stueck_BLIND.stl — flach auf den Rücken (Steg oben)
Die zwei T-Stücke (Flansch ~13×3×2,5 + Steg, Mini-Teile — beide zusammen aufs Bett, je 1
Reserve empfohlen). Flach liegend = Kerbe + Schraubendurchgänge supportfrei.
Der 2,9er-Schlitz im BODY ist der Presssitz (Ø3,1-Koax) — NICHT aufbohren, das Kabel wird
von oben eingedrückt und „hebt". Falls das T-Stück nicht satt einfährt: Maß melden statt feilen.

## Nach dem Druck (Reihenfolge!)

1. **Messing-Inserts ZUERST einschmelzen**, solange das Gehäuse leer ist (Lötkolben 250–270 °C,
   senkrecht ansetzen, langsam sinken lassen, 0,3 mm unter bündig stoppen. Fehlerbild: schiefer
   Insert/Blob = zu heiß oder zu schnell):
   - **3× M3 (Ø5×6)** in die Dach-Bosse, von oben
   - **1× M2 (Ø3,2×3 — deine Messung)** in die Ø2,8-Bohrung ÜBER der Akku-Öffnung (Achse
     horizontal, von außen — die Lasche deckt den Insert-Mund später ab). Tür-Schraube = M2×6.
2. Fit-Checks: Tür einschieben (unten Nasen einhaken → ankippen → M2) · Deckel auflegen (Lippe
   taucht ein, 3× M3) · GoPro-Mate auf die Zähne (**3,0 — Toms Vorgabe 07-06**; falls stramm:
   NICHT feilen, Wert melden) · Kamera einsetzen (linke Schraube von außen durch die
   Wand-Einsenkung!) · XT30-Adern (Ø2,8) in die Sattel-Rinnen legen, Riegel schrauben ·
   **ZE (T-Prinzip, kurze Seiten):** Koax von oben in den 2,9er-Schlitz eindrücken bis es
   auf dem Rundsitz liegt → T-Stück in die Vertiefung einfahren (deckt den Schlitz, Kabel
   läuft durch die Kerbe nach oben) → 2× M2×8 vertikal am Kopf; andere Seite: 05b blind
   rein + 2× M2×8. Flansch muss oben bündig mit dem Dachrand abschließen.
3. Was klemmt/wackelt → kurz notieren (Teil + Stelle + gefühltes Maß) — fließt direkt ins CAD.

**Teile-Übersicht:** Body ~71×39,5×56 · Deckel (dunkel im Viewer) · Klappe (blau, mit Lasche)
· 2 Riegel (grün) · 2 ZE-T-Stücke (magenta: 05a Kerbe + 05b blind).
**Schrauben-Einkauf: 3× M3×8 (Deckel) · 4× M2×8 (ZE) · 1× M2×6 (Lasche→M2-Insert) · 4× M2×8 (Riegel) · 2× M2 (Kamera) · Inserts 3× M3 + 1× M2.**
Viel Erfolg im Labor! 🛠️
