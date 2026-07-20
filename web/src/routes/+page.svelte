<script>
	import data from '$lib/data/index.json';
	import BigValue from '$lib/components/BigValue.svelte';
	import LineChart from '$lib/components/LineChart.svelte';
	import PriceMap from '$lib/components/PriceMap.svelte';

	const byCanal = (c) => data.precio_actual.find((d) => d.canal === c) || {};
	const tort = byCanal('tortillerias');
	const auto = byCanal('autoservicios');
	const canalNombre = { tortillerias: 'Tortillerías', autoservicios: 'Autoservicios' };
</script>

<svelte:head><title>Precio de las tortillas en México</title></svelte:head>

<section class="hero">
	<p class="eyebrow">El costo del kilo, desde 2007</p>
	<h1>El precio de la<br />tortilla en México</h1>
	<p class="deck">
		Cada semana raspamos los precios del SNIIM, los modelamos con dbt y los seguimos —
		tortillería por tortillería, ciudad por ciudad.
	</p>

	<div class="stats">
		<BigValue
			value={tort.precio}
			title="Precio promedio en tortillería"
			fmt="currency"
			featured={true}
			note="MXN por kilo · mes más reciente"
		/>
		<div class="stats-side">
			<BigValue value={auto.precio} title="Precio en autoservicio" fmt="currency" />
			<BigValue
				value={tort.inflacion_yoy}
				title="Inflación 12m (tortillería)"
				fmt="pct1"
				note="vs. hace un año"
			/>
		</div>
	</div>
</section>

<h2 class="section-title">Precio nacional a través del tiempo</h2>
<LineChart
	data={data.precio_nacional_mensual}
	x="mes"
	y="precio"
	series="canal"
	names={canalNombre}
	yAxisTitle="MXN / kg"
	yFmt="currency"
/>

<h2 class="section-title">Precio por ciudad</h2>
<PriceMap points={data.city_points} title="Precio actual en tortillería, mes más reciente" />

<style>
	.hero {
		position: relative;
		margin: 0.5rem 0 2.5rem;
		padding: 1.5rem 1.5rem 2rem;
		border-radius: var(--radius);
		overflow: hidden;
		background:
			radial-gradient(circle at 1px 1px, rgba(193, 90, 43, 0.09) 1px, transparent 0) 0 0 / 18px
				18px,
			linear-gradient(160deg, color-mix(in srgb, var(--corn) 12%, var(--surface)), var(--surface));
		border: 1px solid var(--border);
		box-shadow: var(--shadow);
	}
	.eyebrow {
		font-size: 0.8rem;
		font-weight: 600;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--terracotta);
		margin: 0 0 0.4rem;
	}
	.hero h1 {
		margin: 0 0 0.6rem;
	}
	.deck {
		max-width: 40rem;
		color: var(--text-muted);
		font-size: 1.05rem;
		margin: 0 0 1.75rem;
	}
	.stats {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
	}
	.stats-side {
		flex: 1 1 260px;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
</style>
