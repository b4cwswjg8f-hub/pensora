export const BRAND_NAME = 'Thrive Abroad';

export const BOOK_URL = 'https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach';

export const CARDS = [
  { id: 'depot',        num: '01', badge: 'ETF Investing',       title: 'ETF Savings Plan Calculator', desc: 'Compound-interest growth, real return after inflation, the 4% withdrawal rule, and the savings rate you need to hit your goal.' },
  { id: 'rente',        num: '02', badge: 'State Pension',       title: 'German Pension Calculator',   desc: 'Your statutory German pension under § 64 SGB VI — earnings points, pension value, and the taxable share on payout.' },
  { id: 'ruerup',       num: '03', badge: 'Tax Optimization',    title: 'Rürup Pension Calculator',    desc: 'The tax advantage of a Rürup basic pension under § 10 EStG — fully deductible in 2025. Net cost and projected payout.' },
  { id: 'cashflow',     num: '04', badge: 'Financial Planning',  title: 'Cashflow Calculator',         desc: 'Analyze your monthly cashflow: actual spend vs. the 50/15/15 rule, emergency-fund sizing, and your savings rate.' },
  { id: 'versicherung', num: '05', badge: 'Market Comparison',   title: 'Insurance Check',             desc: 'Your insurance costs vs. the 2025 GDV market average. Spot over- and under-insurance in eight categories.' },
];

export const RATGEBER = [
  { href: 'etf-investing-expats-germany/',    label: 'ETF Investing for Expats' },
  { href: 'buying-property-germany-expat/',   label: 'Buying Property as an Expat' },
  { href: 'inheritance-tax-germany-expats/',  label: 'Inheritance Tax in Germany' },
  { href: 'investing-for-kids-germany/',      label: 'Investing for Your Kids' },
  { href: 'tax-residency-germany-expats/',    label: 'German Tax Residency' },
  { href: 'rsu-stock-options-tax-germany/',   label: 'RSUs & Stock Options' },
  { href: 'us-citizens-investing-germany-pfic/', label: 'US Citizens: Avoiding PFIC' },
];

export const VERGLEICHE = [
  { href: 'financial-planning-expats-germany/', label: 'Holistic Financial Planning' },
];

