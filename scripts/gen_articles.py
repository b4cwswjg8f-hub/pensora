#!/usr/bin/env python3
"""Generate 14 SEO article pages for Pensora public/ directory."""
import os, json, textwrap

BASE = os.path.join(os.path.dirname(__file__), '..', 'public')

FONT = "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap"

CSS = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{color-scheme:dark;--bg:#000;--bg1:#0a0a0a;--bg2:#111;--line:#1c1c1c;--fg:#fafafa;--fg2:#a3a3a3;--fg3:#6b6b6b;--loss:#FF6B6B;--green:#4ade80;--amber:#fbbf24;--rmd:12px;--rlg:18px;}
html,body{min-height:100%;background:var(--bg);color:var(--fg);font-family:'Plus Jakarta Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.55;letter-spacing:-.01em}
a{color:inherit;text-decoration:none}button{font-family:inherit;cursor:pointer}
.nav{display:flex;align-items:center;justify-content:space-between;padding:18px 56px;border-bottom:1px solid var(--line);background:rgba(0,0,0,.85);backdrop-filter:blur(20px);position:sticky;top:0;z-index:10}
.brand{display:flex;align-items:center;gap:10px;font-weight:600;font-size:17px;letter-spacing:-.035em;color:var(--fg)}
.btnp{height:44px;padding:0 22px;border-radius:8px;border:none;background:var(--fg);color:var(--bg);font-size:14px;font-weight:600;cursor:pointer}
.btn{height:44px;padding:0 22px;border-radius:8px;border:1px solid var(--line);background:transparent;color:var(--fg2);font-size:14px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;text-decoration:none}
.wrap{max-width:900px;margin:0 auto;padding:72px 56px}
h1{font-size:52px;line-height:1.02;letter-spacing:-.03em;font-weight:700;margin-bottom:24px}
.lead{font-size:18px;color:var(--fg2);line-height:1.6;margin-bottom:40px}
.intro{font-size:16px;color:var(--fg2);line-height:1.7;margin-bottom:48px}
.intro p{margin-bottom:16px}
.intro h2{font-size:22px;font-weight:700;letter-spacing:-.02em;margin:32px 0 12px;color:var(--fg)}
.intro ul{padding-left:20px;margin-bottom:16px}
.intro ul li{margin-bottom:8px}
.kpi-row{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:24px 0}
.kpi{background:var(--bg1);border:1px solid var(--line);border-radius:14px;padding:20px}
.kpi-val{font-size:28px;font-weight:700;letter-spacing:-.03em;margin-bottom:4px}
.kpi-lbl{font-size:11px;color:var(--fg3);text-transform:uppercase;letter-spacing:.1em}
.data-table{width:100%;border-collapse:collapse;margin:20px 0 24px;font-size:14px}
.data-table th{text-align:left;padding:10px 0;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--fg3);font-weight:500;border-bottom:1px solid var(--line)}
.data-table td{padding:11px 0;border-bottom:1px solid var(--line);color:var(--fg2)}
.data-table td:last-child{text-align:right;font-weight:500;color:var(--fg)}
.cta-box{background:var(--bg1);border:1px solid var(--line);border-radius:var(--rlg);padding:40px;margin-bottom:56px;display:flex;align-items:center;justify-content:space-between;gap:32px}
.cta-box h2{font-size:28px;font-weight:700;letter-spacing:-.025em;margin-bottom:8px}
.cta-box p{font-size:15px;color:var(--fg2);max-width:52ch}
.faq{margin-top:64px}
.faq h2{font-size:32px;font-weight:700;letter-spacing:-.025em;margin-bottom:32px}
.faq-item{padding:24px 0;border-top:1px solid var(--line)}
.faq-item:last-child{border-bottom:1px solid var(--line)}
.faq-q{font-size:17px;font-weight:700;letter-spacing:-.01em;margin-bottom:12px}
.faq-a{font-size:15px;color:var(--fg2);line-height:1.65}
.eyebrow{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--fg3);font-weight:600;margin-bottom:16px}
footer{border-top:1px solid var(--line);padding:40px 56px;display:flex;justify-content:space-between;align-items:center;font-size:13px;color:var(--fg3)}
footer a{color:var(--fg3);margin-left:24px}
@media(max-width:700px){.wrap{padding:40px 24px}h1{font-size:36px}.cta-box{flex-direction:column}.nav{padding:14px 24px}.kpi-row{grid-template-columns:1fr}footer{flex-direction:column;gap:16px;padding:32px 24px}}"""

NAV = """<nav class="nav">
  <a class="brand" href="../"><svg width="22" height="24" viewBox="0 0 22 24" fill="currentColor" style="flex-shrink:0"><rect x="3" y="2" width="3.2" height="20" rx="0.4"/><circle cx="15" cy="8" r="5"/></svg> Pensora</a>
  <div style="display:flex;gap:12px;align-items:center">
    <a class="btn" href="../">← Alle Rechner</a>
    <button class="btnp" onclick="window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach','_blank')">Beratung buchen</button>
  </div>
</nav>"""

FOOT = """<footer>
  <a class="brand" href="../" style="font-size:15px"><svg width="22" height="24" viewBox="0 0 22 24" fill="currentColor" style="flex-shrink:0"><rect x="3" y="2" width="3.2" height="20" rx="0.4"/><circle cx="15" cy="8" r="5"/></svg> Pensora</a>
  <div><a href="../">Alle Rechner</a><a href="#">Impressum</a><a href="#">Datenschutz</a></div>
</footer>"""

def cta(calc_id, calc_label, cta_title, cta_desc):
    return f"""<div class="cta-box">
    <div>
      <h2>{cta_title}</h2>
      <p>{cta_desc}</p>
    </div>
    <div style="flex-shrink:0">
      <button class="btnp" style="height:52px;padding:0 32px;font-size:16px" onclick="window.location='../#{calc_id}'">
        {calc_label} →
      </button>
    </div>
  </div>"""

def red_cta():
    return """<div class="cta-box" style="margin-top:64px;margin-bottom:0;border-color:var(--loss);background:rgba(255,107,107,0.06)">
    <div>
      <h2 style="color:var(--loss)">Erkennst du eine Lücke?</h2>
      <p>30 Minuten kostenloses Gespräch mit einem unabhängigen Finanzberater. Kein Verkauf, keine Provision.</p>
    </div>
    <div style="flex-shrink:0">
      <button class="btnp" style="height:52px;padding:0 32px;font-size:16px;background:var(--loss)" onclick="window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach','_blank')">
        Termin buchen →
      </button>
    </div>
  </div>"""

def kpi(items):
    cells = ''.join(f'<div class="kpi"><div class="kpi-val">{v}</div><div class="kpi-lbl">{l}</div></div>' for v,l in items)
    return f'<div class="kpi-row">{cells}</div>'

def faq_items(pairs):
    items = ''.join(f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q,a in pairs)
    return f'<div class="faq"><h2>Häufige Fragen</h2>{items}</div>'

def ld_article(title, url, date_pub="2026-05-29", date_mod="2026-05-29"):
    return {"@context":"https://schema.org","@type":"Article","headline":title,
            "author":{"@type":"Person","name":"Niall Bradfield","jobTitle":"unabhängiger Finanzberater",
                      "address":{"@type":"PostalAddress","addressLocality":"Stuttgart","addressCountry":"DE"},
                      "url":"https://pensora.de/ueber-uns"},
            "publisher":{"@type":"Organization","name":"Pensora","url":"https://pensora.de"},
            "datePublished":date_pub,"dateModified":date_mod,"url":url}

def ld_faq(pairs):
    return {"@context":"https://schema.org","@type":"FAQPage",
            "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in pairs]}

def page(slug, title, meta_desc, og_desc, eyebrow, h1, lead, content_html, calc_id, calc_label, cta_title, cta_desc, faq_pairs, kpi_items, ld_extra=None):
    url = f"https://pensora.de/{slug}/"
    scripts = [json.dumps(ld_article(title, url), ensure_ascii=False, indent=2)]
    if ld_extra:
        scripts.append(json.dumps(ld_extra, ensure_ascii=False, indent=2))
    scripts.append(json.dumps(ld_faq(faq_pairs), ensure_ascii=False, indent=2))
    ld_tags = '\n'.join(f'<script type="application/ld+json">\n{s}\n</script>' for s in scripts)
    faq_html = faq_items(faq_pairs)
    kpi_html = kpi(kpi_items)
    main_cta = cta(calc_id, calc_label, cta_title, cta_desc)
    html = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Pensora</title>
<meta name="description" content="{meta_desc}">
<meta property="og:title" content="{title} — Pensora">
<meta property="og:description" content="{og_desc}">
<meta property="og:type" content="article">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 22 24'%3E%3Crect x='3' y='2' width='3.2' height='20' rx='0.4' fill='%23fafafa'/%3E%3Ccircle cx='15' cy='8' r='5' fill='%23fafafa'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="{FONT}" rel="stylesheet">
<style>
{CSS}
</style>
{ld_tags}
</head>
<body>
{NAV}
<div class="wrap">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
  {main_cta}
  <div class="intro">
    {kpi_html}
    {content_html}
  </div>
  {faq_html}
  {red_cta()}
</div>
{FOOT}
</body>
</html>"""
    out = os.path.join(BASE, slug)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✓  {slug}/')

# ─────────────────────────────────────────────────────────────────────────────
# ARTICLE DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

articles = []

