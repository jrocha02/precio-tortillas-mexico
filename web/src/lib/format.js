// Formatting helpers that mirror the Evidence formats used on the old site.

const MESES = [
	'ene', 'feb', 'mar', 'abr', 'may', 'jun',
	'jul', 'ago', 'sep', 'oct', 'nov', 'dic'
];

/** "$#,##0.00" -> "$26.16" */
export function currency(v) {
	if (v == null || Number.isNaN(v)) return '—';
	return '$' + Number(v).toLocaleString('en-US', {
		minimumFractionDigits: 2,
		maximumFractionDigits: 2
	});
}

/** Evidence pct1 -> "3.1%" (input is a ratio, e.g. 0.031) */
export function pct1(v) {
	if (v == null || Number.isNaN(v)) return '—';
	return (Number(v) * 100).toFixed(1) + '%';
}

/** "mmm yyyy" -> "abr 2011". Accepts an ISO date string or Date. */
export function monthYear(v) {
	const d = v instanceof Date ? v : new Date(v);
	if (Number.isNaN(d.getTime())) return String(v);
	return `${MESES[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
}

/** Long human date+time for the "last updated" card: "19 jul 2026, 08:14". */
export function dateTime(v) {
	const d = v instanceof Date ? v : new Date(v);
	if (Number.isNaN(d.getTime())) return String(v);
	const hh = String(d.getHours()).padStart(2, '0');
	const mm = String(d.getMinutes()).padStart(2, '0');
	return `${d.getDate()} ${MESES[d.getMonth()]} ${d.getFullYear()}, ${hh}:${mm}`;
}

/**
 * Warm "maíz & masa" categorical series colors, validated with the dataviz
 * palette checker (fixed order — assign by entity, never cycle).
 * Order: terracotta, teal, amber, plum, agave, chili.
 */
export const PALETTE_LIGHT = [
	'#c15a2b', '#0088a0', '#b07400', '#a23a63', '#6e8b3d', '#b23120'
];
export const PALETTE_DARK = [
	'#d97048', '#1f97ac', '#be8a10', '#c56c93', '#5e9e4a', '#d8483a'
];

export function getPalette(isDark) {
	return isDark ? PALETTE_DARK : PALETTE_LIGHT;
}

/** Fixed color per sales channel, consistent across every chart. */
const CANAL_LIGHT = { tortillerias: '#c15a2b', autoservicios: '#b07400' };
const CANAL_DARK = { tortillerias: '#d97048', autoservicios: '#be8a10' };
export function canalColor(canal, isDark) {
	return (isDark ? CANAL_DARK : CANAL_LIGHT)[canal] || (isDark ? '#d97048' : '#c15a2b');
}

/** Back-compat alias (light palette) for any importer that wants a default. */
export const PALETTE = PALETTE_LIGHT;

/**
 * Warm sequential ramp (pale corn -> corn -> terracotta -> deep chili),
 * used by the colorscale table cells and the map markers. t in [0, 1].
 */
const RAMP = [
	[0.0, [246, 231, 184]], // #F6E7B8 pale corn
	[0.4, [224, 162, 26]],  // #E0A21A corn
	[0.72, [193, 90, 43]],  // #C15A2B terracotta
	[1.0, [140, 46, 21]]    // #8C2E15 deep chili
];
export function colorScale(t) {
	const c = Math.max(0, Math.min(1, t));
	for (let i = 1; i < RAMP.length; i++) {
		const [t0, a] = RAMP[i - 1];
		const [t1, b] = RAMP[i];
		if (c <= t1) {
			const k = (c - t0) / (t1 - t0);
			const rgb = a.map((v, j) => Math.round(v + (b[j] - v) * k));
			return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
		}
	}
	return 'rgb(140, 46, 21)';
}

/** Cream text on the darker (hotter) cells, roasted-brown ink on the lighter ones. */
export function contrastText(t) {
	return t > 0.5 ? '#fff7e8' : '#2a2015';
}
