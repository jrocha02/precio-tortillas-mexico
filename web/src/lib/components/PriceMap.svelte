<script>
	import { onMount } from 'svelte';
	import 'leaflet/dist/leaflet.css';
	import { currency, colorScale } from '$lib/format.js';

	/** @property {{ciudad_canonical:string,estado_canonical:string,lat:number,lng:number,precio:number}[]} points */
	let { points = [], title = '' } = $props();

	let el;

	onMount(async () => {
		const L = (await import('leaflet')).default;

		const map = L.map(el, { scrollWheelZoom: false, attributionControl: true }).setView(
			[23.6, -102.5],
			5
		);

		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 18,
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
		}).addTo(map);

		const prices = points.map((p) => p.precio).filter((v) => v != null);
		const min = Math.min(...prices);
		const max = Math.max(...prices);
		const t = (v) => (max > min ? (v - min) / (max - min) : 0.5);

		for (const p of points) {
			L.circleMarker([p.lat, p.lng], {
				radius: 7,
				color: '#ffffff',
				weight: 1.5,
				fillColor: colorScale(t(p.precio)),
				fillOpacity: 0.9
			})
				.bindTooltip(
					`<strong>${p.ciudad_canonical}</strong>, ${p.estado_canonical}<br>${currency(p.precio)} / kg`,
					{ direction: 'top' }
				)
				.addTo(map);
		}

		const ro = new ResizeObserver(() => map.invalidateSize());
		ro.observe(el);
		return () => {
			ro.disconnect();
			map.remove();
		};
	});
</script>

{#if title}
	<h3 class="chart-title">{title}</h3>
{/if}
<div class="map" bind:this={el}></div>
<p class="legend">Color más oscuro = precio más alto (tortillerías, mes más reciente).</p>

<style>
	.chart-title {
		font-family: 'Fraunces Variable', Georgia, serif;
		font-size: 1.05rem;
		font-weight: 600;
		margin: 0.5rem 0 0.5rem;
	}
	.map {
		width: 100%;
		height: 480px;
		border-radius: var(--radius);
		border: 1px solid var(--border);
		box-shadow: var(--shadow);
		z-index: 0;
	}
	/* warm the OpenStreetMap tiles so the corn→chili markers pop and it matches the palette */
	.map :global(.leaflet-tile-pane) {
		filter: sepia(0.16) saturate(1.05) brightness(1.02);
	}
	@media (prefers-color-scheme: dark) {
		.map :global(.leaflet-tile-pane) {
			filter: sepia(0.2) saturate(0.85) brightness(0.82) contrast(0.95);
		}
	}
	.legend {
		font-size: 0.8rem;
		color: var(--text-muted);
		margin: 0.6rem 0 0;
	}
</style>