# 1. Riester Nachfolger
articles.append(dict(
    slug="riester-nachfolger",
    title="Riester Nachfolger 2027 — Das Altersvorsorgedepot kommt",
    meta_desc="Riester wird abgelöst: Das neue Altersvorsorgedepot 2027 erlaubt ETF-Investitionen mit staatlicher Förderung. Was passiert mit deinem Riester-Vertrag?",
    og_desc="Riester-Rente läuft aus. Was kommt danach, was passiert mit bestehenden Verträgen und wer profitiert vom neuen Altersvorsorgedepot?",
    eyebrow="Altersvorsorge · Reform 2027 · Riester-Ablösung",
    h1="Riester Nachfolger 2027",
    lead="Die Riester-Rente wird abgelöst. Ab 2027 ersetzt das Altersvorsorgedepot das gescheiterte Riester-System — mit ETFs statt Versicherungsprodukten, besserer Rendite und weniger Bürokratie.",
    calc_id="depot",
    calc_label="AV-Depot-Rechner",
    cta_title="Jetzt Vorsorgelücke berechnen",
    cta_desc="Mit dem AV-Depot-Rechner siehst du, wie viel du monatlich sparen musst, um deine Rentenlücke bis zur Rente zu schließen.",
    kpi_items=[("2027", "Start Nachfolger"), ("540 €", "Grundzulage/Jahr"), ("30 %", "Max. Teilkapitalisierung")],
    content_html="""<h2>Warum wird Riester abgelöst?</h2>
    <p>Riester scheiterte an drei strukturellen Problemen: Die erzwungene 100-%-Beitragsgarantie verhinderte renditestarke Aktienquoten, die Produktlandschaft war mit über 13 Millionen Verträgen komplex und teuer, und knapp 40 % aller Verträge wurden ruhend gestellt — ein eindeutiges Zeichen für mangelnde Akzeptanz.</p>
    <p>Der Kommissionsbericht zur Reform der privaten Altersvorsorge (2024) empfahl daher eine grundlegende Neuaufstellung: einfachere Produkte, ETFs als zulässige Anlageform, keine Beitragsgarantie und eine deutliche Reduzierung der Produkttypen.</p>
    <h2>Was passiert mit bestehenden Riester-Verträgen?</h2>
    <p>Bestehende Riester-Verträge laufen weiter und werden nicht zwangsbeendet. Vorgesehen ist eine Übergangslösung:</p>
    <ul>
      <li><strong>Weiterführung möglich</strong>: Wer keinen Handlungsbedarf sieht, kann den Riester-Vertrag bis zur Auszahlungsphase laufen lassen</li>
      <li><strong>Übertragung</strong>: Guthaben soll in ein Altersvorsorgedepot übertragbar sein (Details offen)</li>
      <li><strong>Kündigung prüfen</strong>: Bei schlechten Konditionen (hohe Kosten, niedrige Überschüsse) lohnt sich ein Vergleich — Beratung empfohlen</li>
    </ul>
    <h2>Altersvorsorgedepot vs. Riester im Vergleich</h2>
    <table class="data-table">
      <thead><tr><th>Merkmal</th><th>Riester</th><th>AV-Depot 2027</th></tr></thead>
      <tbody>
        <tr><td>Anlageform</td><td>Versicherung, Bankspar, Fonds</td><td>ETFs, Aktien, Fonds</td></tr>
        <tr><td>Beitragsgarantie</td><td>100 % Pflicht</td><td>Keine (geplant)</td></tr>
        <tr><td>Grundzulage</td><td>175 €/Jahr</td><td>540 €/Jahr</td></tr>
        <tr><td>Kinderzulage</td><td>300 €/Jahr</td><td>300 €/Jahr (ähnlich)</td></tr>
        <tr><td>Selbständige</td><td>Ausgeschlossen</td><td>Einbezogen (geplant)</td></tr>
        <tr><td>Renditepotenzial</td><td>Niedrig (Ø ~1–2 %)</td><td>Hoch (hist. ~7 % ETF)</td></tr>
      </tbody>
    </table>
    <h2>Handlungsempfehlungen</h2>
    <p>Wer noch keinen Riester-Vertrag hat: jetzt ein reguläres ETF-Depot starten — dieses kann 2027 als AV-Depot zertifiziert werden. Wer einen alten Riester-Vertrag hat: Kosten und Überschüsse prüfen lassen, ggf. in ETF-Depot wechseln.</p>""",
    faq_pairs=[
        ("Wann kommt der Riester-Nachfolger?", "Das Altersvorsorgedepot soll zum 01.01.2027 starten. Das Gesetz (Altersvorsorge-Stärkungsgesetz) befindet sich im Gesetzgebungsverfahren."),
        ("Was passiert mit meinem Riester-Vertrag?", "Bestehende Verträge laufen weiter. Eine Übertragung des Guthabens in ein Altersvorsorgedepot soll möglich sein. Kündigung lohnt sich bei schlechten Konditionen — vorher Beratung einholen."),
        ("Ist das Altersvorsorgedepot besser als Riester?", "Für die meisten ja: höhere Grundzulage (540 € statt 175 €), ETFs erlaubt, kein Renditeverlust durch Beitragsgarantie. Für ältere Sparer mit kurzer Restlaufzeit ist der Vergleich individuell."),
        ("Für wen lohnt sich das neue AV-Depot besonders?", "Besonders für jüngere Erwerbstätige unter 45 Jahren mit langer Ansparphase, Selbständige (neu: förderberechtigt) und Familien mit Kindern, die von der Kinderzulage profitieren."),
    ]
))

# 2. Frühstartrente Kinder
articles.append(dict(
    slug="fruehstartrente-kinder",
    title="Frühstartrente für Kinder — Altersvorsorge ab Geburt",
    meta_desc="Frühstartrente: Der Staat zahlt 10 € monatlich für jedes Kind von 6–18 Jahren. Was das bedeutet, wie das Geld angelegt wird und wie Eltern profitieren.",
    og_desc="Frühstartrente 2026: 10 € monatlich vom Staat für Kinder. Wie wird das Geld angelegt, wann kann man es abrufen und was bringt das wirklich?",
    eyebrow="Altersvorsorge · Kinder · Frühstartrente",
    h1="Frühstartrente für Kinder",
    lead="Der Staat zahlt 10 € monatlich für jedes Kind zwischen 6 und 18 Jahren als Startkapital für die Altersvorsorge. Eltern können parallel privat einzahlen. Was das wirklich bringt — nüchtern betrachtet.",
    calc_id="depot",
    calc_label="AV-Depot-Rechner",
    cta_title="Wie viel wird aus dem Startkapital?",
    cta_desc="Mit dem AV-Depot-Rechner siehst du, wie sich die staatlichen 10 €/Monat über 50+ Jahre bei 6 % Rendite zu echtem Kapital entwickeln.",
    kpi_items=[("10 €/Mo", "Staatliche Einzahlung"), ("6–18", "Altersspanne"), ("50+ J.", "Ansparhorizont")],
    content_html="""<h2>Was ist die Frühstartrente?</h2>
    <p>Die Frühstartrente ist ein Bestandteil der geplanten Altersvorsorge-Reform. Der Staat zahlt für jedes Kind zwischen 6 und 18 Jahren automatisch 10 € pro Monat (120 €/Jahr) in ein gesperrtes Depot ein. Das Geld wird in einen kostengünstigen ETF investiert und kann erst ab dem Rentenalter abgerufen werden.</p>
    <p>Ziel: Altersvorsorge von Geburt an normalisieren, Zinseszinseffekt maximieren und die nächste Generation nicht mit leeren Händen in die Rente schicken.</p>
    <h2>Was bringt das rechnerisch?</h2>
    <p>Bei 10 € monatlich über 12 Jahre (6–18 Lebensjahr) = 1.440 € Einzahlung. Bei angenommenen 7 % Jahresrendite über 47 weitere Jahre (bis Alter 65) wächst dieses Kapital auf ca. <strong>28.000–32.000 €</strong>. Kein riesiger Betrag, aber ein solider Grundstock.</p>
    <p>Eltern können zusätzlich privat einzahlen: Wer selbst 25 €/Monat ab Geburt spart, erreicht bei gleicher Rendite über 65 Jahre ca. 180.000 €.</p>
    <h2>Kann ich als Elternteil zuzahlen?</h2>
    <p>Ja. Die Frühstartrente soll als Basis-Depot funktionieren, in das Eltern, Großeltern oder das Kind selbst zusätzlich einzahlen können — sofern die gesetzliche Ausgestaltung das erlaubt (Details noch offen). Empfehlung: Parallel ein reguläres ETF-Depot für das Kind eröffnen, das 2027 als Altersvorsorgedepot zertifiziert werden kann.</p>
    <h2>Wann ist die Frühstartrente beschlossen?</h2>
    <p>Der Koalitionsvertrag 2025 der neuen Bundesregierung enthält die Frühstartrente als geplante Maßnahme. Genaues Startdatum und Details zur Umsetzung sind noch nicht final beschlossen. Aktueller Stand: Referentenentwurf in Vorbereitung für 2026.</p>""",
    faq_pairs=[
        ("Was ist die Frühstartrente für Kinder?", "Der Staat zahlt 10 € monatlich für jedes Kind von 6–18 Jahren in ein gesperrtes ETF-Depot. Das Kapital kann ab Rentenalter abgerufen werden."),
        ("Wie viel Geld kommt durch die Frühstartrente zusammen?", "Bei 10 €/Monat über 12 Jahre (Einzahlung: 1.440 €) und 7 % Jahresrendite über weitere 47 Jahre bis Alter 65 entstehen ca. 28.000–32.000 €."),
        ("Können Eltern zusätzlich einzahlen?", "Grundsätzlich ja — Details zur Zuzahlungsmöglichkeit sind noch nicht final beschlossen. Empfehlung: Parallel ein reguläres ETF-Kinderdepot eröffnen."),
        ("Ab wann gibt es die Frühstartrente?", "Im Koalitionsvertrag 2025 angekündigt. Konkretes Startdatum noch nicht beschlossen. Voraussichtlich 2026 oder 2027."),
    ]
))

