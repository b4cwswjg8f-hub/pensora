import { de0 } from './utils.js';

export function lineChart(series, years) {
  const w = 800, h = 280, pad = 40;
  const allVals = series.flatMap(s => s.data);
  const maxY = Math.max(...allVals) * 1.12;
  const xs = i => pad + (i / years) * (w - pad * 2);
  const ys = v => h - pad - Math.max(0, Math.min(v / maxY, 1)) * (h - pad * 2);
  const path = arr => arr.map((v, i) => `${i === 0 ? 'M' : 'L'}${xs(i).toFixed(1)},${ys(v).toFixed(1)}`).join(' ');
  const area = arr => `M${xs(0)},${h - pad} ${arr.map((v, i) => `L${xs(i).toFixed(1)},${ys(v).toFixed(1)}`).join(' ')} L${xs(arr.length - 1)},${h - pad} Z`;
  const yr = new Date().getFullYear();
  const labels = [0, .25, .5, .75, 1].map(f => Math.round(f * maxY));
  return `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" style="display:block">
    <defs>${series.map((s, i) => s.fill ? `<linearGradient id="lg${i}" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="${s.color}" stop-opacity=".3"/><stop offset="100%" stop-color="${s.color}" stop-opacity="0"/></linearGradient>` : '').join('')}</defs>
    ${labels.map(v => `<line x1="${pad}" x2="${w - pad}" y1="${ys(v).toFixed(1)}" y2="${ys(v).toFixed(1)}" stroke="#1f1f1f" stroke-width="1" ${v > 0 ? 'stroke-dasharray="2 3"' : ''}/>
      <text x="${pad - 6}" y="${(ys(v) + 3).toFixed(1)}" fill="#6b6b6b" font-size="10" font-family="'Geist Mono',ui-monospace" text-anchor="end">${de0.format(Math.round(v / 1000))}k</text>`).join('')}
    ${[0, .25, .5, .75, 1].map(f => `<text x="${xs(Math.round(f * years)).toFixed(1)}" y="${h - pad + 16}" fill="#6b6b6b" font-size="10" font-family="'Geist Mono',ui-monospace" text-anchor="middle">${yr + Math.round(f * years)}</text>`).join('')}
    ${series.map((s, i) => s.fill ? `<path d="${area(s.data)}" fill="url(#lg${i})"/>` : '').join('')}
    ${series.map((s) => `<path d="${path(s.data)}" stroke="${s.color}" stroke-width="${s.width || 2}" fill="none" ${s.dash ? `stroke-dasharray="${s.dash}"` : ''}/>`).join('')}
    ${series[0] ? `<circle cx="${xs(0)}" cy="${ys(series[0].data[0]).toFixed(1)}" r="5" fill="${series[0].color}"/>` : ''}
  </svg>`;
}

export function barChart(bars) {
  const max = Math.max(...bars.map(b => b.val)) * 1.1;
  const w = 800, h = 200, pad = 40, bw = Math.floor((w - pad * 2) / bars.length * 0.6);
  const xs = i => pad + (i + 0.2) * (w - pad * 2) / bars.length;
  const ys = v => h - pad - Math.max(0, v / max) * (h - pad * 1.5);
  return `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" style="display:block">
    ${[0, .25, .5, .75, 1].map(f => `<line x1="${pad}" x2="${w - pad}" y1="${ys(f * max).toFixed(1)}" y2="${ys(f * max).toFixed(1)}" stroke="#1f1f1f" stroke-width="1" ${f > 0 ? 'stroke-dasharray="2 3"' : ''}/>
      <text x="${pad - 6}" y="${(ys(f * max) + 3).toFixed(1)}" fill="#6b6b6b" font-size="10" font-family="'Geist Mono',ui-monospace" text-anchor="end">${de0.format(Math.round(f * max / 1000))}k</text>`).join('')}
    ${bars.map((b, i) => `
      <rect x="${xs(i)}" y="${ys(b.val).toFixed(1)}" width="${bw}" height="${(h - pad - ys(b.val)).toFixed(1)}" fill="${b.color}" rx="3"/>
      <text x="${(xs(i) + bw / 2).toFixed(1)}" y="${(ys(b.val) - 6).toFixed(1)}" fill="${b.color}" font-size="11" font-family="'Geist Mono',ui-monospace" text-anchor="middle" font-weight="600">${de0.format(Math.round(b.val))}</text>
      <text x="${(xs(i) + bw / 2).toFixed(1)}" y="${h - pad + 16}" fill="#6b6b6b" font-size="10" font-family="'Geist Mono',ui-monospace" text-anchor="middle">${b.label}</text>`).join('')}
  </svg>`;
}

export function legend(items) {
  return `<div class="row g24" style="flex-wrap:wrap;font-size:12px;color:var(--fg2);font-family:var(--mono)">${items.map(([c, l, d]) => `<span><span style="display:inline-block;width:14px;height:${d ? '0' : d === false ? '10px' : '2px'};${d === false ? `background:${c};border-radius:2px` : d ? `border-top:2px ${d} ${c};vertical-align:middle` : `background:${c};vertical-align:middle`};margin-right:8px"></span>${l}</span>`).join('')}</div>`;
}
