<script>
	import '@fontsource-variable/fraunces';
	import '@fontsource-variable/inter';
	import '../app.css';
	import { base } from '$app/paths';
	import Nav from '$lib/components/Nav.svelte';
	import LastUpdatedCard from '$lib/components/LastUpdatedCard.svelte';
	let { children } = $props();
</script>

<header>
	<Nav />
</header>

<div class="page">
	<div class="updated-row">
		<LastUpdatedCard />
	</div>
	{@render children()}
</div>

<footer>
	<div class="foot">
		<span class="foot-mark">Precio de las tortillas en México</span>
		<span class="foot-links">
			Datos del <a href="https://www.economia-sniim.gob.mx/TortillaMesPorDia.asp">SNIIM</a> ·
			Código en <a href="https://github.com/jrocha02/precio-tortillas-mexico">GitHub</a> ·
			<a href="{base}/dbt-docs/index.html">dbt docs</a>
		</span>
	</div>
</footer>

<style>
	header {
		border-bottom: 1px solid var(--border);
		background: color-mix(in srgb, var(--bg) 88%, transparent);
		backdrop-filter: saturate(1.4) blur(8px);
		position: sticky;
		top: 0;
		z-index: 10;
	}
	.updated-row {
		margin-bottom: 1.5rem;
	}
	footer {
		border-top: 1px solid var(--border);
		margin-top: 3.5rem;
		background: var(--surface);
	}
	.foot {
		max-width: var(--maxw);
		margin: 0 auto;
		padding: 1.75rem 1.25rem;
		font-size: 0.85rem;
		color: var(--text-muted);
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		gap: 0.5rem 1.5rem;
	}
	.foot-mark {
		font-family: 'Fraunces Variable', Georgia, serif;
		color: var(--text);
		font-weight: 600;
	}
</style>