# 3. AltersvorsorgeDepot Beamte
articles.append(dict(
    slug="altersvorsorgedepot-beamte",
    title="Altersvorsorgedepot für Beamte — Lohnt es sich?",
    meta_desc="Altersvorsorgedepot 2027 für Beamte: Wer ist förderberechtigt, wie hoch ist der Steuerbonus und wann lohnt das AV-Depot trotz guter Pension?",
    og_desc="Beamte und das neue Altersvorsorgedepot 2027: Förderung, Steuervorteil, Versorgungslücken schließen. Was ist für Beamte sinnvoll?",
    eyebrow="Beamte · Altersvorsorge · AV-Depot 2027",
    h1="Altersvorsorgedepot für Beamte",
    lead="Beamte haben eine gute Grundversorgung — aber nicht immer eine lückenlose. Das neue Altersvorsorgedepot 2027 kann auch für Beamte sinnvoll sein: für Teilzeit-Phasen, Elternzeit oder einfach mehr finanzielle Unabhängigkeit.",
    calc_id="pension",
    calc_label="Pensionsrechner",
    cta_title="Versorgungslücke berechnen",
    cta_desc="Mit dem Pensionsrechner siehst du, wie hoch deine Pension wirklich ist — und ob ein AV-Depot sinnvoll deine Lücke schließt.",
    kpi_items=[("71,75 %", "Max. Ruhegehaltssatz"), ("2 % / J.", "Steigerung p. a."), ("40 J.", "Vollversorgung")],
    content_html="""<h2>Sind Beamte für das Altersvorsorgedepot förderberechtigt?</h2>
    <p>Aktueller Planungsstand: Ja. Beamte sollen — anders als bei Riester, wo sie als mittelbar Zulagenberechtigte galten — beim Altersvorsorgedepot direkt einbezogen werden. Die genaue Ausgestaltung (Grundzulage, Steuerbonus, Mindestbeitrag) ist noch nicht final beschlossen.</p>
    <p>Bei Riester hatten Beamte nur Anspruch auf die Grundzulage, wenn sie selbst Beiträge einzahlten. Beim neuen System soll der Zugang einfacher werden.</p>
    <h2>Wann lohnt sich das AV-Depot trotz Pension?</h2>
    <p>Die Beamtenpension ist eine gute Grundlage, aber nicht in jedem Fall lückenlos:</p>
    <ul>
      <li><strong>Teilzeit-Phasen</strong>: Jedes Teilzeitjahr reduziert den Ruhegehaltssatz — A13-Beamte verlieren pro Teilzeitjahr ca. 0,7–1,0 % Ruhegehaltssatz dauerhaft</li>
      <li><strong>Elternzeit</strong>: Bis zu 3 Jahre pro Kind zählen nicht als ruhegehaltsfähige Dienstzeit (außer Erziehungsurlaub bei Kindern vor 1992)</li>
      <li><strong>Frühpensionierung</strong>: Abzug von 3,6 % pro Jahr vor Regelpensionsalter</li>
      <li><strong>PKV-Kosten im Ruhestand</strong>: Ohne Beihilfe-Ergänzung können die Beiträge im Alter erheblich steigen</li>
    </ul>
    <h2>Steuerbonus: Wann lohnt sich der Abzug?</h2>
    <p>Beamte ab A13/E13 haben häufig Grenzsteuersätze von 35–42 %. Bei einem Steuerbonus von bis zu 2.100 €/Jahr (Sonderausgabenabzug) entstehen jährliche Steuerersparnisse von 735–882 €. Das ist ein klarer Vorteil gegenüber einem regulären Depot ohne Steuerbegünstigung.</p>
    <h2>Was sollten Beamte jetzt tun?</h2>
    <p>Da das AV-Depot erst 2027 startet und bestehende ETF-Depots zertifiziert werden sollen: Jetzt ein reguläres ETF-Depot eröffnen, konsequent besparen und 2027 den Zertifizierungsantrag stellen. Parallel: Pensionsrechner nutzen, um die individuelle Versorgungslücke zu kennen.</p>""",
    faq_pairs=[
        ("Sind Beamte beim Altersvorsorgedepot 2027 förderberechtigt?", "Laut aktuellem Planungsstand ja. Beamte sollen direkt einbezogen werden — anders als bei Riester, wo sie nur mittelbar zulageberechtigt waren."),
        ("Lohnt sich das AV-Depot trotz Pension?", "Ja, besonders bei Teilzeit-Phasen, Elternzeit, frühem Pensionseintritt oder hohem PKV-Beitrag im Ruhestand. Wer eine Versorgungslücke hat, sollte handeln."),
        ("Wie hoch ist der Steuerbonus für Beamte?", "Bei Grenzsteuersatz 42 % und max. Abzug 2.100 €/Jahr: 882 € Steuerersparnis jährlich. Bei 35 %: 735 €/Jahr."),
        ("Was ist der Unterschied zum Rürup-Vertrag?", "Rürup ist eine Rentenversicherung mit lebenslanger Auszahlung und höherem Steuerbonus (bis 27.565 €/Jahr absetzbar). Das AV-Depot erlaubt flexible Kapitalanlage in ETFs. Für Beamte kann Rürup ab Grenzsteuer 40 %+ attraktiver sein."),
    ]
))

# 4. AltersvorsorgeDepot Förderung
articles.append(dict(
    slug="altersvorsorgedepot-foerderung",
    title="Altersvorsorgedepot Förderung 2027 — Zulage, Steuer, Bedingungen",
    meta_desc="Alle Förderdetails zum Altersvorsorgedepot 2027: Grundzulage 540 €, Kinderzulage 300 €, Steuerbonus, Mindestbeitrag, wer förderberechtigt ist.",
    og_desc="Altersvorsorgedepot 2027: Grundzulage 540 €/Jahr, Kinderzulage 300 €, Steuerbonus bis 2.100 €. Alle Förderdetails und Bedingungen.",
    eyebrow="Förderung · Zulage · Steuerbonus · 2027",
    h1="Altersvorsorgedepot Förderung 2027",
    lead="Das neue Altersvorsorgedepot bringt eine deutlich verbesserte Förderung gegenüber Riester: 540 € Grundzulage, 300 € Kinderzulage, Steuerbonus auf Einzahlungen. Hier sind alle Förderdetails auf einen Blick.",
    calc_id="depot",
    calc_label="AV-Depot-Rechner",
    cta_title="Persönliche Förderung berechnen",
    cta_desc="Mit dem AV-Depot-Rechner siehst du, wie viel Förderung du erhältst und wie sich das auf deine Altersvorsorge auswirkt.",
    kpi_items=[("540 €", "Grundzulage/Jahr"), ("300 €", "Kinderzulage/Kind"), ("2.100 €", "Max. Steuerbonus/Jahr")],
    content_html="""<h2>Übersicht: Alle Förderarten im AV-Depot</h2>
    <table class="data-table">
      <thead><tr><th>Förderart</th><th>Betrag</th><th>Bedingung</th></tr></thead>
      <tbody>
        <tr><td>Grundzulage</td><td>540 €/Jahr</td><td>4 % Mindestbeitrag vom Vorjahreseinkommen</td></tr>
        <tr><td>Kinderzulage</td><td>300 €/Jahr pro Kind</td><td>Kind unter 25, Kindergeldberechtigung</td></tr>
        <tr><td>Steuerbonus</td><td>bis ~2.100 €/Jahr absetzbar</td><td>Sonderausgabenabzug, Günstigerprinzip</td></tr>
        <tr><td>Junger-Einsteiger-Bonus</td><td>Geplant (Details offen)</td><td>Ersteinzahlung unter 25 Jahren</td></tr>
      </tbody>
    </table>
    <h2>Mindestbeitrag: Was muss ich einzahlen?</h2>
    <p>Wie bei Riester ist ein Mindestbeitrag von 4 % des rentenversicherungspflichtigen Vorjahreseinkommens erforderlich, um die volle Grundzulage zu erhalten. Bei 50.000 € Brutto = 2.000 €/Jahr (167 €/Monat). Wer weniger einzahlt, erhält die Zulage anteilig.</p>
    <p>Mindesteigenleistung: 60 €/Jahr (1,2 % des gesetzlichen Sockels). Wer also kaum Einkommen hat, kann trotzdem Zulage bekommen.</p>
    <h2>Günstigerprinzip: Zulage oder Steuerbonus?</h2>
    <p>Der Staat gewährt automatisch das Günstigere: Wenn dein Steuerbonus (Grenzsteuersatz × Beitrag) höher ist als die Grundzulage, erhältst du den Steuerbonus. Liegt die Zulage höher, wird die Zulage gewährt. Das läuft automatisch über die Steuererklärung.</p>
    <p><strong>Beispiel</strong>: 42 % Grenzsteuer, 2.100 € eingezahlt → Steuerbonus 882 €. Das übersteigt die Grundzulage 540 €, also wird der Steuerbonus gewährt. Bei 25 % Grenzsteuer: 525 € Steuerbonus < 540 € Zulage → Zulage wird gewährt.</p>
    <h2>Auszahlungsphase: Nachgelagerte Besteuerung</h2>
    <p>Die staatliche Förderung ist an die nachgelagerte Besteuerung geknüpft: Einzahlungen und Gewinne werden erst bei Auszahlung versteuert. Da das Renteneinkommen meist niedriger ist als das Erwerbseinkommen, entsteht in der Regel ein echter Steuervorteil.</p>
    <h2>Wer ist förderberechtigt?</h2>
    <p>Geplant: alle gesetzlich Rentenversicherten, Beamte, Richter, Soldaten und weitere Gruppen gemäß EStG. Neu gegenüber Riester: auch Selbständige ohne GRV-Pflichtversicherung sollen einbezogen werden.</p>""",
    faq_pairs=[
        ("Wie hoch ist die Grundzulage beim Altersvorsorgedepot 2027?", "540 € pro Jahr. Das ist mehr als dreimal so viel wie die bisherige Riester-Grundzulage (175 €/Jahr)."),
        ("Wie viel Kinderzulage gibt es beim Altersvorsorgedepot?", "300 € pro Kind und Jahr, solange das Kind unter 25 ist und Kindergeldberechtigung besteht. Bei 2 Kindern: 600 €/Jahr zusätzlich."),
        ("Muss ich 4 % einzahlen, um die volle Förderung zu erhalten?", "Ja — bei 50.000 € Brutto sind das 2.000 €/Jahr. Wer weniger einzahlt, bekommt die Zulage anteilig. Mindesteigenleistung: 60 €/Jahr."),
        ("Was ist das Günstigerprinzip beim Altersvorsorgedepot?", "Der Staat vergleicht automatisch deinen Steuerbonus mit der Grundzulage und gewährt den höheren Betrag. Bei hohem Grenzsteuersatz lohnt sich der Steuerbonus mehr."),
    ]
))

