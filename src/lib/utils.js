export const de0 = new Intl.NumberFormat('de-DE', { maximumFractionDigits: 0 });
export const de1 = new Intl.NumberFormat('de-DE', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
export const fmtE = n => de0.format(Math.round(Math.abs(n))) + ' €';
export const fmtP = n => de1.format(n * 100) + ' %';

export function taxDE(zvE, kirche) {
  let e = 0;
  if (zvE > 12096) {
    if (zvE <= 17443) e = (zvE - 12096) * 0.14;
    else if (zvE <= 68480) e = (zvE - 17443) * 0.24 + 750;
    else if (zvE <= 277825) e = (zvE - 68480) * 0.42 + 12896 + 750;
    else e = (zvE - 277825) * 0.45 + (277825 - 68480) * 0.42 + 12896 + 750;
  }
  const k = kirche ? e * 0.09 : 0;
  const s = e < 18130 ? 0 : e * 0.055;
  return { e, k, s, tot: e + k + s };
}
