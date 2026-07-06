# SkyLive Sender 850 — Druckanleitung (Labor-fertig)

Mini-Vents · GoPro-Zähne 3,0 · 1 langer Bay-Schlitz Kamera-Seite), alle STLs frisch aus dem
verifizierten CAD (alle Gates grün; Export 08:23, **02_deckel NEU 07-06 nachmittags** —
Kopf-Auflage-Fix nach Toms Fund, s. unten). 5 Dateien, Riegel + T-Stück 2× drucken → **7 Teile
gesamt**. Ehrlich: CAD-verifiziert, ERSTER Fit-Druck — Passungen (Tür, Deckel, Inserts, GoPro,
ZE-Presssitz) am Teil prüfen, Werte rückmelden.*

> **Was sich seit der ersten Freigabe geändert hat (Body + Klappe + Teil 05):**
> **(1) Antennen-ZE = DIE REFERENZ-MECHANIK (T-Prinzip 2.0, 07-06 abends — der Einwand
> „das Kabel soll GANZ RUNTER und VOLL eingeklemmt werden" + STEP-Vermessung seines T-Teils
> und Grundkörpers):** Der Sitz in der Wand hat **SPIEL** (Ø3,2 auf Ø3,1 — Referenz-Maß, mein
> früherer „2,9-Presssitz" war eine Fehldeutung!). **Die Klemmkraft kommt von den Schrauben:**
> das T-Stück hat einen Steg mit **konvexer Nase R1,55** (= Kabelradius), die 2× M2×8
> VERTIKAL ziehen die Nase **0,4 mm in Presslage** aufs Kabel. Von oben: Mund 18×2,5
> (Querhaupt bündig) → Führungsschlitz 3,3 → Rundsitz Ø3,2 durch die Wand. **KEINE Kerbe,
> KEIN Bohren mehr nötig** — der Steg sitzt ÜBER dem Kabel, der Kabelweg durch die Wand ist
> immer frei. 1 T-Typ, 2× gedruckt, beidseitig identisch — **Seitenwahl bleibt DEINE** am
> Realteil. (Unbenutzte Seite: Mund+Schlitz zu; unterm Nasen-Steg bleiben zwei kleine
> Ø3,2-Sichel-Öffnungen des Sitzes — ehrlich gesagt: Mini-Vents, kein Loch.)
> **(2) Akku-Klappe SCHLICHT:** der alte Innen-Schraubboss hätte mit dem Akku kollidiert
> (60+1 Swell endet bei 28,5 — Boss begann bei 26,5; der Einwand war richtig, jetzt per
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

### 02_deckel.stl — **flach, Außenseite nach UNTEN** ⚠ NEU 07-06 abends: DIE REFERENZ-SENKUNG
Kein Support nötig (die 3 Unterseiten-Pads Ø10×1,5 drucken als flache Zylinder oben auf).
**Die Ansage „übernimm das vom Referenz-Prototyp" umgesetzt — sein Deckel.STEP vermessen:** CB **Ø6,5 ×
3,4**, Durchgang Ø3,4, **Kopf versenkt 0,4 unter bündig**, tragender Boden 1,1 (exakt des Referenz-Prototyps
Werte). Sein Deckel ist 4,5 dick — unserer holt die Dicke über **lokale Pads an der
Unterseite** (Deckel misst an den Schrauben 4,5, sonst 3,0). Dafür: Bosse 1,5 gekürzt +
Schrauben 1 mm diagonal einwärts (±28/±12 — sonst ragt der versenkte Kopf in die Falz-Ecke;
per Gate bewiesen). **Der Fund #1 bleibt dokumentiert:** die Ur-Datei hätte den Kopf komplett
durchfallen lassen. Deckel aus einer älteren Datei = wegwerfen, nur diese gilt.

### 03_akkuklappe.stl — **flach, Außenseite nach UNTEN**
Kein Support. Die Nasen liegen horizontal → Layer längs = stabil beim Einhängen/Kippen.
Die 2 Mini-Louver drucken bei dieser Lage supportfrei (45°-Eigenüberhang).

### 04_xt30_riegel_2x.stl — **2× drucken**, flach (größte Fläche nach unten)
Kein Support. Klein — beide nebeneinander aufs Bett.

### 05_ze_t_stueck_2x.stl — **2× drucken** (+1 Reserve), flach auf den Rücken (Nase oben) ⚠ NEU 07-06 abends
**die Referenz-Mechanik 1:1** (sein T-Teil STEP-vermessen): Querhaupt 17,7 × Steg 3,1 mit
**Rundnase R1,55**. Einbau: Kabel von oben in den Schlitz ganz runter bis in den Ø3,2-Sitz
drücken (geht LEICHT — der Sitz hat Spiel, das ist richtig so!) → T einschieben, Nase aufs
Kabel → **2× M2×8 anziehen = DIE Klemmung** (die Schrauben ziehen die Nase 0,4 ins Kabel).
Nichts bohren, nichts kerben. Beide Seiten identisch; Seitenwahl deine. Falls das T nicht
leicht in Mund/Schlitz einfährt: Maß melden statt feilen.

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
   **ZE (T-Prinzip 2.0, kurze Seiten — DEINE Seitenwahl):** Koax von oben durch Mund +
   Schlitz GANZ RUNTER in den Ø3,2-Sitz legen (fällt leicht rein — Spiel ist korrekt; es
   läuft waagerecht durch die Wand, Glocke außen direkt an der Wand) → T-Stück einschieben,
   Nase liegt aufs Kabel → **2× M2×8 vertikal ANZIEHEN = Klemmung** (Nase presst 0,4 ein);
   andere Seite: zweites T identisch + 2× M2×8. Querhaupt oben bündig mit dem Dachrand.
3. Was klemmt/wackelt → kurz notieren (Teil + Stelle + gefühltes Maß) — fließt direkt ins CAD.

**Teile-Übersicht:** Body ~71×39,5×56 · Deckel (dunkel im Viewer) · Klappe (blau, mit Lasche)
· 2 Riegel (grün) · 2× dasselbe ZE-T-Stück (Nasen-Steg — Schrauben klemmen; Seitenwahl deine).
**Schrauben-Einkauf: 3× M3×8 (Deckel) · 4× M2×8 (ZE) · 1× M2×6 (Lasche→M2-Insert) · 4× M2×8 (Riegel) · 2× M2 (Kamera) · Inserts 3× M3 + 1× M2.**
Viel Erfolg im Labor! 🛠️