# 5. Rentenlücke 2026
articles.append(dict(
    slug="rentenluecke-2026",
    title="Rentenlücke 2026 — So groß ist deine Versorgungslücke wirklich",
    meta_desc="Die Rentenlücke 2026: Warum die gesetzliche Rente nicht reicht, wie groß die Lücke wirklich ist und wie du sie berechnest und schließt.",
    og_desc="Rentenlücke 2026: Durchschnittliche GRV-Rente ca. 1.500 € netto. Lebenshaltungskosten ca. 2.025 €/Monat. Was fehlt und was dagegen hilft.",
    eyebrow="Rentenlücke · Altersarmut · 2026",
    h1="Rentenlücke 2026",
    lead="Die durchschnittliche Nettorente in Deutschland lag 2025 bei ca. 1.450–1.600 €. Die durchschnittlichen Lebenshaltungskosten eines Rentner-Haushalts liegen deutlich darüber. Die Lücke ist real — und wächst.",
    calc_id="rente",
    calc_label="Rentenrechner",
    cta_title="Eigene Rentenlücke berechnen",
    cta_desc="Mit dem Rentenrechner siehst du in 60 Sekunden, wie groß deine persönliche Rentenlücke ist — mit realen Zahlen aus deiner Rentenauskunft.",
    kpi_items=[("1.543 €", "Ø Nettorente 2025"), ("2.025 €", "Ø Lebenshaltung"), ("–482 €", "Ø Monatliche Lücke")],
    content_html="""<h2>Was ist die Rentenlücke?</h2>
    <p>Die Rentenlücke (oder Versorgungslücke) ist die Differenz zwischen deinem gewünschten Nettoeinkommen im Ruhestand und dem, was die gesetzliche Rentenversicherung tatsächlich auszahlt. Die meisten Menschen unterschätzen diese Lücke erheblich — weil sie entweder die Bruttorente mit der Nettorente verwechseln oder die Inflation nicht einrechnen.</p>
    <h2>Wie groß ist die Rentenlücke 2026 im Durchschnitt?</h2>
    <p>Nach Daten der Deutschen Rentenversicherung 2025:</p>
    <table class="data-table">
      <thead><tr><th>Kennzahl</th><th>Männer</th><th>Frauen</th><th>Gesamt</th></tr></thead>
      <tbody>
        <tr><td>Ø Bruttorente/Monat</td><td>1.751 €</td><td>1.316 €</td><td>~1.540 €</td></tr>
        <tr><td>Ø Nettorente (nach Steuer/KV)</td><td>~1.630 €</td><td>~1.190 €</td><td>~1.430 €</td></tr>
        <tr><td>Ø Lebenshaltung (Destatis 2025)</td><td colspan="2">~2.025 €/Monat (2-Pers.-HH)</td><td>~2.025 €</td></tr>
        <tr><td>Lücke (netto)</td><td>–395 €</td><td>–835 €</td><td>~–600 €</td></tr>
      </tbody>
    </table>
    <h2>Warum ist die Lücke bei Frauen größer?</h2>
    <p>Frauen haben im Schnitt niedrigere Renten durch: Teilzeit-Arbeit (häufiger als Männer), Elternzeit-Unterbrechungen, Pflege von Angehörigen und historisch niedrigere Löhne. Das führt zu weniger Rentenpunkten und damit zu einer strukturell größeren Versorgungslücke.</p>
    <h2>Wie entwickelt sich die Lücke bis 2050?</h2>
    <p>Der Rentenniveaupfad zeigt: Das Sicherungsniveau vor Steuern sinkt von aktuell ~48 % auf voraussichtlich ~45–46 % bis 2035. Gleichzeitig steigen Lebenshaltungskosten mit der Inflation. Wer heute 40 ist und erst bei Renteneintritt handelt, hat zu wenig Zeit für den Zinseszinseffekt.</p>
    <h2>Wie schließt man die Rentenlücke?</h2>
    <ul>
      <li><strong>Früh anfangen</strong>: 25 €/Monat ab 30 = ca. 45.000 € bei 65 (7 % p. a.)</li>
      <li><strong>ETF-Depot aufbauen</strong>: Kostengünstig, flexibel, ab 2027 förderfähig</li>
      <li><strong>Rürup für Gutverdiener</strong>: Steuerbonus bis 42 % auf Einzahlungen bis 27.565 €/Jahr</li>
      <li><strong>Erwerbsminderungsrente absichern</strong>: Berufsunfähigkeit ist das größte Altersarmutsrisiko vor der Rente</li>
    </ul>""",
    faq_pairs=[
        ("Wie groß ist die durchschnittliche Rentenlücke 2026?", "Im Schnitt ca. 400–800 €/Monat, je nach Geschlecht, Einkommen und Erwerbsbiografie. Frauen sind durch Teilzeit und Elternzeit besonders betroffen."),
        ("Wie berechnet man die eigene Rentenlücke?", "Rentenwunsch (netto) minus erwartete GRV-Nettorente (aus Rentenauskunft, nach Abzug von Steuer und KV-Beitrag) = Rentenlücke. Mit dem Pensora-Rentenrechner in 60 Sekunden automatisch berechnet."),
        ("Was sind die Lebenshaltungskosten im Rentenalter?", "Nach Destatis 2025 für einen 2-Personen-Rentnerhaushalt ca. 2.025 €/Monat: Warmmiete 960 €, Lebensmittel 440 €, Transport 210 €, Energie 160 €, Gesundheit 110 €, weitere 145 €."),
        ("Wie schließt man die Rentenlücke am effizientesten?", "Früh anfangen (Zinseszins), ETF-Depot aufbauen (ab 2027 AV-Depot), Rürup bei hohem Steuersatz, Berufsunfähigkeitsversicherung als Basisschutz."),
    ]
))

# 6. gesetzliche Rente reicht nicht
articles.append(dict(
    slug="gesetzliche-rente-reicht-nicht",
    title="Gesetzliche Rente reicht nicht — Was du jetzt tun musst",
    meta_desc="Warum die gesetzliche Rente nicht zum Leben reicht, was das Versorgungsniveau wirklich bedeutet und welche 3 Maßnahmen jetzt sinnvoll sind.",
    og_desc="GRV reicht nicht: Rentenniveau ~48 %, Nettorente oft unter 1.600 €. Warum das so ist und was du konkret dagegen tun kannst.",
    eyebrow="GRV · Altersvorsorge · Handlungsbedarf",
    h1="Gesetzliche Rente reicht nicht",
    lead="Das Rentenniveau in Deutschland liegt bei ~48 % — vor Steuern, auf den Durchschnittslohn. Was das für dich bedeutet: Die meisten Menschen werden mit der GRV-Rente allein nicht den gewohnten Lebensstandard halten können.",
    calc_id="rente",
    calc_label="Rentenrechner",
    cta_title="Wie viel Rente bekommst du wirklich?",
    cta_desc="Mit dem Rentenrechner berechnest du deine voraussichtliche Nettorente, die echte Kaufkraft nach Inflation und deine Versorgungslücke.",
    kpi_items=[("~48 %", "Rentenniveau 2025"), ("–2,5 %", "Kaufkraftverlust p. a."), ("15+ J.", "Ø Rentenbezugsdauer")],
    content_html="""<h2>Was bedeutet „Rentenniveau 48 %"?</h2>
    <p>Das Sicherungsniveau vor Steuern von ~48 % bedeutet: Ein Durchschnittsverdiener, der 45 Jahre lang gearbeitet hat, bekommt eine Rente von ca. 48 % seines letzten Durchschnittslohns — vor Steuern und Sozialabgaben. Netto landet weniger an.</p>
    <p>Wer nicht genau 45 Jahre eingezahlt hat (Elternzeit, Studium, Teilzeit, Selbständigkeit), bekommt noch deutlich weniger. Das Rentenniveau gilt nur für den Idealtypus.</p>
    <h2>Warum sinkt das Rentenniveau weiter?</h2>
    <p>Drei strukturelle Ursachen:</p>
    <ul>
      <li><strong>Demografischer Wandel</strong>: Weniger Beitragszahler finanzieren mehr Rentner — das Verhältnis verschlechtert sich bis 2040 drastisch</li>
      <li><strong>Nachhaltigkeitsfaktor</strong>: Gesetzlicher Mechanismus, der das Rentenniveau bei ungünstigem Demografieverhältnis automatisch dämpft</li>
      <li><strong>Haltelinie nur bis 2025 gesetzlich gesichert</strong>: Das 48 %-Niveau war eine politische Zusicherung bis 2025. Was danach gilt, ist politisch offen</li>
    </ul>
    <h2>Was reicht die Rente wirklich?</h2>
    <p>Rechenbeispiel für einen Arbeitnehmer, 45 Jahre lang 45.000 € Brutto pro Jahr:</p>
    <ul>
      <li>Erwartete Bruttorente: ~1.350 €/Monat</li>
      <li>Abzüge (KV + PV + Steuern): ca. –150 bis –250 €</li>
      <li>Nettorente: ~1.100–1.200 €/Monat</li>
      <li>Kaufkraft real (nach 30 Jahren Inflation à 2,5 %): entspricht heute ~580–640 €</li>
    </ul>
    <p>Fazit: Wer heute 35 ist und nur auf die GRV setzt, wird mit realer Kaufkraft von ~600 €/Monat in Rente gehen.</p>
    <h2>Die drei wichtigsten Maßnahmen</h2>
    <ul>
      <li><strong>1. Rentenlücke jetzt berechnen</strong>: Rentenauskunft beantragen (DRV), reale Nettorente berechnen, Lücke beziffern</li>
      <li><strong>2. ETF-Depot aufbauen</strong>: Frühzeitig, kostengünstig, ab 2027 als AV-Depot förderfähig</li>
      <li><strong>3. Erwerbsminderungsschutz</strong>: Berufsunfähigkeitsversicherung als häufig vergessene Säule — Invalidität ist das größte Risiko für Altersarmut</li>
    </ul>""",
    faq_pairs=[
        ("Reicht die gesetzliche Rente zum Leben?", "Für die meisten Menschen nicht allein. Die Durchschnittsnettorente 2025 liegt bei ~1.430 €, die Lebenshaltungskosten bei ~2.025 €/Monat. Die Lücke ist real."),
        ("Was ist das Rentenniveau und was bedeutet es?", "Das Rentenniveau (Sicherungsniveau vor Steuern) zeigt, wie viel Prozent des Durchschnittslohns die Rente eines Durchschnittsverdieners nach 45 Jahren entspricht. 2025: ~48 %."),
        ("Warum sinkt das Rentenniveau?", "Demografischer Wandel (weniger Beitragszahler, mehr Rentner), Nachhaltigkeitsfaktor und politisch nicht dauerhaft gesicherte Haltelinie."),
        ("Was kann ich gegen eine zu geringe Rente tun?", "Rentenlücke berechnen (Pensora-Rechner), ETF-Depot aufbauen, Rürup bei hohem Steuersatz nutzen, Berufsunfähigkeitsversicherung abschließen."),
    ]
))

