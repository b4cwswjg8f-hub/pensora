export const BOOK_URL = 'https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach';

export const CARDS = [
  { id: 'pension',      num: '01', badge: 'Beamte',              title: 'Pensionsrechner',    desc: 'Nettopension nach § 14 BeamtVG — Ruhegehaltssatz, Mindestversorgung, Steuer und KV-Beihilfe.',                        tags: ['§ 14 BeamtVG', '17 Bundesländer', 'PKV/GKV'] },
  { id: 'rente',        num: '02', badge: 'Angestellte',          title: 'Rentenrechner',      desc: 'Gesetzliche Rente nach § 64 SGB VI. Entgeltpunkte, Rentenwert 2025 · 40,79 €, Besteuerungsanteil.',                    tags: ['§ 64 SGB VI', 'Rentenwert 40,79 €', 'Rentenlücke'] },
  { id: 'depot',        num: '03', badge: 'ETF · Altersvorsorge', title: 'AV-Depot-Rechner',  desc: 'Zinseszins-Depot, reale Rendite nach Inflation, 4 %-Entnahmerate und Sparrate zum Ziel.',                               tags: ['Zinseszins', '4 %-Regel', 'Realrendite'] },
  { id: 'ruerup',       num: '04', badge: 'Steueroptimierung',    title: 'Rürup-Rechner',      desc: 'Steuervorteil der Basisrente nach § 10 EStG. 100 % absetzbar 2025. Netto-Kosten & Rentenprognose.',                    tags: ['§ 10 EStG', '100 % absetzbar', 'ETF-Rürup'] },
  { id: 'cashflow',     num: '05', badge: 'Finanzplanung',        title: 'Cashflow-Rechner',   desc: 'Monatlichen Cashflow analysieren: Ist vs. 50/15/15-Empfehlung, Notgroschen und AV-Sparquote.',                         tags: ['50/15/15-Regel', 'Notgroschen', 'Sparquote'] },
  { id: 'versicherung', num: '06', badge: 'Marktvergleich',       title: 'Versicherungscheck', desc: 'Deine Versicherungskosten vs. GDV-Marktdurchschnitt 2025. Über- und Unterversicherung.',                               tags: ['GDV-Daten 2025', '8 Kategorien', 'Einsparpotenzial'] },
];

export const RATGEBER = [
  { href: 'lehrerpension-nrw/',                       label: 'Lehrerpension NRW' },
  { href: 'lehrerpension-bw/',                        label: 'Lehrerpension BW' },
  { href: 'lehrerpension-bayern/',                    label: 'Lehrerpension Bayern' },
  { href: 'a13-gehalt-pension/',                      label: 'Pension A13' },
  { href: 'teilzeit-pension-lehrer/',                 label: 'Teilzeit & Pension' },
  { href: 'referendariat-pension/',                   label: 'Referendariat' },
  { href: 'altersvorsorgedepot-2027/',                label: 'AV-Depot 2027' },
  { href: 'ruerup-lehrer/',                           label: 'Rürup für Lehrer' },
  { href: 'pkv-beamte-ruhestand/',                    label: 'PKV im Ruhestand' },
  { href: 'riester-nachfolger/',                      label: 'Riester Nachfolger' },
  { href: 'fruehstartrente-kinder/',                  label: 'Frühstartrente Kinder' },
  { href: 'altersvorsorgedepot-beamte/',              label: 'AV-Depot Beamte' },
  { href: 'altersvorsorgedepot-foerderung/',          label: 'AV-Depot Förderung' },
  { href: 'rentenluecke-2026/',                       label: 'Rentenlücke 2026' },
  { href: 'gesetzliche-rente-reicht-nicht/',          label: 'GRV reicht nicht' },
  { href: 'rente-mit-63-lehrer/',                     label: 'Rente mit 63 Lehrer' },
  { href: 'aktivrente-2026/',                         label: 'Aktivrente 2026' },
  { href: 'muetterrente-2027/',                       label: 'Mütterrente 2027' },
  { href: 'versorgungsluecke-beamte-berechnen/',      label: 'Versorgungslücke Beamte' },
  { href: 'pensionsluecke-lehrer/',                   label: 'Pensionslücke Lehrer' },
  { href: 'pension-lehrer-prozent/',                  label: 'Pension Lehrer Prozent' },
  { href: 'beamtenversorgung-teilzeit-elternzeit/',   label: 'Teilzeit Elternzeit Pension' },
  { href: 'private-altersvorsorge-beamte/',           label: 'Private AV Beamte' },
];

