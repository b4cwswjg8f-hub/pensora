export const BRAND_NAME = 'Thrive Abroad';

export const BOOK_URL = 'https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach';

export const CARDS = [
  { id: 'depot',        num: '01', badge: 'ETF Investing',       title: 'ETF Savings Plan Calculator', desc: 'Compound-interest growth, real return after inflation, the 4% withdrawal rule, and the savings rate you need to hit your goal.', tags: ['Compound Interest', '4% Rule', 'Real Return'] },
  { id: 'rente',        num: '02', badge: 'State Pension',       title: 'German Pension Calculator',   desc: 'Your statutory German pension under § 64 SGB VI — earnings points, pension value, and the taxable share on payout.',              tags: ['§ 64 SGB VI', 'Pension Value', 'Pension Gap'] },
  { id: 'ruerup',       num: '03', badge: 'Tax Optimization',    title: 'Rürup Pension Calculator',    desc: 'The tax advantage of a Rürup basic pension under § 10 EStG — fully deductible in 2025. Net cost and projected payout.',          tags: ['§ 10 EStG', 'Fully Deductible', 'ETF-Rürup'] },
  { id: 'cashflow',     num: '04', badge: 'Financial Planning',  title: 'Cashflow Calculator',         desc: 'Analyze your monthly cashflow: actual spend vs. the 50/15/15 rule, emergency-fund sizing, and your savings rate.',                tags: ['50/15/15 Rule', 'Emergency Fund', 'Savings Rate'] },
  { id: 'versicherung', num: '05', badge: 'Market Comparison',   title: 'Insurance Check',             desc: 'Your insurance costs vs. the 2025 GDV market average. Spot over- and under-insurance in eight categories.',                      tags: ['2025 GDV Data', '8 Categories', 'Savings Potential'] },
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

export const PERSONAS = [
  { id: 'newcomer',     icon: '🧳', title: 'Newcomer',                 sub: 'Just relocated to Germany',        hint: 'New job, new tax system, new rules',         calcs: ['rente', 'cashflow', 'versicherung'] },
  { id: 'employed',     icon: '💼', title: 'Employed',                 sub: 'On a German payroll',              hint: 'Subject to German social insurance',         calcs: ['rente', 'depot', 'ruerup', 'cashflow'] },
  { id: 'selfemployed', icon: '⚡',  title: 'Self-Employed / Freelance', sub: 'Rürup · Depot · Insurance',        hint: 'Freelancer, founder, contractor',            calcs: ['ruerup', 'depot', 'cashflow', 'versicherung'] },
  { id: 'family',       icon: '👨‍👩‍👧', title: 'Building Wealth for Kids', sub: 'Investing · Rürup · Budget',       hint: 'Planning for your family\'s future',         calcs: ['depot', 'ruerup', 'cashflow'] },
];
