<script>
	import data from '$lib/data/inflacion.json';
	import Dropdown from '$lib/components/Dropdown.svelte';
	import LineChart from '$lib/components/LineChart.svelte';
	import DataTable from '$lib/components/DataTable.svelte';

	const canalOptions = [
		{ value: 'tortillerias', label: 'Tortillerías' },
		{ value: 'autoservicios', label: 'Autoservicios' }
	];
	let canal = $state('tortillerias');

	const yoy = $derived(data.yoy.filter((d) => d.canal === canal));
	const top10 = $derived(data.top_inflation.filter((d) => d.canal === canal).slice(0, 10));

	const columns = [
		{ id: 'ciudad_canonical', title: 'Ciudad' },
		{ id: 'estado_canonical', title: 'Estado' },
		{ id: 'mes', title: 'Mes', fmt: 'monthYear' },
		{ id: 'precio_mensual', title: 'Precio', fmt: 'currency' },
		{ id: 'inflacion_yoy', title: 'Inflación YoY', fmt: 'pct1', colorscale: true }
	];
</script>

<svelte:head><title>La historia de la inflación · Precio de las tortillas en México</title></svelte:head>

<h1>Comparación de la inflación a través de los años</h1>
<p>
	El precio de la tortilla se ha triplicado desde 2010 y últimamente se ha tenido un repunte en
	los precios.
</p>

<div class="controls">
	<Dropdown title="Canal" options={canalOptions} bind:value={canal} />
</div>

<h2 class="section-title">Inflación anualizada</h2>
<LineChart
	data={yoy}
	x="mes"
	y="inflacion_yoy_nacional"
	title="Inflación anualizada (YoY) — promedio nacional"
	yAxisTitle="Cambio anual (%)"
	yFmt="pct1"
/>
<p>
	Cada punto representa cuánto más cara estaba la tortilla en ese mes comparado con doce meses
	antes. Valores por encima de 10% indican inflación significativa.
</p>

<h2 class="section-title">Top 10: los peores momentos de inflación</h2>
<p>Las 10 ciudades más golpeadas por la inflación.</p>
<DataTable data={top10} {columns} rows={10} />

<p>
	Para las tortillerías la mayoría se centran en <strong>2023</strong>. En ciudades como Ciudad Juárez y
  Guadalajara y en zonas urbanas del centro de México , esto se debió a que los ingredientes de las tortillas 
  como la harina y la toneladad del maíz blanco subió.
</p>

<style>
	.controls {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
		margin: 1.25rem 0;
	}
</style>
