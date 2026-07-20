<script>
	import { onMount, onDestroy } from 'svelte';
	import * as echarts from 'echarts';
	import { getPalette, canalColor, currency, pct1, monthYear } from '$lib/format.js';

	/**
	 * @typedef {Object} Props
	 * @property {any[]} data
	 * @property {string} x            - field for the x (time) axis, ISO date strings
	 * @property {string|string[]} y   - one field, or several for multi-line
	 * @property {string} [series]     - field to split long data into series
	 * @property {string} [title]
	 * @property {string} [yAxisTitle]
	 * @property {'currency'|'pct1'} [yFmt]
	 * @property {Record<string,string>} [names] - map raw field -> display name (for y[])
	 */
	let {
		data = [],
		x,
		y,
		series = null,
		title = '',
		yAxisTitle = '',
		yFmt = 'currency',
		names = {}
	} = $props();

	let el;
	let chart;
	let isDark = $state(false);
	let mql;

	const fmt = (v) => (yFmt === 'pct1' ? pct1(v) : currency(v));

	function colorFor(rawName, idx, pal) {
		const s = String(rawName).toLowerCase();
		if (s.includes('tortiller')) return canalColor('tortillerias', isDark);
		if (s.includes('autoservicio')) return canalColor('autoservicios', isDark);
		return pal[idx % pal.length];
	}

	function buildSeries() {
		const pal = getPalette(isDark);
		let raw;
		if (series) {
			const groups = new Map();
			for (const row of data) {
				const key = row[series];
				if (!groups.has(key)) groups.set(key, []);
				groups.get(key).push([new Date(row[x]).getTime(), row[y]]);
			}
			raw = [...groups.entries()].map(([name, pts], i) => ({
				rawName: name,
				name: names[name] || name,
				pts,
				color: colorFor(name, i, pal)
			}));
		} else {
			const yFields = Array.isArray(y) ? y : [y];
			raw = yFields.map((field, i) => ({
				rawName: field,
				name: names[field] || field,
				pts: data.map((row) => [new Date(row[x]).getTime(), row[field]]),
				color: colorFor(field, i, pal)
			}));
		}

		const filled = raw.length <= 2; // area fill only when it won't turn muddy
		const label = series && raw.length > 2; // direct end-labels for multi-city (CVD relief)

		return raw.map((s) => ({
			name: s.name,
			type: 'line',
			showSymbol: false,
			smooth: 0.18,
			connectNulls: true,
			data: s.pts,
			lineStyle: { width: 2, cap: 'round', join: 'round', color: s.color },
			itemStyle: { color: s.color },
			emphasis: { focus: 'series' },
			endLabel: label
				? { show: true, formatter: (p) => p.seriesName, color: s.color, fontSize: 11, fontWeight: 600 }
				: undefined,
			areaStyle: filled
				? {
						opacity: 1,
						color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
							{ offset: 0, color: hexA(s.color, isDark ? 0.28 : 0.22) },
							{ offset: 1, color: hexA(s.color, 0) }
						])
					}
				: undefined
		}));
	}

	function hexA(hex, a) {
		const h = hex.replace('#', '');
		const r = parseInt(h.slice(0, 2), 16);
		const g = parseInt(h.slice(2, 4), 16);
		const b = parseInt(h.slice(4, 6), 16);
		return `rgba(${r},${g},${b},${a})`;
	}

	function css(name) {
		return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
	}

	function option() {
		const s = buildSeries();
		const multi = s.length > 1;
		const hasEndLabel = s.some((x) => x.endLabel);
		const axis = css('--text-muted') || (isDark ? '#b3a184' : '#8b7a5e');
		const grid = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(74,48,20,0.10)';
		const surface = css('--surface') || (isDark ? '#262019' : '#fffdf7');
		const border = css('--border') || (isDark ? '#3e3428' : '#e7dac0');
		const ink = css('--text') || (isDark ? '#f1e7d4' : '#2a2015');
		return {
			color: getPalette(isDark),
			textStyle: { fontFamily: 'Inter Variable, sans-serif' },
			animationDuration: 450,
			grid: { left: 8, right: hasEndLabel ? 96 : 18, top: multi ? 42 : 14, bottom: 6, containLabel: true },
			legend: multi
				? { top: 4, textStyle: { color: axis }, itemWidth: 18, itemHeight: 10, icon: 'roundRect' }
				: undefined,
			tooltip: {
				trigger: 'axis',
				backgroundColor: surface,
				borderColor: border,
				borderWidth: 1,
				textStyle: { color: ink },
				valueFormatter: (v) => fmt(v),
				axisPointer: {
					lineStyle: { color: axis },
					label: { formatter: (p) => monthYear(new Date(p.value)) }
				}
			},
			xAxis: {
				type: 'time',
				axisLabel: { color: axis, formatter: (v) => monthYear(new Date(v)) },
				axisLine: { lineStyle: { color: border } },
				axisTick: { show: false },
				splitLine: { show: false }
			},
			yAxis: {
				type: 'value',
				name: yAxisTitle,
				nameTextStyle: { color: axis, align: 'left' },
				axisLabel: { color: axis, formatter: (v) => fmt(v) },
				splitLine: { lineStyle: { color: grid } }
			},
			series: s
		};
	}

	onMount(() => {
		mql = window.matchMedia('(prefers-color-scheme: dark)');
		isDark = mql.matches;
		const onTheme = (e) => {
			isDark = e.matches;
		};
		mql.addEventListener('change', onTheme);

		chart = echarts.init(el, null, { renderer: 'canvas' });
		chart.setOption(option());

		const ro = new ResizeObserver(() => chart && chart.resize());
		ro.observe(el);

		return () => {
			mql.removeEventListener('change', onTheme);
			ro.disconnect();
		};
	});

	$effect(() => {
		data;
		isDark;
		if (chart) chart.setOption(option(), { notMerge: true });
	});

	onDestroy(() => chart && chart.dispose());
</script>

{#if title}
	<h3 class="chart-title">{title}</h3>
{/if}
<div class="chart" bind:this={el}></div>

<style>
	.chart-title {
		font-family: 'Fraunces Variable', Georgia, serif;
		font-size: 1.05rem;
		font-weight: 600;
		margin: 0.5rem 0 0.4rem;
		color: var(--text);
	}
	.chart {
		width: 100%;
		height: 350px;
	}
</style>