# 7. Rente mit 63 Lehrer
articles.append(dict(
    slug="rente-mit-63-lehrer",
    title="Rente mit 63 für Lehrer — Was Verbeamtete wissen müssen",
    meta_desc="Können Lehrer mit 63 in den Ruhestand? Abzüge bei Frühpensionierung, Dienstunfähigkeit als Alternative und was netto übrigbleibt.",
    og_desc="Rente mit 63 für Lehrer: Frühpensionierung, Abzüge von 3,6 %/Jahr, Dienstunfähigkeit und was am Ende wirklich netto bleibt.",
    eyebrow="Lehrer · Frühpensionierung · Versorgung",
    h1="Rente mit 63 für Lehrer",
    lead="Lehrer sind verbeamtet und gehen nicht in die Rente, sondern in die Pension. Frühpensionierung mit 63 ist möglich — aber mit dauerhaften Abzügen. Was bleibt netto übrig, und wann lohnt es sich wirklich?",
    calc_id="pension",
    calc_label="Pensionsrechner",
    cta_title="Pensionshöhe mit 63 berechnen",
    cta_desc="Mit dem Pensionsrechner siehst du genau, wie hoch deine Pension bei Eintritt mit 63, 64 oder 65 ist — und wie groß die Abzüge sind.",
    kpi_items=[("3,6 %", "Abzug pro Frühpensionsjahr"), ("10,8 %", "Abzug bei 3 Jahren früher"), ("71,75 %", "Max. Ruhegehaltssatz")],
    content_html="""<h2>Können verbeamtete Lehrer mit 63 in Rente?</h2>
    <p>Lehrer sind Beamte und haben kein Rentenkonto bei der gesetzlichen Rentenversicherung. Sie können nicht die „Rente mit 63" (für Arbeitnehmer mit 45 Beitragsjahren) beantragen. Was es gibt: die <strong>Antragsversetzung in den Ruhestand</strong> ab dem 62. oder 63. Lebensjahr (je nach Bundesland) — mit dauerhaften Versorgungsabzügen.</p>
    <h2>Wann kann ein Beamten-Lehrer früher in Pension?</h2>
    <ul>
      <li><strong>Antragsruhestand</strong>: In den meisten Bundesländern ab 62 oder 63 Jahren auf Antrag möglich</li>
      <li><strong>Schwerbehinderung</strong>: Ab GdB 50 frühere Pensionierung ohne volle Abzüge möglich</li>
      <li><strong>Dienstunfähigkeit</strong>: Bei gesundheitlicher Einschränkung Pensionierung ohne Mindestalter — aber mit Abzügen</li>
      <li><strong>Langjährige Beamte</strong>: In manchen Bundesländern Sonderregelungen nach 40+ Dienstjahren</li>
    </ul>
    <h2>Wie hoch sind die Abzüge bei Frühpensionierung?</h2>
    <p>Pro Jahr vor dem Regelruhestandsalter (65 oder 67, je nach Bundesland): <strong>3,6 % dauerhafter Abzug</strong> vom Ruhegehalt. Maximum: 10,8 % (nach 3 Jahren). Dieser Abzug gilt lebenslang und erhöht sich nicht mehr zurück.</p>
    <table class="data-table">
      <thead><tr><th>Pensionseintritt</th><th>Jahre früher</th><th>Abzug</th><th>Restpension bei 71,75 %</th></tr></thead>
      <tbody>
        <tr><td>Regelruhestand (67)</td><td>0</td><td>0 %</td><td>71,75 % des Grundgehalts</td></tr>
        <tr><td>Mit 65</td><td>2</td><td>–7,2 %</td><td>~64,5 % des Grundgehalts</td></tr>
        <tr><td>Mit 64</td><td>3</td><td>–10,8 %</td><td>~60,9 % des Grundgehalts</td></tr>
        <tr><td>Mit 63</td><td>4</td><td>–10,8 % (gedeckelt)</td><td>~60,9 % des Grundgehalts</td></tr>
      </tbody>
    </table>
    <h2>Was bleibt netto bei Frühpensionierung mit 63?</h2>
    <p>Beispiel A13-Lehrer (Stufe 8, ~5.100 € brutto): Maximalversorgung 71,75 % = ~3.660 € brutto Pension. Mit 10,8 % Abzug: ~3.263 € brutto. Abzüge: PKV-Beitrag (~350–500 €), Pflegeversicherung, Steuern. Netto: ca. 2.400–2.700 €.</p>
    <h2>Lohnt es sich, früher in Pension zu gehen?</h2>
    <p>Die Faustregel: Pro Jahr früher verlierst du nicht nur ein Pensionsjahr (weniger Einzahlungsjahre), sondern auch 3,6 % dauerhaft. Wer mit 63 statt 67 in Pension geht: 4 Jahre weniger Gehalt UND ~10,8 % weniger Pension für den Rest des Lebens. Das rechnet sich oft nur bei schlechter Gesundheit oder wenn das Familieneinkommen ohnehin ausreicht.</p>""",
    faq_pairs=[
        ("Können Lehrer mit 63 in Rente?", "Lehrer sind verbeamtet und gehen in die Pension, nicht in die Rente. Antragsruhestand ab 62 oder 63 ist möglich — aber mit dauerhaftem Abzug von bis zu 10,8 %."),
        ("Wie hoch ist der Abzug bei Frühpensionierung für Lehrer?", "3,6 % pro Jahr vor dem Regelruhestandsalter, maximal 10,8 %. Der Abzug gilt lebenslang."),
        ("Was ist der Unterschied zwischen Rente mit 63 und Beamtenpension mit 63?", "Rente mit 63 ist eine GRV-Regelung für Arbeitnehmer mit 45 Beitragsjahren. Beamte haben kein GRV-Konto — für sie gibt es nur den Antragsruhestand mit Versorgungsabzügen."),
        ("Wann lohnt sich Frühpensionierung für Lehrer?", "Finanziell selten — der lebenslange Abzug von 10,8 % ist erheblich. Empfehlenswert bei schwerwiegender Gesundheitseinschränkung, Schwerbehinderung oder wenn das Haushaltseinkommen ohnehin gesichert ist."),
    ]
))

# 8. Aktivrente 2026
articles.append(dict(
    slug="aktivrente-2026",
    title="Aktivrente 2026 — bis 2.000 € steuerfrei im Ruhestand dazuverdienen",
    meta_desc="Aktivrente 2026: Rentner können bis zu 2.000 € monatlich steuerfrei dazuverdienen. Wer profitiert, was die Bedingungen sind und ab wann die Regelung gilt.",
    og_desc="Aktivrente 2026: 2.000 €/Monat steuerfrei für arbeitende Rentner. Koalitionsvertrag 2025, geplanter Start, Bedingungen und steuerliche Auswirkungen.",
    eyebrow="Aktivrente · Nebenerwerb · Steuerfreiheit 2026",
    h1="Aktivrente 2026",
    lead="Der Koalitionsvertrag 2025 sieht vor, dass Rentner bis zu 2.000 € monatlich steuerfrei dazuverdienen können. Die Aktivrente soll Arbeit im Rentenalter attraktiver machen und dem Fachkräftemangel entgegenwirken.",
    calc_id="rente",
    calc_label="Rentenrechner",
    cta_title="Rente + Nebenerwerb planen",
    cta_desc="Mit dem Rentenrechner berechnest du deine voraussichtliche GRV-Rente und kannst prüfen, ob und wie viel Aktivrente deine Lücke schließt.",
    kpi_items=[("2.000 €", "Steuerfrei/Monat"), ("24.000 €", "Steuerfrei/Jahr"), ("2026", "Geplanter Start")],
    content_html="""<h2>Was ist die Aktivrente?</h2>
    <p>Die Aktivrente ist eine neue steuerliche Regelung aus dem Koalitionsvertrag der Bundesregierung 2025 (CDU/CSU + SPD). Rentner, die weiterarbeiten oder einer Nebentätigkeit nachgehen, sollen bis zu <strong>2.000 € pro Monat (24.000 €/Jahr) steuerfrei</strong> verdienen dürfen — zusätzlich zu ihrer Rente.</p>
    <p>Ziel ist doppelt: Erstens soll Arbeit im Rentenalter steuerlich attraktiver werden. Zweitens soll dem Fachkräftemangel entgegengewirkt werden, indem erfahrene Arbeitskräfte länger dem Arbeitsmarkt zur Verfügung stehen.</p>
    <h2>Was sind die Bedingungen?</h2>
    <ul>
      <li><strong>Rentenempfänger</strong>: Nur für Personen, die bereits GRV-Rente beziehen</li>
      <li><strong>Einkommensgrenze</strong>: Bis 2.000 €/Monat Bruttoeinnahmen aus Erwerbstätigkeit steuerfrei</li>
      <li><strong>Art der Tätigkeit</strong>: Selbständigkeit, Anstellung, Minijob — Details noch offen</li>
      <li><strong>Kombination mit Rente</strong>: Die Rente selbst bleibt nachgelagert steuerpflichtig — nur der Hinzuverdienst wird freigestellt</li>
    </ul>
    <h2>Was ändert sich gegenüber der bisherigen Regelung?</h2>
    <p>Bisher gilt: Rentner können unbegrenzt hinzuverdienen (seit 2023 keine Hinzuverdienstgrenze mehr). Aber: Der Hinzuverdienst wird normal besteuert und erhöht zusammen mit der Rente das zu versteuernde Einkommen.</p>
    <p>Mit der Aktivrente-Regelung wird ein Freibetrag von 2.000 €/Monat eingeführt — der Hinzuverdienst bis 2.000 € bleibt komplett steuerfrei. Das ergibt effektiv eine Steuerersparnis von ca. 400–840 €/Monat (je nach Grenzsteuersatz 20–42 %).</p>
    <h2>Für wen ist die Aktivrente besonders attraktiv?</h2>
    <ul>
      <li>Selbständige und Freiberufler, die nach Rentenbeginn weiter tätig sein wollen</li>
      <li>Handwerker, Ärzte, Ingenieure mit gefragten Spezialkompetenzen</li>
      <li>Lehrer und Beamte im Ruhestand (ggf. über Honorartätigkeiten)</li>
      <li>Wer eine kleine Rente hat und die Lücke durch Arbeit schließen will</li>
    </ul>
    <h2>Ab wann gilt die Aktivrente?</h2>
    <p>Geplant: 2026. Das Gesetzgebungsverfahren läuft. Aktuelle Informationen werden nach Verabschiedung des Gesetzes aktualisiert.</p>""",
    faq_pairs=[
        ("Was ist die Aktivrente 2026?", "Eine neue steuerliche Regelung, nach der Rentner bis zu 2.000 €/Monat aus Erwerbstätigkeit steuerfrei dazuverdienen können. Geplanter Start: 2026."),
        ("Wer profitiert von der Aktivrente?", "Alle GRV-Rentner, die weiterarbeiten oder einer Nebentätigkeit nachgehen — besonders attraktiv für Selbständige, Freiberufler und Rentner mit kleiner Rente."),
        ("Wie viel Steuern spart man mit der Aktivrente?", "Bei 2.000 €/Monat Hinzuverdienst und 35 % Grenzsteuersatz: ~700 €/Monat Steuerersparnis. Bei 42 %: ~840 €/Monat."),
        ("Gilt die Aktivrente auch für Beamte im Ruhestand?", "Details noch offen. Grundsätzlich gilt sie für GRV-Rentner. Für Beamte im Ruhestand (Pension) kann eine analoge Regelung kommen — aktuell noch nicht beschlossen."),
    ]
))