export const TOPICS = [
  {
    id: 'pension',
    calc: 'rente',
    accent: 'green',
    icon: 'pension',
    eyebrow: 'State Pension · § 64 SGB VI',
    title: 'How the German State Pension Actually Works',
    paragraphs: [
      'Germany’s statutory pension isn’t based on what you paid in — it’s based on “earnings points” (Entgeltpunkte). Roughly speaking, a year at the average German salary earns you one point; a full career at that level nets around 45 points by retirement.',
      'Each point has a fixed euro value at payout — about €39.32 in 2024. Change employer, go part-time, move abroad and come back: none of it resets your points, they simply keep accumulating for as long as you contribute.',
      'For internationals, totalization agreements between Germany and dozens of countries let years worked abroad count toward the minimum vesting period — but the pension amount itself is still paid out purely on German points earned.',
    ],
    fact: { value: '€39.32', label: 'value of 1 pension point (2024, West Germany)' },
    calcLabel: 'Calculate My German Pension',
  },
  {
    id: 'etf',
    calc: 'depot',
    accent: 'teal',
    icon: 'etf',
    eyebrow: 'Wealth Accumulation · ETF Sparplan',
    title: 'Building Wealth With ETFs While Living Abroad',
    paragraphs: [
      'German bank interest rarely beats inflation, and the state pension alone won’t fund an early or comfortable retirement — which is why most long-term wealth here is built through low-cost, broad ETF savings plans, not individual stock picking.',
      'A globally diversified index like the MSCI World has returned roughly 7–8% a year on average over recent decades, before inflation. Automated monthly investing smooths out volatility and lets compounding turn a modest income into real capital over 15–20 years.',
      'Two things trip up expats specifically: the “Vorabpauschale” (an advance tax on unrealized ETF gains, charged even if you never sell), and — for US citizens — the PFIC rules that turn most European-domiciled ETFs into a tax trap.',
    ],
    fact: { value: '≈ 7–8%', label: 'avg. annual return, MSCI World, before inflation' },
    calcLabel: 'Run My ETF Savings Plan',
  },
  {
    id: 'tax',
    calc: 'ruerup',
    accent: 'amber',
    icon: 'tax',
    eyebrow: 'Income Tax · § 10 EStG',
    title: 'Germany’s Tax System, Simply Explained',
    paragraphs: [
      'German income tax is progressive: it starts around 14% just above the tax-free allowance and climbs to 42% for higher incomes, then 45% for very high earners. Most employees also pay an 8–9% church tax if registered with a religion, plus a small solidarity surcharge above a high threshold.',
      'Your tax class (Steuerklasse I–VI) only controls how much is withheld from your paycheck each month — not what you actually owe. Married couples can combine classes III/V or both take IV; either way, the real number gets settled in your annual tax return.',
      'One of the few ways to legally shrink your taxable income is the Rürup pension (Basisrente): in 2025, contributions are fully deductible — turning a high-earning year into meaningful, locked-in retirement capital.',
    ],
    fact: { value: '100%', label: 'of Rürup contributions are tax-deductible in 2025' },
    calcLabel: 'See My Rürup Tax Saving',
  },
  {
    id: 'cashflow',
    calc: 'cashflow',
    accent: 'rose',
    icon: 'cashflow',
    eyebrow: 'Financial Planning · Savings Rate',
    title: 'The 50/15/15 Rule for Your Household Budget',
    paragraphs: [
      'Once you know your net income, the real question is where it goes. A simple benchmark planners use: 50% for fixed living costs, 15% toward retirement, 15% toward other goals — leaving roughly 20% as a buffer for irregular spending.',
      'Expats often carry costs locals never budget for — obligations back home, currency transfers, higher insurance in the first years — so an honest monthly cashflow view matters more here than the rule of thumb alone.',
      'Building a 3–6 month emergency fund in easily accessible savings, before investing aggressively, is the step most people skip — and the one they regret when a visa renewal, deposit, or flight home comes up unplanned.',
    ],
    fact: { value: '50/15/15/20', label: 'costs / retirement / goals / buffer' },
    calcLabel: 'Analyze My Cashflow',
  },
  {
    id: 'insurance',
    calc: 'versicherung',
    accent: 'azure',
    icon: 'insurance',
    eyebrow: 'Insurance · GDV Benchmark',
    title: 'Which Insurance You Actually Need in Germany',
    paragraphs: [
      'Germany is one of the most heavily insured countries in the world, but not every policy sold to newcomers is necessary. Health insurance is mandatory by law; personal liability insurance (Haftpflicht) is a near-universal must at roughly €60 a year.',
      'Occupational disability insurance (Berufsunfähigkeitsversicherung) is the one most advisors call essential and most expats skip — state disability protection is minimal, especially in your first years of contributions.',
      'Comparing your actual premiums against the GDV’s published market averages across eight categories is the fastest way to spot where you’re overpaying, or dangerously underinsured.',
    ],
    fact: { value: '≈ €60/yr', label: 'typical cost of German liability insurance' },
    calcLabel: 'Check My Insurance',
  },
];

export const PERSONAS = [
  { id: 'newcomer',     icon: '🧳', title: 'Newcomer',                 sub: 'Just relocated to Germany',        hint: 'New job, new tax system, new rules',         calcs: ['rente', 'cashflow', 'versicherung'] },
  { id: 'employed',     icon: '💼', title: 'Employed',                 sub: 'On a German payroll',              hint: 'Subject to German social insurance',         calcs: ['rente', 'depot', 'ruerup', 'cashflow'] },
  { id: 'selfemployed', icon: '⚡',  title: 'Self-Employed / Freelance', sub: 'Rürup · Depot · Insurance',        hint: 'Freelancer, founder, contractor',            calcs: ['ruerup', 'depot', 'cashflow', 'versicherung'] },
  { id: 'family',       icon: '👨‍👩‍👧', title: 'Building Wealth for Kids', sub: 'Investing · Rürup · Budget',       hint: 'Planning for your family\'s future',         calcs: ['depot', 'ruerup', 'cashflow'] },
];
