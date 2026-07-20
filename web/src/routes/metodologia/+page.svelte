<svelte:head><title>Metodología · Precio de las tortillas en México</title></svelte:head>

<h1>Metodología</h1>
<p>Cómo se construye este sitio, de dónde vienen los datos, y qué saber antes de citar los números.</p>

<h2 class="section-title">Fuente de los datos</h2>
<p>
	Todos los precios provienen del
	<a href="https://www.economia-sniim.gob.mx/TortillaMesPorDia.asp">SNIIM</a>
	(Sistema Nacional de Información e Integración de Mercados), una iniciativa de la Secretaría de
	Economía que publica precios de productos básicos desde 2007.
</p>
<p>
	SNIIM publica precios de tortilla <strong>tres veces por semana</strong> (lunes, miércoles y
	viernes), por ciudad y por canal de venta. Este sitio raspa esos datos automáticamente, los
	limpia, los modela y los republica en formato abierto.
</p>

<h2 class="section-title">Arquitectura</h2>
<p>
	El pipeline corre automáticamente vía GitHub Actions tres veces por semana (martes, jueves y
	sábado), un día después de cada publicación de SNIIM. Cada corrida reconstruye y republica este
	sitio en GitHub Pages.
</p>

<h2 class="section-title">Stack técnico</h2>
<ul>
	<li><strong>Python 3.13</strong> con <code>uv</code>, <code>httpx</code> + <code>pandas</code> para el scraper</li>
	<li><strong>dbt-duckdb</strong> para modelado de datos con esquema en estrella</li>
	<li><strong>DuckDB</strong> como motor de almacenamiento local</li>
	<li><strong>GitHub Actions</strong> para orquestación y CI/CD</li>
	<li><strong>GitHub Pages</strong> para hospedar este sitio y la documentación de dbt</li>
	<li><strong>SvelteKit</strong> (build estático) con <strong>ECharts</strong> y <strong>Leaflet + OpenStreetMap</strong> para el sitio que estás viendo</li>
</ul>

<h2 class="section-title">Modelo de datos</h2>
<p>Los datos siguen un esquema en estrella clásico, organizados en capas:</p>
<ul>
	<li><strong>Staging</strong> (<code>stg_sniim__tortilla_prices</code>): datos crudos limpiados.</li>
	<li><strong>Dimensiones</strong> (<code>dim_city</code>): catálogo canónico de 56 ciudades con código INEGI y región.</li>
	<li><strong>Hechos</strong> (<code>fct_tortilla_prices_daily</code>): un registro por (ciudad, canal, fecha).</li>
	<li><strong>Marts</strong> (<code>mart_price_inflation</code>, <code>mart_price_dispersion</code>, <code>mart_channel_gap</code>): tablas pre-agregadas.</li>
</ul>

<h2 class="section-title">Datos disponibles para descarga</h2>
<p>
	Cada ejecución exitosa del pipeline publica los marts como archivos Parquet a un
	<a href="https://github.com/jrocha02/precio-tortillas-mexico/releases/latest">release público de GitHub</a>.
	Puedes consultarlos directamente desde DuckDB, Python, R, o cualquier herramienta que lea Parquet
	por URL.
</p>

<div class="table-wrap">
	<table>
		<thead>
			<tr><th>Archivo</th><th>Grano</th><th>Filas aprox.</th></tr>
		</thead>
		<tbody>
			<tr><td>fct_tortilla_prices_daily.parquet</td><td>Ciudad × canal × día</td><td>257,000</td></tr>
			<tr><td>dim_city.parquet</td><td>Ciudad</td><td>56</td></tr>
			<tr><td>mart_price_inflation.parquet</td><td>Ciudad × canal × mes</td><td>20,000</td></tr>
			<tr><td>mart_price_dispersion.parquet</td><td>Canal × mes</td><td>432</td></tr>
			<tr><td>mart_channel_gap.parquet</td><td>Ciudad × mes</td><td>8,100</td></tr>
		</tbody>
	</table>
</div>

<pre><code>import duckdb
df = duckdb.sql("""
    SELECT *
    FROM 'https://github.com/jrocha02/precio-tortillas-mexico/releases/latest/download/fct_tortilla_prices_daily.parquet'
    WHERE ciudad_canonical = 'Culiacán'
""").df()</code></pre>

<h2 class="section-title">Advertencias sobre los datos</h2>
<ul>
	<li><strong>El canal de tortillerías comienza en 2010.</strong> SNIIM solo publicaba autoservicios antes.</li>
	<li><strong>Cobertura variable año con año.</strong> Autoservicios cubre ~50–56 ciudades; tortillerías ~41–43.</li>
	<li><strong>Los canales no son directamente comparables.</strong> Autoservicios reporta tortilla industrial; tortillerías, tortilla fresca de nixtamal.</li>
	<li><strong>El año 2026 es parcial.</strong> Los datos del año actual están al día pero incompletos.</li>
	<li><strong>SNIIM revisa ocasionalmente meses pasados.</strong> Este sitio refleja la versión más reciente.</li>
	<li><strong>Algunas ciudades aparecen como ZM</strong> (Zona Metropolitana) y pueden sobreestimar el centro del país.</li>
</ul>

<h2 class="section-title">Código y reproducibilidad</h2>
<p>
	Todo el código es público:
	<a href="https://github.com/jrocha02/precio-tortillas-mexico">github.com/jrocha02/precio-tortillas-mexico</a>.
	El sitio se reconstruye automáticamente; revisa los
	<a href="https://github.com/jrocha02/precio-tortillas-mexico/actions">GitHub Actions</a> para timestamps.
</p>

<style>
	.table-wrap {
		overflow-x: auto;
		border: 1px solid var(--border);
		border-radius: var(--radius);
		margin: 1rem 0;
	}
	th,
	td {
		padding: 0.5rem 0.75rem;
		text-align: left;
		border-bottom: 1px solid var(--border);
	}
	th {
		background: var(--surface-2);
	}
	tbody tr:last-child td {
		border-bottom: none;
	}
</style>
