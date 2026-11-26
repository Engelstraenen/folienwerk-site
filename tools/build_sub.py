#!/usr/bin/env python3
"""Baut die Unterseiten von SCHICHTWECHSEL aus einem Inhalts-Verzeichnis.
Start: python3 tools/build_sub.py   (schreibt site/*.html)
Jede Unterseite: Kopf, großes Bild, Lamellen-Leiste (Fächer als Unternavigation), Blöcke, FAQ, Rückweg an dieselbe Stelle."""
import html, os
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")

NAV = [("folien", "Folien", "chrom"), ("wissen", "Wissen", "satin"), ("handwerk", "Handwerk", "matt"),
       ("referenzen", "Referenzen", "strass"), ("alles-folierbar", "Alles folierbar", "holo"),
       ("karriere", "Karriere", "glitter"), ("angebot", "Angebot", "klar")]

def head(title, desc):
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} – SCHICHTWECHSEL Fahrzeugfolierung Köln</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#150c26">
<link rel="preload" href="assets/fonts/grotesk.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="sub">
<div class="demo" id="demo">Demo-Seite<span class="for"></span> · Formulare senden nichts</div>
<header class="nav solid" id="nav">
  <a class="logo" href="index.html" aria-label="SCHICHTWECHSEL Startseite"><b>SCHICHTWECHSEL</b><small>Fahrzeugfolierung, Köln</small></a>
  <nav class="links" id="links" aria-label="Unterseiten">
""" + "".join(f'    <a href="{s}.html">{n}</a>\n' for s, n, _ in NAV[:6]) + """  </nav>
  <a class="btn btn-s holo-b" href="angebot.html">Angebot per Foto</a>
  <button class="burger" id="burger" aria-label="Menü öffnen" aria-expanded="false"><span></span><span></span></button>
</header>
"""

def strip(cur):
    out = '<nav class="sub-fan" aria-label="Musterfächer">'
    for s, n, sw in NAV:
        c = ' class="on" aria-current="page"' if s == cur else ''
        out += f'<a href="{s}.html"{c}><i class="sw sw-{sw}"></i><span>{n}</span></a>'
    return out + '</nav>'

def page(slug, title, desc, kick, h1, lead, img, img_alt, back, blocks, faq=None, extra=""):
    o = head(title, desc)
    o += f"""<main class="sub-main">
<section class="sub-hero">
  <div class="sh-img">{f'<img src="assets/img/{img}" alt="{html.escape(img_alt)}">' if img else ''}</div>
  <div class="sh-copy">
    <a class="back" href="index.html#{back}">← Zurück zum Fächer</a>
    <small class="kick">{kick}</small>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
{strip(slug)}
"""
    for b in blocks:
        o += b + "\n"
    if faq:
        o += '<section class="sub-faq"><h2>Häufige Fragen</h2>'
        for q, a in faq:
            o += f'<details><summary>{q}</summary><p>{a}</p></details>'
        o += '</section>\n'
    o += extra
    o += f"""<section class="sub-cta">
  <h2>Welche Folie passt zu deinem Auto?</h2>
  <p>Drei Fotos genügen. Du bekommst ein festes Angebot.</p>
  <div class="row"><a class="btn holo-b" href="angebot.html">Angebot per Foto</a><a class="btn btn-o" href="index.html#{back}">Zurück zum Fächer</a></div>
</section>
</main>
<footer class="foot">
  <div><b>SCHICHTWECHSEL</b><br>Fahrzeugfolierung, Köln<br><small>Demo-Unternehmen, keine echte Firma</small></div>
  <div><a href="folien.html">Folien</a><a href="wissen.html">Wissen</a><a href="handwerk.html">Handwerk</a><a href="referenzen.html">Referenzen</a></div>
  <div><a href="alles-folierbar.html">Alles folierbar</a><a href="karriere.html">Karriere</a><a href="angebot.html">Angebot</a><a href="impressum.html">Impressum</a></div>
