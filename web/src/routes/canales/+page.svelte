<script>
	import data from '$lib/data/canales.json';
	import LineChart from '$lib/components/LineChart.svelte';
	import DataTable from '$lib/components/DataTable.svelte';

	const seriesNames = {
		precio_tortilleria: 'Tortillería',
		precio_autoservicio: 'Autoservicio'
	};

	const columns = [
		{ id: 'ciudad_canonical', title: 'Ciudad' },
		{ id: 'estado_canonical', title: 'Estado' },
		{ id: 'region', title: 'Región' },
		{ id: 'precio_tortilleria', title: 'Tortillería', fmt: 'currency' },
		{ id: 'precio_autoservicio', title: 'Autoservicio', fmt: 'currency' },
		{ id: 'gap_absoluto', title: 'Diferencia', fmt: 'currency' },
		{ id: 'gap_relativo', title: 'Brecha %', fmt: 'pct1', colorscale: true }
	];
</script>

<svelte:head><title>Tortillerías vs autoservicios · Precio de las tortillas en México</title></svelte:head>

<h1>Tortillerías vs autoservicios</h1>
<p>
	Las tortillerías cobran consistentemente más que los supermercados. Pero antes de leer estos
	números como "eficiencia del autoservicio", hay un matiz importante.
</p>

<blockquote>
	<strong>Aviso sobre los datos.</strong> Los autoservicios venden principalmente tortilla
	industrial (genérica), mientras que las tortillerías venden tortilla fresca de nixtamal. Son
	productos distintos. La diferencia de precio refleja tanto el tipo de producto como el margen
	del vendedor — no son directamente comparables.
</blockquote>

<h2 class="section-title">Brecha promedio nacional a lo largo del tiempo</h2>
<LineChart
	data={data.channel_trend}
	x="mes"
	y={['precio_tortilleria', 'precio_autoservicio']}
	names={seriesNames}
	title="Precio promedio nacional por canal"
	yAxisTitle="MXN / kg"
	yFmt="currency"
/>

<h2 class="section-title">Brecha relativa a través del tiempo</h2>
<LineChart
	data={data.gap_over_time}
	x="mes"
	y="gap_promedio"
	title="¿Cuánto más caro es comprar en tortillería?"
	yAxisTitle="Diferencia relativa"
	yFmt="pct1"
/>
<p>
	Un valor de 100% significa que las tortillerías cobran el doble que los autoservicios. La
	estabilidad de esta línea sugiere que las dos categorías de producto se mueven en paralelo,
	aunque a niveles de precio muy distintos.
</p>

<h2 class="section-title">Brecha actual por ciudad</h2>
<p>Ciudades con la mayor diferencia entre canales en el mes más reciente:</p>
<DataTable data={data.current_gap_by_city} {columns} rows={20} search={true} />

<h2 class="section-title">¿Por qué importa esta diferencia?</h2>
<p>
	Esta brecha refleja una elección común en hogares mexicanos: pagar más por tortilla fresca de
	nixtamal, o ahorrar comprando tortilla industrial empacada. Los datos muestran que el ahorro es
	sustancial — alrededor de <strong>40–60% más barato</strong> comprar en el supermercado, a costa
	de un producto distinto en sabor, textura y elaboración.
</p>
