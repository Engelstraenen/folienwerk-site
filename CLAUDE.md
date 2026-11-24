# PROJEKT-MASTERFILE – FOLIENWERK
Gilt zusätzlich zur globalen Masterfile (~/.claude/CLAUDE.md).

## 1. Ziel und Endprodukt
Interaktive Demo-Webseite für einen erfundenen Autofolierer (FOLIENWERK Fahrzeugfolierung, Annahme: Köln). Musterbeispiel für Akquise an Folierbetriebe (nach LICHTBOGEN Elektro, WARMHERZ, FARBKANTE Maler).
Probleme, die die Seite löst:
- „Was kostet das?“-Anfragenflut ohne Daten → Angebot per Foto (Modell, Fotos, Wunschfarbe), keine Euro auf der Seite
- Kunde kann sich die Farbe nicht vorstellen → Farb-Konfigurator am Auto
- Billig-Konkurrenz / Laien-Folierer → Qualität sichtbar: Demontage, eingeschlagene Kanten, Ablauf im Zeitraffer
- Auto mehrere Tage weg, Kunde ruft ständig an → Live-Status mit Werkstattfotos
- Firmenkunden/Flotten → Fuhrpark-Anfrage, Logo-Vorschau, Folieren nachts/Wochenende
- Weitere Umsätze: Lackschutzfolie (PPF), Leasing-Rückgabe, Scheibentönung
- Nachwuchs/Fachkräfte → eigenes Recruiting-Kapitel (Film + 60-s-Bewerbung)
- Vertrauen → Bewertungen bewegt (Demo: als Beispiel markiert)

## 2. Qualitätsanspruch & Referenzen
Aufbau wie FLUTLICHT27/FARBKANTE: Film-Kapitel (Scroll spult Vorher → Arbeit → Ergebnis) im Wechsel mit Motion-Design-Kapiteln. Leitmotiv eindeutig Folierer: Rakel mit Filzkante, Heißluftföhn, Folie über die Kante einschlagen, Farbwechsel im Zeitraffer.

## 3. Regeln für dieses Projekt
- HELDENAUTO = PORSCHE 911 TURBO S (992) (Eugen 23.11.2026, VERBINDLICH): In allen Bildern/Filmen dasselbe Auto, nie Markenwechsel (Fehler FOMIX-A: BMW vorher, Audi nachher). Jeder Prompt nennt „the same Porsche 911 Turbo S 992“ mit Merkmalen (breites Heck, Leuchtband, fester Heckflügel, runde Scheinwerfer) und „never a different car“. Original-Lack silber, Folie Satin-Waldgrün. Ausnahme nur Fuhrpark (weißer Transporter).
- KEIN PORSCHE-WAPPEN, KEINE MARKENZEICHEN (Eugen 24.11.2026, VERBINDLICH, Markenrecht): Auto komplett entmarkt: kein Wappen auf Haube, keine Wappen in den Radnabendeckeln (glatt, schwarz), kein Schriftzug am Heck, keine Lenkrad-/Felgen-Logos. Jeder Prompt: „fully debadged, no crest or emblem on the hood, plain black wheel center caps, no lettering or logos anywhere on the car“. Vor dem Zeigen jedes Bild/Video auf Wappen prüfen.
- Keine echten Firmen, sonst keine Automarken/Logos, keine lesbaren Kennzeichen, keine Folienmarken, keine Preise/Euro, kein Wort „KI“.
- Demo-Hinweis oben, Formulare senden nichts. Persönlicher Link per `?firma=Name`.
- Alle Seiten mobil-optimiert (4 Größen + Kopfzeile 1081–1600 px).
- Bilder für die Seite 4K, Endvideos MiniMax H3 2K nur nach Kosten-OK.

## 4. Skills, Plugins, Agenten, MCP
Keine zusätzlichen nötig.

## 5. Zugänge
gh (Engelstraenen), sjinn in Chrome eingeloggt (Unlimited).

## 6. Workflow & Freigabepunkte
Storyboard-Wahl (Eugen) → First Frames 2K (Dreamina GPT Image 2.5 Sunburst, Unlimited) → Video-Drafts Dreamina Seedance 2.5 720P Unlimited (nur First Frame, Wächter SW.go prüft Schalter + Preis 0) → Seite bauen → Screenshot-Vergleich → GitHub Pages.

## 7. Befehle
(folgt mit dem ersten Code)

## 8. Offene Fragen
- Video-Drafts F2–F9 (Plan konzepte/video-plan.md), danach Seite bauen.

## 9. Entschieden
- 23.11.2026: Name FOLIENWERK, Stadt Köln (Annahme). 3 Storyboards (Prompts konzepte/prompts.md).
- 23.11.2026 (Eugen): Look der Storyboards passt („so muss das bei Autofolierern aussehen, trendy, modern“). Keine Einzelwahl → Claudes Empfehlung: Basis 1 „Die Rakel“ (Graphit + Säuregrün) + Lackschutz, Leasing, Live-Status aus 3 + Fuhrpark aus 2. Gesamt-Storyboard FOMIX-A (4x3) erzeugt.
- 23.11.2026 (Eugen): FOMIX-A abgelehnt, Auto wechselte die Marke. Durchgehend Porsche 911 Turbo S 992 → FOMIX-B.

- 24.11.2026 (Eugen): Porsche-Wappen überall entfernen → Storyboard konzepte/6-gesamtseite-ohne-wappen.png. Freigabe „Freigegeben, los“. Startbilder FF1–FF9 in 2K auf Dreamina (frames/). Video F1 Hero abgenommen („Passt, weiter“).

## 10. Ablage
Code: Dropbox/CLAUDE/Projekte/FOLIENWERK · Storyboards: konzepte/