</footer>
<script src="assets/js/sub.js"></script>
</body>
</html>
"""
    open(os.path.join(ROOT, slug + ".html"), "w").write(o)

def split(img, alt, h2, text, rev=False, more=""):
    return f"""<section class="sub-split{' rev' if rev else ''}">
  <div class="ss-img"><img src="assets/img/{img}" alt="{html.escape(alt)}" loading="lazy"></div>
  <div class="ss-copy"><h2>{h2}</h2>{text}{more}</div>
</section>"""

def facts(items, h2=None):
    o = '<section class="sub-facts">' + (f'<h2>{h2}</h2>' if h2 else '') + '<div class="fx">'
    for big, small in items:
        o += f'<div class="f"><b>{big}</b><span>{small}</span></div>'
    return o + '</div></section>'

def table(h2, head_, rows, note=""):
    o = f'<section class="sub-table"><h2>{h2}</h2><div class="tw"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head_) + '</tr></thead><tbody>'
    for r in rows:
        o += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    return o + f'</tbody></table></div>{f"<p class=note>{note}</p>" if note else ""}</section>'

def steps(h2, items):
    o = f'<section class="sub-steps"><h2>{h2}</h2><ol>'
    for i, (t, d) in enumerate(items, 1):
        o += f'<li><b>{i:02d}</b><div><h3>{t}</h3><p>{d}</p></div></li>'
    return o + '</ol></section>'

def swatches(h2, items):
    o = f'<section class="sub-sw"><h2>{h2}</h2><div class="swg">'
    for sw, name, text, ids in items:
        o += f'<article id="{ids}"><i class="sw sw-{sw}"></i><h3>{name}</h3><p>{text}</p></article>'
    return o + '</div></section>'

SRC = "Herstellerangaben aus technischen Datenblättern (u. a. ORAFOL, 3M, Avery Dennison) für Außenflächen, vertikal, mitteleuropäisches Klima. Maximalwerte, keine Garantie."

# ---------- Folien ----------
page("folien", "Folienarten", "Chrom, Color-Shift, Satin, Matt, Glitzer, Carbon und Lackschutz erklärt.",
     "02 · Folien", "Über 200 Folien. Sieben Familien.",
     "Jede Folie im Fächer gehört zu einer Familie. Die Familie entscheidet, wie das Auto im Licht aussieht, wie viel Pflege es braucht und wie lange die Folie hält.",
     "k1.webp", "Sportwagen in Spiegelchrom Silber", "folie",
     [swatches("Die Familien im Fächer", [
        ("shift", "Color-Shift", "Wechselt je nach Blickwinkel die Farbe, zum Beispiel von Türkis über Violett zu Gold. Gegossene Spezialfolie, braucht saubere Verarbeitung an Rundungen.", "shift"),
        ("chrom", "Chrom", "Spiegelnde Oberfläche wie poliertes Metall. Die anspruchsvollste Folie: dehnt sich weniger und zeigt jede Unebenheit. Hält kürzer als Farbfolie.", "chrom"),
        ("satin", "Satin", "Seidenglanz zwischen Matt und Hochglanz. Wirkt wie ein teurer Speziallack und verzeiht kleine Kratzer besser als Hochglanz.", "satin"),
        ("matt", "Matt", "Keine Spiegelung, klare Linien. Nicht polieren und nicht wachsen, sonst entstehen glänzende Stellen.", "matt"),
        ("glitter", "Glitzer und Flakes", "Metallflocken in der Folie funkeln in der Sonne. Von dezent bis auffällig.", "glitter"),
        ("strass", "Strass", "Echte Kristall-Folie in Handarbeit, meist für Spiegelkappen, Akzente oder Showautos.", "strass"),
        ("carbon", "Carbon", "Struktur- oder Forged-Carbon-Optik für Dach, Spiegel, Innenraum und Anbauteile.", "carbon"),
        ("klar", "Lackschutz (PPF)", "Klare, dicke Schutzfolie aus Polyurethan gegen Steinschläge. Unsichtbar, auf Wunsch auch matt.", "ppf"),
      ]),
      table("Richtwerte je Familie", ["Familie", "Optik", "Pflege", "Haltbarkeit*"], [
        ["Farbe gegossen (Glanz, Satin, Matt)", "deckend", "normal", "bis 8–10 Jahre"],
        ["Metallic, Glitzer", "funkelnd", "normal", "bis ca. 6 Jahre"],
        ["Chrom, Color-Shift", "spiegelnd", "vorsichtig", "deutlich kürzer, Datenblatt beachten"],
        ["Kalandriert (günstige Folie)", "deckend", "normal", "ca. 3–5 Jahre"],
        ["Lackschutz PPF", "unsichtbar", "selbstheilend bei Wärme", "5–10 Jahre"],
      ], "* " + SRC),
      split("k3.webp", "Sportwagen in Matt Schwarz", "Gleiches Auto, andere Wirkung.",
            "<p>Matt nimmt dem Auto Glanz und macht die Form strenger. Chrom macht es laut. Satin wirkt edel. Im Fächer auf der Startseite kannst du das am selben Auto durchschalten.</p>",
            more='<a class="more" href="index.html#folie">Am Auto durchschalten</a>'),
     ],
     [("Wie viele Folien gibt es?", "Bei den großen Herstellern zusammen mehrere hundert Farben und Oberflächen. Im Fächer zeigen wir eine Auswahl, beim Termin hast du die echten Muster in der Hand."),
      ("Kann ich Folien kombinieren?", "Ja. Typisch sind Dach und Spiegel in Schwarz oder Carbon, der Rest in Farbe. Oder Lackschutz vorne und Farbe rundum."),
      ("Sieht man, dass es Folie ist?", "Bei sauberer Arbeit nicht. Wir bauen Anbauteile ab und schlagen die Folie um die Kanten ein, statt sie am Spalt abzuschneiden.")])

# ---------- Wissen ----------
page("wissen", "Wissen", "Gegossene und kalandrierte Folie, Aufbau, Haltbarkeit und Pflege.",
     "03 · Wissen", "Gegossen oder kalandriert?",
     "Der wichtigste Unterschied zwischen einer Folierung, die Jahre hält, und einer, die nach zwei Sommern schrumpft, ist die Art, wie die Folie hergestellt wurde.",
     "k2.webp", "Sportwagen in Satin Magenta", "wissen",
     [facts([("50–110 µm", "Dicke gegossener Folie"), ("100–150 µm", "Dicke kalandrierter Folie"), ("bis 10 J.", "gegossen, laut Herstellern"), ("3–5 J.", "kalandriert, typisch")], "Zahlen, die den Unterschied machen"),
      steps("So entsteht die Folie", [
        ("Gegossen (Cast)", "Flüssiges PVC wird dünn auf einen Träger gegossen und getrocknet. Die Folie hat keine innere Spannung und bleibt in jeder Sicke, in die man sie mit Wärme legt."),
        ("Kalandriert", "Die Masse wird zwischen Walzen zu einer Bahn gepresst. Die Folie ist dicker und hat Spannung, sie will zurück in ihre Form. Gut für flache Flächen, schlecht für Rundungen."),
        ("Luftkanäle im Kleber", "Feine Kanäle im Kleber lassen beim Andrücken Luft entweichen. So entstehen keine Blasen, und die Folie lässt sich vor dem endgültigen Andrücken noch korrigieren."),
        ("Schutzlaminat", "Bei bedruckten Folien schützt ein klares Laminat Druck und Farbe vor Kratzern und UV-Licht.")]),
      table("Haltbarkeit nach Fläche", ["Fläche", "Sonne", "Richtwert gegossene Farbfolie*"], [
        ["Seiten, Türen (vertikal)", "wenig direkt", "bis 8–10 Jahre"],
        ["Haube, Dach, Kofferraum (horizontal)", "viel direkt", "deutlich kürzer, oft etwa die Hälfte"],
        ["Auto in der Garage", "wenig", "eher am oberen Ende"],
        ["Laternenparker im Süden", "viel", "eher am unteren Ende"]], "* " + SRC),
      steps("Pflege", [
        ("Waschen", "Handwäsche oder Waschanlage ohne harte Bürsten. Die erste Wäsche frühestens nach einer Woche."),
        ("Hochdruck", "Mindestens 30 cm Abstand, nie direkt auf Kanten und Nähte halten."),
        ("Matt und Satin", "Nicht polieren und kein Wachs. Spezielle Matt-Pflegemittel verwenden."),
        ("Vogelkot, Harz, Insekten", "Schnell abwaschen, sie greifen auch Folie an.")]),
     ],
     [("Schadet Folie dem Lack?", "Nein, auf intaktem Originallack schützt sie ihn sogar. Beim Abziehen kann nur nachlackierter oder beschädigter Lack mitkommen."),
      ("Was passiert nach Ablauf der Haltbarkeit?", "Die Folie wird spröder und lässt sich schwerer abziehen. Darum rechtzeitig wechseln oder entfernen lassen."),
      ("Warum ist gegossene Folie teurer?", "Die Herstellung ist aufwendiger, die Folie dünner und stabiler. Am Auto spart sie Arbeit an Rundungen und hält länger.")])

# ---------- Handwerk ----------
page("handwerk", "Handwerk und Ablauf", "Demontage, Reinigung, Auflegen, Einschlagen, Nachwärmen, Endkontrolle.",
     "04 · Handwerk", "Eingeschlagen. Nicht abgeschnitten.",
     "Eine Folierung sieht nur dann aus wie Lack, wenn die Folie um die Kanten läuft. Dafür kommen Teile ab. Das dauert länger, und genau das sieht man.",
     "m1.webp", "Rakel drückt Chromfolie in eine Sicke", "handwerk",
     [split("ab1.webp", "Demontage von Stoßstange und Spiegeln", "1 · Demontage",
            "<p>Stoßstangen, Spiegel, Griffe, Leuchten und Embleme kommen ab. Nur so lässt sich die Folie um jede Kante legen. Alles wird beschriftet und auf gepolsterten Wagen abgelegt.</p>"),
      split("ab2.webp", "Zwei Folierer legen eine große Folienbahn auf", "2 · Reinigen und Auflegen",
            "<p>Erst Wäsche, dann Reinigungsknete und Entfetter, bis kein Wachs und kein Staub mehr auf dem Lack ist. Große Teile wie die Haube werden zu zweit in einem Stück belegt.</p>", rev=True),
      steps("Der ganze Ablauf", [
        ("Annahme mit Fotos", "Wir fotografieren den Lack rundum und notieren Vorschäden. Die Fotos bekommst du aufs Handy."),
        ("Demontage", "Anbauteile ab, alles beschriftet."),
        ("Reinigen", "Wäsche, Knete, Entfetter. Lackschäden werden vorher besprochen."),
        ("Auflegen", "Folie spannungsfrei auflegen, mit der Rakel mit Filzkante von der Mitte nach außen andrücken."),
        ("Einschlagen", "Mit Wärme um Kanten und in Falze legen, Kanten sauber schneiden, ohne den Lack zu berühren."),
        ("Nachwärmen", "Kanten und gedehnte Stellen auf die Temperatur aus dem Datenblatt bringen, damit die Folie ihre neue Form behält."),
        ("Montage", "Alle Teile zurück, Funktionen prüfen."),
        ("Endkontrolle", "Mit Lichtleiste jede Fläche prüfen, letzte Fotos, Übergabe mit Pflegehinweisen.")]),
      split("ab3.webp", "Endkontrolle mit LED-Lichtleiste", "Endkontrolle mit Licht",
            "<p>Eine lange LED-Leiste wird über jede Fläche geführt. Gerade Lichtlinien zeigen, dass nichts eingeschlossen ist. Erst dann geht das Auto raus.</p>"),
      facts([("3–5 Tage", "typische Dauer einer Vollfolierung"), ("8", "Arbeitsschritte"), ("0", "Schnitte auf dem Lack")]),
     ],
     [("Wie lange ist mein Auto weg?", "Für eine Vollfolierung meist drei bis fünf Werktage, je nach Modell und Folie. Chrom dauert länger."),
      ("Wird auf meinem Lack geschnitten?", "Nein. Geschnitten wird an Kanten, die später verdeckt sind, oder mit Schneideband unter der Folie."),
      ("Was ist mit Türfalzen und Einstiegen?", "Auf Wunsch folieren wir Einstiege und Falze mit, dann sieht man auch bei offener Tür keinen Originallack.")])

# ---------- Referenzen ----------
page("referenzen", "Referenzen", "Folierte Autos: Holografik-Linien, Strass, Forged Carbon.",
     "05 · Referenzen", "Referenzen, die für sich sprechen.",
     "Drei Beispiele aus dem Fächer. Demo: Bilder sind gestaltete Beispiele, keine echten Kundenaufträge.",
     "r0.webp", "Drei folierte Sportwagen", "referenzen",
     [split("r1.webp", "Matt schwarzer Sportwagen mit holografischen Linien", "Holografik Linien",
            "<p>Matt Schwarz als Grund, darüber schmale Linien aus holografischer Folie. Die Linien laufen über die Sicken und werden von Hand gesetzt.</p><ul class='ul'><li>Folie: Matt Schwarz gegossen + Holo-Streifen</li><li>Aufwand: Vollfolierung + Linien von Hand</li></ul>"),
      split("r2.webp", "Coupé mit Strass-Folie", "Crystal Rhinestone",
            "<p>Tausende kleine Kristalle auf Trägerfolie, Bahn für Bahn verlegt. Für Showautos, Events und alle, die nicht übersehen werden wollen.</p><ul class='ul'><li>Folie: Strass auf Trägerfolie</li><li>Aufwand: Handarbeit, mehrere Tage</li></ul>", rev=True),
      split("r3.webp", "Kompaktsportler in Forged-Carbon-Optik", "Forged Carbon",
            "<p>Marmorierte Carbon-Optik am ganzen Auto, satin versiegelt. Wirkt wie Sichtcarbon, wiegt aber nichts extra.</p><ul class='ul'><li>Folie: Forged-Carbon-Struktur</li><li>Aufwand: Vollfolierung</li></ul>"),
      '<section class="sub-note"><p><b>Bewertungen:</b> Hier erscheinen im echten Betrieb die Google-Bewertungen mit Note, Anzahl und Link. Diese Demo zeigt keine erfundenen Bewertungen.</p></section>',
     ])

# ---------- Alles folierbar ----------
page("alles-folierbar", "Alles folierbar", "Boote, Motorräder, Schaufenster, Werbeflächen, Fuhrpark, Konsolen und Möbel.",
     "06 · Alles folierbar", "Vom Boot bis zur Konsole.",
     "Was eine glatte Fläche hat, kann Folie bekommen. Die Folie ist je nach Untergrund eine andere, das Handwerk bleibt dasselbe.",
     "a1.webp", "Sportboot in Color-Shift-Chrom", "alles",
     [split("a1.webp", "Sportboot", "Boote", "<p id='boote'>Rumpf und Aufbauten in Farbe oder mit Design. Für Wasserkontakt gibt es spezielle Marine-Folien. Das Boot kommt auf dem Trailer zu uns.</p>"),
      split("a2.webp", "Motorradtank in Holo-Folie", "Motorrad", "<p id='motorrad'>Tank, Verkleidung, Felgenränder. Kleine Teile mit vielen Rundungen, ideal für gegossene Folie oder Lackschutz am Tank.</p>", rev=True),
      split("a3.webp", "Schaufenster mit Fensterfolie", "Schaufenster und Werbeflächen", "<p id='schaufenster'>Fensterbeschriftung, Sichtschutz, Milchglas-Optik, Wandflächen und Messewände. Auf Wunsch nachts, damit das Geschäft offen bleibt.</p>"),
      split("f1.webp", "Transporter wird mit Firmendesign foliert", "Fuhrpark", "<p id='fuhrpark'>Firmendesign auf Transportern und Pkw, auch als Serie. Wir folieren nachts und am Wochenende, damit kein Auto im Betrieb fehlt. Bei Leasing-Rückgabe kommt alles rückstandsfrei ab.</p>", rev=True),
      split("a4.webp", "Spielkonsole mit Holo-Skin und Controller", "Konsole, Laptop, Möbel", "<p id='konsole'>Bei Konsolen kommen nur die Seitenplatten und der Controller unter Folie, der schwarze Kern bleibt frei, damit Lüftung und Anschlüsse funktionieren. Dazu Laptops, Küchenfronten, Türen. Kleine Aufträge erledigen wir oft am selben Tag.</p>"),
     ],
     [("Geht Folie auch auf Holz oder Kunststoff?", "Auf glatten, versiegelten Flächen ja. Rohes Holz und weiche Kunststoffe müssen vorbehandelt werden."),
      ("Wie lange hält Fensterfolie?", "Innen viele Jahre, außen je nach Folie und Sonne kürzer. Wir beraten passend zum Fenster.")])

# ---------- Karriere ----------
page("karriere", "Karriere", "Folierer werden: Quereinstieg mit Anlernen, Hersteller-Zertifikat bezahlt.",
     "08 · Karriere", "Feste Crew. Führerschein. Zertifikat? Zahlen wir.",
     "Folierer ist kein Ausbildungsberuf. Du lernst bei uns im Team und machst die Hersteller-Schulung auf unsere Kosten.",
     "j1.webp", "Junger Folierer mit Heißluftföhn und Musterfächer", "karriere",
     [facts([("Quereinstieg", "mit Anlernen im Team"), ("Zertifikat", "Hersteller-Schulung bezahlen wir"), ("Führerschein", "Klasse B zahlen wir mit"), ("Feste Crew", "keine Leiharbeit")], "Was wir bieten"),
      steps("Wen wir suchen", [
        ("Quereinsteiger", "Du arbeitest genau, hast ruhige Hände und Geduld. Den Rest zeigen wir dir."),
        ("Fahrzeuglackierer/in", "Du kennst Lack, Untergründe und Karosserie. Ideal für Lackschutz und Endkontrolle."),
        ("Schilder- und Lichtreklamehersteller/in", "Du kennst Folie, Plotter und Werbetechnik. Ideal für Fuhrpark und Schaufenster.")]),
      steps("So läuft die Bewerbung", [
        ("60 Sekunden", "Vier Fragen beantworten, kein Lebenslauf nötig."),
        ("Anruf", "Wir melden uns innerhalb von zwei Tagen."),
        ("Probetag", "Einen Tag mitarbeiten, bezahlt."),
        ("Start", "Einarbeitung im Team, Schulung im ersten Jahr.")]),
     ],
     [("Brauche ich eine Ausbildung?", "Nein. Folierer ist kein anerkannter Ausbildungsberuf. Wichtiger sind Sorgfalt und Lust aufs Handwerk."),
      ("Gibt es eine Ausbildung bei euch?", "Passende anerkannte Ausbildungen sind Fahrzeuglackierer/in und Schilder- und Lichtreklamehersteller/in. Sprich uns an."),
      ("Wie sind die Arbeitszeiten?", "Tagschicht, für Fuhrpark-Aufträge auch mal nachts oder am Wochenende, mit Ausgleich.")],
     extra='<section class="sub-cta"><h2>In 60 Sekunden bewerben</h2><p>Vier Fragen, kein Lebenslauf.</p><div class="row"><a class="btn holo-b" href="index.html#karriere">Zur Bewerbung</a></div></section>')

# ---------- Angebot ----------
page("angebot", "Angebot per Foto", "Drei Fotos, Modell, Wunschfolie: festes Angebot ohne Anfahrt. Live-Status während der Folierung.",
     "09 · Angebot", "Drei Fotos. Ein festes Angebot.",
     "Kein Vorbeikommen zum Schätzen, keine Rückrufschleife. Aus Fotos, Modell und Wunschfolie entsteht ein Angebot, das hält.",
     "k0.webp", "Sportwagen in Color-Shift-Folie", "angebot",
     [steps("So läuft es ab", [
        ("Fotos", "Front, Seite, Heck. Bei Lackschäden ein Foto aus der Nähe."),
        ("Folie wählen", "Am Fächer oder im Konfigurator auf der Startseite. Unsicher? Wir empfehlen."),
        ("Angebot", "Festes Angebot mit Dauer und Termin, meist am nächsten Werktag."),
        ("Termin", "Abgabe am Morgen, Annahme mit Fotos."),
        ("Live-Status", "Jeder Schritt kommt mit Foto aufs Handy: Angenommen, Demontage, Folie, Endkontrolle, Abholbereit."),
        ("Abholung", "Übergabe mit Pflegehinweisen.")]),
      facts([("3", "Fotos reichen"), ("1 Werktag", "bis zum Angebot, meist"), ("5", "Live-Status-Schritte")]),
      steps("Auch möglich", [
        ("Leasing-Rückgabe", "Folie ab, Lack wie neu. Wir entfernen Folie rückstandsfrei vor der Rückgabe."),
        ("Lackschutz", "Nur Front, Front und Spiegel oder komplett in klarer Lackschutzfolie."),
        ("Scheibentönung", "Hintere Scheiben, nur mit zugelassener Folie und Prüfzeichen."),
        ("Fuhrpark", "Serienangebot für mehrere Fahrzeuge, Arbeit nachts oder am Wochenende.")]),
     ],
     [("Warum stehen keine Preise auf der Seite?", "Weil der Preis vom Modell, von der Folie und vom Zustand des Lacks abhängt. Mit Fotos bekommst du einen festen Preis statt einer Spanne."),
      ("Was, wenn mein Lack Schäden hat?", "Wir sehen es auf den Fotos und sagen dir vorher, was das bedeutet. Folie deckt keine Dellen ab."),
      ("Wird meine Anfrage gespeichert?", "Demo: Diese Seite sendet nichts. Im echten Betrieb nur für das Angebot.")],
     extra='<section class="sub-cta"><h2>Jetzt Fotos machen</h2><div class="row"><a class="btn holo-b" href="index.html#angebot">Zum Angebot per Foto</a></div></section>')

# ---------- Impressum ----------
o = head("Impressum", "Impressum der Demo-Seite")
o += """<main class="sub-main"><section class="sub-legal"><a class="back" href="index.html">← Zur Startseite</a><h1>Impressum</h1>
<p>Dies ist eine Demo-Seite. SCHICHTWECHSEL ist ein erfundenes Unternehmen. Es gibt keine Firma, keine Anschrift und keine Leistungen unter diesem Namen.</p>
<p>Formulare senden nichts. Es werden keine Daten gespeichert. Bilder sind gestaltete Beispiele, keine echten Kundenaufträge. Die Autos sind ohne Marken- und Herstellerzeichen dargestellt.</p>
</section></main>
<footer class="foot"><div><b>SCHICHTWECHSEL</b><br>Demo-Unternehmen</div><div><a href="index.html">Startseite</a></div><div><a href="angebot.html">Angebot</a></div></footer>
<script src="assets/js/sub.js"></script></body></html>"""
open(os.path.join(ROOT, "impressum.html"), "w").write(o)
print("ok")
