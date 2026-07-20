<script>
	import data from '$lib/data/ciudades.json';
	import Dropdown from '$lib/components/Dropdown.svelte';
	import MultiDropdown from '$lib/components/MultiDropdown.svelte';
	import LineChart from '$lib/components/LineChart.svelte';
	import DataTable from '$lib/components/DataTable.svelte';

	const canalOptions = [
		{ value: 'tortillerias', label: 'Tortillerías' },
		{ value: 'autoservicios', label: 'Autoservicios' }
	];
	let canal = $state('tortillerias');
	let cities = $state(['Culiacán', 'Ciudad Juárez', 'Mérida']);

	const trends = $derived(
		data.city_series.filter((d) => d.canal === canal && cities.includes(d.ciudad_canonical))
	);
	const ranking = $derived(data.ranking.filter((d) => d.canal === canal));

	const columns = [
		{ id: 'ciudad_canonical', title: 'Ciudad' },
		{ id: 'estado_canonical', title: 'Estado' },
		{ id: 'region', title: 'Región' },
		{ id: 'precio_mensual', title: 'Precio (MXN/kg)', fmt: 'currency' },
		{ id: 'inflacion_yoy', title: 'Inflación YoY', fmt: 'pct1' }
	];
</script>

<svelte:head><title>Comparar ciudades · Precio de las tortillas en México</title></svelte:head>

<h1>Comparar precios entre ciudades</h1>
<p>Selecciona varias ciudades para comparar la evolución de su precio promedio mensual.</p>

<div class="controls">
	<MultiDropdown title="Ciudades" options={data.cities_list} bind:selected={cities} />
	<Dropdown title="Canal" options={canalOptions} bind:value={canal} />
</div>

<LineChart
	data={trends}
	x="mes"
	y="precio_mensual"
	series="ciudad_canonical"
	title="Precio mensual por ciudad"
	yAxisTitle="MXN / kg"
	yFmt="currency"
/>

<h2 class="section-title">Ranking actual</h2>
<DataTable data={ranking} {columns} rows={15} search={true} />

<style>
	.controls {
		display: flex;
		gap: 1.5rem;
		flex-wrap: wrap;
		margin: 1.25rem 0 2rem;
		align-items: flex-start;
	}
</style>