export const VERGLEICHE = [
  { href: 'pension-vs-rente/',              label: 'Pension vs. Rente' },
  { href: 'pension-vs-rente-lehrer/',       label: 'Pension vs. Rente Lehrer' },
  { href: 'ruerup-vs-altersvorsorgedepot/', label: 'Rürup vs. AV-Depot' },
  { href: 'pkv-vs-gkv-beamte-ruhestand/',  label: 'PKV vs. GKV Beamte' },
  { href: 'teilzeit-vs-vollzeit-pension/',  label: 'Teilzeit vs. Vollzeit' },
];

export const UPDATES = [
  { label: 'Rente ab 63 — wird die Frührente gestoppt?', sub: 'Aktuelle Debatte · Stand Juni 2026',       href: 'fruehrente-63/',                  dot: true  },
  { label: 'AV-Depot im Bundestag beschlossen',       sub: 'Grundzulage 540 €/Jahr · ab 01.01.2027',     href: 'altersvorsorgedepot-2027/',       dot: true  },
  { label: 'Rentenwert 2026 steigt auf 42,52 €',      sub: 'DRV · ab 1. Juli 2026 · +4,25 %',            href: 'rentenluecke-2026/',              dot: true  },
  { label: 'Rürup-Höchstbetrag 2026',                 sub: '30.826 € absetzbar · § 10 EStG',             href: 'ruerup-lehrer/',                  dot: false },
  { label: 'Aktivrente 2026 — unbegrenzt dazuverdienen', sub: 'Ab 65: kein Hinzuverdienstdeckel mehr',   href: 'aktivrente-2026/',                dot: false },
  { label: 'Mütterrente 2027 — aktueller Stand',      sub: 'Geplante Erweiterung im Überblick',          href: 'muetterrente-2027/',              dot: false },
  { label: 'AV-Depot Förderung — Details',            sub: 'Wer profitiert, wie viel, ab wann',          href: 'altersvorsorgedepot-foerderung/', dot: false },
];

export const STATS = [
  { val: '71,75 %',   label: 'Max. Ruhegehaltssatz', sub: '§ 14 BeamtVG · 40 Dienstjahre' },
  { val: '40,79 €',   label: 'Rentenwert 2025',       sub: 'DRV · pro Entgeltpunkt · ab Juli' },
  { val: '938 €/Mo.', label: 'Ø Versorgungslücke',    sub: 'Lehrkräfte · inflationsbereinigt' },
  { val: '540 €',     label: 'AV-Depot Grundzulage',  sub: 'ab 01.01.2027 · pro Jahr' },
];

export const PERSONAS = [
  { id: 'beamter',       icon: '🏛',  title: 'Beamter/in',      sub: 'Pension · PKV · Beihilfe',           hint: 'Lehrkraft, Richter, Polizei, Verwaltung',       calcs: ['pension', 'depot', 'ruerup', 'versicherung'] },
  { id: 'angestellter',  icon: '💼',  title: 'Angestellte/r',   sub: 'Gesetzliche Rente · Depot · Budget', hint: 'Sozialversicherungspflichtig beschäftigt',       calcs: ['rente', 'depot', 'ruerup', 'cashflow'] },
  { id: 'selbstaendiger',icon: '⚡',  title: 'Selbständige/r',  sub: 'Rürup · Depot · Versicherungen',     hint: 'Freiberufler, Unternehmer, Freelancer',          calcs: ['ruerup', 'depot', 'cashflow', 'versicherung'] },
  { id: 'vorrente',      icon: '🌅',  title: 'Kurz vor Rente',  sub: 'Versorgung · Entnahme · Cashflow',   hint: 'Weniger als 5 Jahre bis zum Ruhestand',          calcs: ['pension', 'rente', 'depot', 'cashflow'] },
];