# 9. Mütterrente 2027
articles.append(dict(
    slug="muetterrente-2027",
    title="Mütterrente 2027 — Was sich ändert und wer mehr bekommt",
    meta_desc="Mütterrente 2027: Geplante Verbesserungen bei der Anrechnung von Kindererziehungszeiten. Wer profitiert und wie viel mehr Rente entsteht.",
    og_desc="Mütterrente 2027: Kindererziehungszeiten, Entgeltpunkte, geplante Verbesserungen. Wie viel mehr Rente bekommen Mütter ab 2027?",
    eyebrow="Mütterrente · Kindererziehungszeit · GRV",
    h1="Mütterrente 2027",
    lead="Die Mütterrente ist die Anerkennung von Kindererziehungszeiten in der gesetzlichen Rentenversicherung. 2024 gab es Verbesserungen für Kinder vor 1992 — ab 2027 stehen weitere Reformen im Raum. Was sich ändert und wer profitiert.",
    calc_id="rente",
    calc_label="Rentenrechner",
    cta_title="Eigene Rente mit Kindererziehungszeiten berechnen",
    cta_desc="Mit dem Rentenrechner siehst du, wie sich Kindererziehungszeiten auf deine Rente auswirken und wie groß deine Versorgungslücke bleibt.",
    kpi_items=[("3 EP", "Pro Kind ab 1992"), ("2,5 EP", "Pro Kind vor 1992"), ("~37 €/Monat", "Wert pro Entgeltpunkt 2025")],
    content_html="""<h2>Was ist die Mütterrente?</h2>
    <p>Die Mütterrente bezeichnet die Anrechnung von Kindererziehungszeiten als Beitragszeiten in der gesetzlichen Rentenversicherung. Für jedes Kind, das ab 1992 geboren wurde, werden 3 Jahre Kindererziehungszeit angerechnet (= 3 Entgeltpunkte). Für Kinder, die vor 1992 geboren wurden, wurden ursprünglich nur 2 Punkte angerechnet — durch die Mütterrente I (2014) und Mütterrente II (2019) wurden die Punkte schrittweise auf 2,5 erhöht.</p>
    <h2>Wie viel Rente bringt ein Entgeltpunkt?</h2>
    <p>Ein Entgeltpunkt entspricht 2025 einem aktuellen Rentenwert von ca. 37,60 €/Monat. Drei Entgeltpunkte (= 3 Jahre Kindererziehung ab 1992) bringen ca. <strong>112 €/Monat mehr Rente</strong>. Für 2 Kinder: ~224 €/Monat.</p>
    <table class="data-table">
      <thead><tr><th>Kinder</th><th>Geburtsjahr</th><th>Entgeltpunkte</th><th>Mehr Rente/Monat (2025)</th></tr></thead>
      <tbody>
        <tr><td>1 Kind</td><td>ab 1992</td><td>3,0 EP</td><td>~+112 €</td></tr>
        <tr><td>1 Kind</td><td>vor 1992</td><td>2,5 EP</td><td>~+94 €</td></tr>
        <tr><td>2 Kinder</td><td>ab 1992</td><td>6,0 EP</td><td>~+225 €</td></tr>
        <tr><td>3 Kinder</td><td>ab 1992</td><td>9,0 EP</td><td>~+338 €</td></tr>
      </tbody>
    </table>
    <h2>Was ist für 2027 geplant?</h2>
    <p>Im Koalitionsvertrag 2025 sind weitere Verbesserungen für Geringverdienende mit Kindererziehungszeiten geplant. Die genaue Ausgestaltung ist noch offen. Diskutiert wird:</p>
    <ul>
      <li>Gleichstellung von Kindern vor 1992 auf 3 Entgeltpunkte (wie nach 1992)</li>
      <li>Verlängerung der anrechenbaren Kindererziehungszeit von 3 auf bis zu 4 Jahre</li>
      <li>Verbesserung bei Mehrfachkindern (z. B. Überlappungszeiten)</li>
    </ul>
    <h2>Wer profitiert am meisten?</h2>
    <p>Frauen mit Kindern, die vor 1992 geboren wurden, profitieren am stärksten von einer möglichen Gleichstellung auf 3 Entgeltpunkte — sie bekämen dann ~18 €/Monat mehr Rente pro Kind. Für Frauen mit 3+ älteren Kindern summiert sich das auf ~55 €/Monat.</p>""",
    faq_pairs=[
        ("Was ist die Mütterrente und wie viel bringt sie?", "Kindererziehungszeiten werden als Rentenpunkte angerechnet: 3 Punkte pro Kind ab 1992, 2,5 Punkte für Kinder vor 1992. Ein Punkt = ~37,60 €/Monat Rente."),
        ("Was ändert sich bei der Mütterrente 2027?", "Geplant sind Verbesserungen bei der Gleichstellung von Kindern vor 1992 auf 3 Entgeltpunkte. Details noch offen — Gesetz nicht beschlossen."),
        ("Bekommen Väter auch Mütterrente?", "Ja — auch Väter, die Kindererziehungszeiten nachweisen können, erhalten Entgeltpunkte. Die Bezeichnung 'Mütterrente' ist historisch bedingt."),
        ("Wie wirkt sich die Mütterrente auf meine Rentenlücke aus?", "Bei 2 Kindern (ab 1992) ca. +225 €/Monat Rente. Das reduziert die Versorgungslücke erheblich — vor allem für Frauen mit Teilzeit-Biografie."),
    ]
))

# 10. Versorgungslücke Beamte berechnen
articles.append(dict(
    slug="versorgungsluecke-beamte-berechnen",
    title="Versorgungslücke Beamte berechnen — So geht's richtig",
    meta_desc="Wie Beamte ihre Versorgungslücke korrekt berechnen: Ruhegehaltssatz, PKV-Abzug, Inflation, Beihilfe. Mit konkreten Beispielrechnungen.",
    og_desc="Versorgungslücke Beamte: Ruhegehaltssatz korrekt berechnen, PKV-Kosten im Ruhestand einbeziehen, Inflation berücksichtigen. Schritt für Schritt.",
    eyebrow="Beamte · Versorgungslücke · Berechnung",
    h1="Versorgungslücke Beamte berechnen",
    lead="Die Versorgungslücke ist die Differenz zwischen Versorgungswunsch und tatsächlicher Nettopension. Viele Beamte unterschätzen sie, weil sie PKV-Kosten, Inflation und Teilzeit-Abzüge nicht korrekt einrechnen.",
    calc_id="pension",
    calc_label="Pensionsrechner",
    cta_title="Versorgungslücke jetzt berechnen",
    cta_desc="Der Pensionsrechner berechnet deinen individuellen Ruhegehaltssatz, PKV-Kosten und die echte Versorgungslücke nach Inflation.",
    kpi_items=[("71,75 %", "Max. Ruhegehaltssatz"), ("2 % p. a.", "Steigerung"), ("40 J.", "Vollversorgung")],
    content_html="""<h2>Schritt 1: Ruhegehaltssatz berechnen</h2>
    <p>Der Ruhegehaltssatz bestimmt, wie viel Prozent des letzten Grundgehalts du als Pension bekommst. Er steigt mit jedem Dienstjahr um 1,79375 % (bei Verbeamtung ab 2. Lebenshalbjahr 2005 nach BBG). Mindestversorgung: 35 %, Maximum: 71,75 %.</p>
    <p><strong>Formel</strong>: Ruhegehaltsfähige Dienstjahre × 1,79375 % = Ruhegehaltssatz (max. 71,75 %)</p>
    <p><strong>Beispiel A13, Eintritt mit 28, Pension mit 67</strong>: 39 Dienstjahre × 1,79375 % = 69,96 %. Bruttopension: 69,96 % × 5.100 € = 3.568 €/Monat.</p>
    <h2>Schritt 2: Was mindert den Ruhegehaltssatz?</h2>
    <ul>
      <li><strong>Elternzeit</strong>: Bis zu 3 Jahre anrechenbar, aber nicht vollständig als Dienstzeit</li>
      <li><strong>Teilzeit</strong>: Teilzeitjahre werden anteilig berechnet (50 % Teilzeit = 0,5 Dienstjahre)</li>
      <li><strong>Frühpensionierung</strong>: 3,6 % Abzug pro Jahr vor Regelruhestandsalter (max. 10,8 %)</li>
      <li><strong>Auszeiten</strong>: Beurlaubungen, Sonderurlaube ohne Dienstbezüge</li>
    </ul>
    <h2>Schritt 3: PKV-Kosten im Ruhestand einrechnen</h2>
    <p>Im Ruhestand zahlen Beamte ihren PKV-Beitrag komplett selbst (abzüglich Beihilfe). Bei einem 60-jährigen PKV-Versicherten (Beihilfesatz 70 %): PKV-Beitrag ca. 350–500 €/Monat, Beihilfe deckt 70 % der Kosten ab. Eigenanteil: 30 % = ~100–150 €/Monat. Aber: PKV-Beiträge steigen im Alter.</p>
    <p>Achtung: Im Alter 80+ können PKV-Beiträge (vor Beihilfe) auf 800–1.200 €/Monat steigen. Bei 70 % Beihilfe: ~240–360 €/Eigenanteil. Das muss einkalkuliert werden.</p>
    <h2>Schritt 4: Inflation berücksichtigen</h2>
    <p>Pensionen werden an die allgemeine Besoldungsentwicklung angepasst — aber meist mit Verzögerung und unterhalb der Inflation. Bei 2 % jährlicher Inflation verliert die Pension in 20 Jahren ca. 33 % ihrer Kaufkraft. Reale Versorgungslücke = nominale Lücke × Inflationseffekt.</p>
    <h2>Rechenbeispiel: Vollständige Versorgungslücke A13</h2>
    <ul>
      <li>Bruttopension: 3.568 €</li>
      <li>Abzüge: Kirchensteuer (–100 €), Einkommensteuer (–320 €), PKV-Eigenanteil (–130 €)</li>
      <li>Nettopension: ~3.018 €</li>
      <li>Versorgungsziel: 3.500 € netto</li>
      <li><strong>Lücke: –482 €/Monat</strong></li>
    </ul>""",
    faq_pairs=[
        ("Wie berechnet man den Ruhegehaltssatz für Beamte?", "Ruhegehaltsfähige Dienstjahre × 1,79375 % = Ruhegehaltssatz, maximal 71,75 %. Teilzeit und Frühpensionierung mindern den Satz."),
        ("Was ist die typische Versorgungslücke bei Beamten?", "Typisch: 300–600 €/Monat nach Abzug von PKV, Steuern und unter Berücksichtigung des Versorgungsziels. Bei Teilzeit-Biografie oder früher Pension auch deutlich mehr."),
        ("Wie hoch ist der PKV-Eigenanteil im Beamtenruhestand?", "Bei 70 % Beihilfe und ca. 500 €/Monat PKV-Beitrag: ~150 €/Monat Eigenanteil. Im hohen Alter (80+) kann der Gesamtbeitrag steigen."),
        ("Wie beeinflusst Elternzeit den Ruhegehaltssatz?", "Elternzeit mindert die ruhegehaltsfähige Dienstzeit — bis zu 3 Jahre werden angerechnet, aber die genaue Behandlung variiert nach Bundesland und Zeitpunkt."),
    ]
))

# 11. Pensionslücke Lehrer
articles.append(dict(
    slug="pensionsluecke-lehrer",
    title="Pensionslücke Lehrer — Wie groß ist sie wirklich?",
    meta_desc="Pensionslücke bei Lehrern: Teilzeit, Elternzeit, PKV-Kosten, Frühpensionierung. Wie groß ist die Lücke wirklich und was lässt sich dagegen tun?",
    og_desc="Pensionslücke Lehrer 2026: Ruhegehaltssatz, Teilzeit-Abzüge, PKV-Eigenanteil, Versorgungswunsch vs. Realität. Mit Beispielrechnungen.",
    eyebrow="Lehrer · Pension · Versorgungslücke",
    h1="Pensionslücke Lehrer",
    lead="Lehrer gelten als gut versorgt — aber die Realität ist differenzierter. Teilzeit, Elternzeit und PKV-Kosten im Alter können eine echte Versorgungslücke hinterlassen, die ohne private Vorsorge nicht zu schließen ist.",
    calc_id="pension",
    calc_label="Pensionsrechner",
    cta_title="Persönliche Pensionslücke berechnen",
    cta_desc="Mit dem Pensionsrechner siehst du in 60 Sekunden, wie groß deine Pensionslücke als Lehrer wirklich ist — mit Teilzeit und Elternzeit.",
    kpi_items=[("–1,79 %", "Je Teilzeitjahr (50 %)"), ("3,6 %", "Abzug je Frühpensionsjahr"), ("70 %", "Beihilfesatz (typisch)")]    ,
    content_html="""<h2>Warum haben Lehrer eine Pensionslücke?</h2>
    <p>Lehrer sind in Deutschland in der Regel verbeamtet und haben Anspruch auf eine Beamtenpension. Theoretisch können sie bis zu 71,75 % ihres letzten Grundgehalts als lebenslange Pension erhalten. Praktisch ergibt sich eine Lücke aus mehreren Faktoren:</p>
    <ul>
      <li><strong>Teilzeit für Kinderbetreuung</strong>: Besonders häufig bei Lehrerinnen — jedes Teilzeitjahr reduziert den Ruhegehaltssatz dauerhaft</li>
      <li><strong>Elternzeit</strong>: Bis zu 3 Jahre pro Kind werden bei der Dienstzeit eingeschränkt berücksichtigt</li>
      <li><strong>Frühpensionierung</strong>: Wer früher geht, zahlt 3,6 % pro Jahr drauf</li>
      <li><strong>PKV-Kostensteigerung</strong>: Im Alter steigen die Beiträge — bei manchen Lehrern auf 600–800 €/Monat vor Beihilfe</li>
    </ul>
    <h2>Rechenbeispiel: Lehrerin A13, 5 Jahre Teilzeit (50 %)</h2>
    <p>Eintritt mit 28, Pension mit 67. Normalfall (keine Teilzeit): 39 × 1,79375 % = 69,96 % → 3.568 €/Monat brutto.</p>
    <p>Mit 5 Jahren 50 % Teilzeit: Statt 5 vollen Jahren nur 2,5 anrechenbare Jahre → effektiv 36,5 Dienstjahre → 65,47 % → 3.339 €/Monat brutto. Differenz: –229 €/Monat brutto = lebenslang.</p>
    <p>Netto nach Abzügen (Steuer, PKV-Eigenanteil ~150 €): ca. 2.600–2.700 €. Bei Versorgungswunsch 3.200 €: <strong>Lücke ~500 €/Monat</strong>.</p>
    <h2>Was hilft gegen die Pensionslücke?</h2>
    <ul>
      <li><strong>Rürup-Rente</strong>: Steuerbonus bis 42 % auf Einzahlungen bis 27.565 €/Jahr. Für Lehrer ab A13 mit hohem Grenzsteuersatz sehr attraktiv</li>
      <li><strong>AV-Depot</strong>: Ab 2027 staatlich gefördert, flexibel, kostengünstig über ETFs</li>
      <li><strong>Dienstunfähigkeitsversicherung</strong>: Absicherung bei gesundheitlichem Ausfall — für Lehrer eines der größten Risiken</li>
    </ul>""",
    faq_pairs=[
        ("Wie groß ist die typische Pensionslücke bei Lehrern?", "Typisch 300–600 €/Monat netto, besonders bei Teilzeit-Biografie oder Elternzeit. Mit PKV-Kostensteigerung im Alter kann es mehr werden."),
        ("Wie wirkt sich Teilzeit auf die Pension aus?", "Jedes Teilzeitjahr (50 %) zählt nur als 0,5 Dienstjahre. 5 Jahre 50 % Teilzeit = –2,5 Dienstjahre = ca. –4,5 % Ruhegehaltssatz dauerhaft."),
        ("Was hilft Lehrern gegen die Pensionslücke?", "Rürup (hoher Steuerbonus), AV-Depot ab 2027, Dienstunfähigkeitsversicherung. Früh anfangen — der Zinseszinseffekt ist entscheidend."),
        ("Haben Lehrer eine PKV-Lücke im Ruhestand?", "Ja. PKV-Beiträge steigen mit dem Alter. Bei 70 % Beihilfe bleibt ein wachsender Eigenanteil — im hohen Alter kann das 200–350 €/Monat ausmachen."),
    ]
))

# 12. Pension Lehrer wie viel Prozent
articles.append(dict(
    slug="pension-lehrer-prozent",
    title="Pension Lehrer: Wie viel Prozent bekommt man wirklich?",
    meta_desc="Wie viel Prozent Pension bekommen Lehrer? Ruhegehaltssatz, Dienstjahre, Grundgehalt — mit konkreten Beispielrechnungen für A12, A13, A14.",
    og_desc="Lehrerpension in Prozent: Ruhegehaltssatz 1,79375 % pro Jahr, max. 71,75 %. Konkrete Beispiele für A12, A13, A14 nach 35, 40 und 45 Jahren.",
    eyebrow="Lehrer · Pension · Prozent · Berechnung",
    h1="Pension Lehrer: Wie viel Prozent?",
    lead="Die Lehrerpension wird nach einem festen Satz berechnet: 1,79375 % des letzten Grundgehalts pro anrechenbarem Dienstjahr, maximal 71,75 %. Hier sind konkrete Zahlen für Lehrer in verschiedenen Besoldungsgruppen.",
    calc_id="pension",
    calc_label="Pensionsrechner",
    cta_title="Eigene Pension berechnen",
    cta_desc="Mit dem Pensionsrechner siehst du in 60 Sekunden, wie viel Prozent Pension du bekommst — mit deiner genauen Besoldungsgruppe und Dienstzeit.",
    kpi_items=[("1,79375 %", "Je Dienstjahr"), ("71,75 %", "Maximum"), ("40 J.", "Vollversorgung (ca.)")],
    content_html="""<h2>Wie berechnet sich der Ruhegehaltssatz?</h2>
    <p>Grundformel: <strong>Ruhegehaltsfähige Dienstjahre × 1,79375 % = Ruhegehaltssatz</strong> (maximal 71,75 %).</p>
    <p>Ruhegehaltsfähige Dienstjahre sind alle anrechenbaren Zeiten: aktive Dienstzeit, Ausbildungszeiten (Studium, Referendariat), Kindererziehungszeiten (begrenzt), Wehrdienstzeiten. Teilzeit-Phasen werden anteilig berechnet.</p>
    <h2>Tabelle: Pension in Prozent nach Dienstjahren</h2>
    <table class="data-table">
      <thead><tr><th>Dienstjahre</th><th>Ruhegehaltssatz</th><th>Bruttopension A13 Stufe 8 (5.100 €)</th></tr></thead>
      <tbody>
        <tr><td>35 Jahre</td><td>62,78 %</td><td>~3.202 €</td></tr>
        <tr><td>38 Jahre</td><td>68,16 %</td><td>~3.476 €</td></tr>
        <tr><td>40 Jahre (max. ~)</td><td>71,75 %</td><td>~3.659 €</td></tr>
        <tr><td>45 Jahre</td><td>71,75 % (gedeckelt)</td><td>~3.659 €</td></tr>
      </tbody>
    </table>
    <h2>Konkrete Beispiele nach Besoldungsgruppe (40 Dienstjahre)</h2>
    <table class="data-table">
      <thead><tr><th>Besoldung</th><th>Grundgehalt (Stufe 8)</th><th>Ruhegehaltssatz</th><th>Bruttopension</th></tr></thead>
      <tbody>
        <tr><td>A12</td><td>~4.600 €</td><td>71,75 %</td><td>~3.301 €</td></tr>
        <tr><td>A13</td><td>~5.100 €</td><td>71,75 %</td><td>~3.659 €</td></tr>
        <tr><td>A14</td><td>~5.600 €</td><td>71,75 %</td><td>~4.018 €</td></tr>
        <tr><td>A15</td><td>~6.200 €</td><td>71,75 %</td><td>~4.449 €</td></tr>
      </tbody>
    </table>
    <h2>Was wird von der Bruttopension abgezogen?</h2>
    <ul>
      <li><strong>Einkommensteuer</strong>: Pensionen sind vollständig steuerpflichtig. Bei 3.500 € brutto ca. 400–500 €/Monat Steuer</li>
      <li><strong>PKV-Eigenanteil</strong>: Bei 70 % Beihilfe ca. 100–200 €/Monat</li>
      <li><strong>Pflegeversicherung</strong>: Pensionäre zahlen eigenständig (ca. 50–80 €/Monat)</li>
    </ul>
    <p>Nettopension bei A13, 40 Dienstjahre: ca. <strong>2.800–3.000 €</strong> — je nach Steuerklasse und PKV-Eigenanteil.</p>
    <h2>Was mindert den Ruhegehaltssatz?</h2>
    <p>Teilzeit (anteilige Anrechnung), Frühpensionierung (–3,6 %/Jahr), längere Beurlaubungen. Wer 5 Jahre zu 50 % Teilzeit gearbeitet hat, verliert ~4–5 % Ruhegehaltssatz dauerhaft.</p>""",
    faq_pairs=[
        ("Wie viel Prozent Pension bekommen Lehrer?", "1,79375 % pro anrechenbarem Dienstjahr, maximal 71,75 %. Bei 40 Dienstjahren: ~71,75 % des letzten Grundgehalts als Bruttopension."),
        ("Wie viel Pension bekommt ein A13-Lehrer netto?", "Bei 40 Dienstjahren und Stufe 8: ~3.659 € brutto → netto nach Steuern und PKV-Eigenanteil ca. 2.800–3.000 €/Monat."),
        ("Ab wie vielen Dienstjahren ist die Maximalpension erreicht?", "Bei 71,75 % Maximum: 71,75 ÷ 1,79375 = ~40 Dienstjahre. Mehr Dienstjahre erhöhen die Pension nicht."),
        ("Was passiert mit der Pension bei Teilzeit?", "Teilzeit-Jahre werden anteilig angerechnet. 5 Jahre bei 50 % = 2,5 Dienstjahre. Das reduziert den Ruhegehaltssatz dauerhaft um ca. 4,5 %."),
    ]
))

# 13. Beamtenversorgung Teilzeit Elternzeit
articles.append(dict(
    slug="beamtenversorgung-teilzeit-elternzeit",
    title="Beamtenversorgung bei Teilzeit und Elternzeit — Was du verlierst",
    meta_desc="Wie sich Teilzeit und Elternzeit auf die Beamtenpension auswirken: Ruhegehaltssatz-Verluste, Rechenbeispiele und wie man die Lücke schließt.",
    og_desc="Beamtenversorgung Teilzeit Elternzeit: Wie viel Pension verliert man durch Teilzeit und Elternzeit? Mit konkreten Zahlen und Gegenmaßnahmen.",
    eyebrow="Beamte · Teilzeit · Elternzeit · Versorgung",
    h1="Beamtenversorgung bei Teilzeit und Elternzeit",
    lead="Elternzeit und Teilzeit sind für viele Beamte unausweichlich — aber sie kosten dauerhaft Pension. Hier sind die genauen Zahlen und was man dagegen tun kann.",
    calc_id="pension",
    calc_label="Pensionsrechner",
    cta_title="Pension mit Teilzeit berechnen",
    cta_desc="Mit dem Pensionsrechner siehst du exakt, wie viel Pension du durch Teilzeit oder Elternzeit verlierst — und wie du die Lücke schließt.",
    kpi_items=[("0,5 J.", "Wert: 1 Teilzeitjahr (50 %)"), ("1,79 %", "Verlust pro vollem Dienstjahr"), ("3 J.", "Max. Elternzeit-Anrechnung")],
    content_html="""<h2>Wie wird Teilzeit bei der Beamtenpension behandelt?</h2>
    <p>Teilzeit-Jahre werden anteilig als Dienstzeit angerechnet. Wer 1 Jahr bei 50 % Teilzeit arbeitet, erhält nur 0,5 anrechenbare Dienstjahre. Das reduziert den Ruhegehaltssatz um 0,5 × 1,79375 % = <strong>0,897 % dauerhaft</strong>.</p>
    <p>Bei 5 Jahren 50 % Teilzeit: –4,48 % Ruhegehaltssatz. Bei A13-Grundgehalt 5.100 €: –228 €/Monat brutto Pension für den Rest des Lebens.</p>
    <h2>Tabelle: Pensionsverlust durch Teilzeit</h2>
    <table class="data-table">
      <thead><tr><th>Teilzeitjahre (50 %)</th><th>Verlorene Dienstjahre</th><th>Ruhegehaltssatz-Verlust</th><th>Brutto-Verlust A13</th></tr></thead>
      <tbody>
        <tr><td>2 Jahre</td><td>–1 Jahr</td><td>–1,79 %</td><td>~–91 €/Monat</td></tr>
        <tr><td>4 Jahre</td><td>–2 Jahre</td><td>–3,59 %</td><td>~–183 €/Monat</td></tr>
        <tr><td>6 Jahre</td><td>–3 Jahre</td><td>–5,38 %</td><td>~–274 €/Monat</td></tr>
        <tr><td>10 Jahre</td><td>–5 Jahre</td><td>–8,97 %</td><td>~–457 €/Monat</td></tr>
      </tbody>
    </table>
    <h2>Wie wird Elternzeit bei der Beamtenpension behandelt?</h2>
    <p>Elternzeit ist grundsätzlich nicht automatisch als Dienstzeit anrechenbar — aber es gibt Ausnahmen:</p>
    <ul>
      <li><strong>Kindererziehungszeiten</strong>: Bis zu 3 Jahre pro Kind werden berücksichtigt (aber nicht als volle Dienstzeit)</li>
      <li><strong>Kinder vor 1992</strong>: Nur eingeschränkte Anerkennung (1 Jahr statt 3 Jahre)</li>
      <li><strong>Teilweise Anrechnung</strong>: Je nach Landesrecht und Zeitpunkt der Elternzeit unterschiedlich</li>
    </ul>
    <h2>Kann man die Verluste ausgleichen?</h2>
    <p>Durch private Vorsorge — ja. Die Faustformel: Pro 100 €/Monat dauerhafter Pensionsverlust braucht man ein Kapital von ca. 30.000 € bei Renteneintritt (bei 3–4 % Entnahmerate). Das aufzubauen ist mit ETF-Depot oder Rürup gut möglich, wenn man früh genug beginnt.</p>
    <p><strong>Beispiel</strong>: 5 Jahre 50 % Teilzeit = –228 €/Monat Pensionsverlust. Ausgleich: ca. 68.000 € Kapital bei Pensionseintritt → bei 7 % p. a. und 20 Jahren Ansparzeit: ca. 135 €/Monat Sparrate ausreichend.</p>""",
    faq_pairs=[
        ("Wie viel Pension verliert man durch Teilzeit?", "1 Jahr bei 50 % Teilzeit = –0,897 % Ruhegehaltssatz dauerhaft. Bei A13: –46 €/Monat brutto Pension pro Teilzeitjahr. Über 5 Jahre Teilzeit: –228 €/Monat."),
        ("Wie wird Elternzeit bei der Beamtenpension angerechnet?", "Bis zu 3 Jahre Kindererziehungszeit werden berücksichtigt, aber nicht als volle Dienstzeit. Details variieren nach Bundesland und Zeitpunkt."),
        ("Kann man den Teilzeit-Pensionsverlust ausgleichen?", "Ja — durch private Vorsorge (ETF-Depot, Rürup). Faustformel: Pro 100 €/Monat Pensionsverlust ca. 30.000 € Kapital bei Pensionseintritt."),
        ("Lohnt sich Teilzeit trotz Pensionsverlust?", "Das ist eine individuelle Entscheidung. Wichtig: Den Pensionsverlust früh quantifizieren und durch private Vorsorge ausgleichen, statt im Ruhestand böse überrascht zu werden."),
    ]
))

# 14. Private Altersvorsorge Beamte sinnvoll
articles.append(dict(
    slug="private-altersvorsorge-beamte",
    title="Private Altersvorsorge für Beamte — Wann ist sie sinnvoll?",
    meta_desc="Brauchen Beamte private Altersvorsorge? Wann Rürup, AV-Depot oder ETF-Depot für Beamte sinnvoll sind — mit Steuervorteil-Rechnung.",
    og_desc="Private Altersvorsorge Beamte: Rürup vs. ETF-Depot vs. AV-Depot 2027. Wann lohnt sich private Vorsorge trotz guter Pension?",
    eyebrow="Beamte · Private Altersvorsorge · Rürup · ETF",
    h1="Private Altersvorsorge für Beamte",
    lead="Beamte haben eine gute Basisversorgung — aber nicht immer eine lückenlose. Private Altersvorsorge lohnt sich für Beamte besonders dann, wenn Teilzeit, Elternzeit oder früher Pensionseintritt Lücken hinterlassen.",
    calc_id="pension",
    calc_label="Pensionsrechner",
    cta_title="Versorgungslücke berechnen",
    cta_desc="Mit dem Pensionsrechner siehst du, ob und wie groß deine Lücke ist — Basis für eine fundierte Entscheidung zur privaten Vorsorge.",
    kpi_items=[("71,75 %", "Max. Ruhegehaltssatz"), ("42 %", "Max. Grenzsteuersatz Rürup"), ("7 % p. a.", "Hist. ETF-Rendite")],
    content_html="""<h2>Brauchen Beamte private Altersvorsorge?</h2>
    <p>Nicht automatisch — aber in vielen Fällen ja. Die Beamtenpension ist eine solide Grundlage, aber sie ist nicht immer ausreichend:</p>
    <ul>
      <li>Teilzeit- oder Elternzeit-Phasen reduzieren den Ruhegehaltssatz dauerhaft</li>
      <li>Früher Pensionseintritt kostet 3,6 % pro Jahr</li>
      <li>PKV-Kosten steigen im Alter erheblich</li>
      <li>Inflation nagt an der Kaufkraft der Pension</li>
    </ul>
    <p>Wer keine dieser Abzüge hat und bis 67 arbeitet, kommt mit der Pension oft gut aus. Alle anderen haben häufig eine echte Lücke.</p>
    <h2>Option 1: Rürup-Rente für Beamte</h2>
    <p>Rürup ist für Beamte mit hohem Grenzsteuersatz (35–42 %) besonders attraktiv. Bis zu 27.565 € pro Jahr absetzbar (2025), das ergibt bis zu 11.577 € Steuerersparnis jährlich.</p>
    <p><strong>Wann Rürup sinnvoll</strong>: Grenzsteuersatz ≥ 35 %, Versorgungslücke > 300 €/Monat, Eintritt nicht zu kurz vor Pension. Nachteil: Kapital kann nicht entnommen werden, lebenslange Verrentung.</p>
    <h2>Option 2: Altersvorsorgedepot (ab 2027)</h2>
    <p>Das neue AV-Depot 2027 kombiniert ETF-Flexibilität mit staatlicher Förderung (Grundzulage 540 €, Kinderzulage 300 €). Für Beamte mit mittlerem Grenzsteuersatz (25–35 %) oft attraktiver als Rürup, weil das Kapital nicht verrentet werden muss und flexibler bleibt.</p>
    <h2>Option 3: Reguläres ETF-Depot</h2>
    <p>Ohne staatliche Förderung, aber maximale Flexibilität: kein Renteneintrittsalter, keine Auszahlungsregeln, vererb- und übertragbar. Empfehlenswert als Ergänzung zu Rürup/AV-Depot oder für Beamte, die mehr Freiheit wollen als die staatlich geförderten Produkte bieten.</p>
    <h2>Vergleich: Welche Vorsorge lohnt sich wann?</h2>
    <table class="data-table">
      <thead><tr><th>Produkt</th><th>Steuervorteil</th><th>Flexibilität</th><th>Empfohlen bei</th></tr></thead>
      <tbody>
        <tr><td>Rürup</td><td>Sehr hoch (42 % GrSt)</td><td>Gering (Verrentung)</td><td>Grenzsteuersatz ≥ 35 %</td></tr>
        <tr><td>AV-Depot 2027</td><td>Mittel (Zulage + Bonus)</td><td>Mittel (30 % Kapital)</td><td>Grenzsteuersatz 25–35 %</td></tr>
        <tr><td>ETF-Depot</td><td>Gering (nur Vorabpauschale)</td><td>Sehr hoch</td><td>Ergänzung, Flexibilitätswunsch</td></tr>
      </tbody>
    </table>""",
    faq_pairs=[
        ("Brauchen Beamte private Altersvorsorge?", "Nicht zwingend — aber bei Teilzeit, Elternzeit, Frühpensionierung oder hohem PKV-Eigenanteil im Alter entsteht oft eine echte Lücke, die private Vorsorge sinnvoll macht."),
        ("Lohnt sich Rürup für Beamte?", "Ja, ab Grenzsteuersatz 35 %. Bis zu 27.565 €/Jahr absetzbar, ergibt bis zu 11.577 € Steuerersparnis. Nachteil: Kapital ist bis zur Rente gebunden."),
        ("Was ist besser für Beamte: Rürup oder AV-Depot?", "Bei Grenzsteuersatz ≥ 35 %: Rürup. Bei niedrigerem Steuersatz oder Flexibilitätswunsch: AV-Depot 2027 oder ETF-Depot. Kombination möglich."),
        ("Können Beamte ETF-Depot als Altersvorsorge nutzen?", "Ja — ohne staatliche Förderung, aber maximale Flexibilität. Ab 2027 kann ein reguläres ETF-Depot als Altersvorsorgedepot zertifiziert und dann gefördert werden."),
    ]
))

# ─── Generate all pages ─────────────────────────────────────────────────────

print(f"Generating {len(articles)} SEO articles in {BASE}/")
for a in articles:
    page(**a)
print("Done.")
