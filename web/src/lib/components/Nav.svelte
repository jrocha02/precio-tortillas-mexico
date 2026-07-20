<script>
	import { base } from '$app/paths';
	import { page } from '$app/stores';

	const links = [
		{ href: '', label: 'Inicio' },
		{ href: '/inflacion', label: 'Inflación' },
		{ href: '/ciudades', label: 'Ciudades' },
		{ href: '/canales', label: 'Canales' },
		{ href: '/metodologia', label: 'Metodología' }
	];

	const current = $derived($page.url.pathname.replace(base, '') || '/');
	const isActive = (href) => (href === '' ? current === '/' : current === href);
</script>

<nav>
	<a class="brand" href="{base}/">
		<svg class="disc" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true">
			<circle class="masa" cx="12" cy="12" r="10.5" />
			<circle class="spot" cx="9" cy="10" r="1.1" />
			<circle class="spot" cx="14.2" cy="9" r="0.9" />
			<circle class="spot" cx="13.2" cy="14" r="1.2" />
			<circle class="spot" cx="9.4" cy="14.6" r="0.8" />
			<circle class="spot" cx="16" cy="13.5" r="0.7" />
		</svg>
		<span>Precio de las tortillas en México</span>
	</a>
	<div class="links">
		{#each links as l}
			<a href="{base}{l.href}" class:active={isActive(l.href)}>{l.label}</a>
		{/each}
	</div>
</nav>

<style>
	nav {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem 1rem;
		max-width: var(--maxw);
		margin: 0 auto;
		padding: 0.85rem 1.25rem;
	}
	.brand {
		display: inline-flex;
		align-items: center;
		gap: 0.55rem;
		font-family: 'Fraunces Variable', Georgia, serif;
		font-weight: 600;
		font-size: 1.02rem;
		color: var(--text);
		letter-spacing: -0.01em;
	}
	.brand:hover {
		text-decoration: none;
	}
	.disc .masa {
		fill: var(--corn);
		stroke: var(--terracotta);
		stroke-width: 1.5;
	}
	.disc .spot {
		fill: var(--terracotta);
		opacity: 0.62;
	}
	.links {
		display: flex;
		flex-wrap: wrap;
		gap: 0.15rem;
	}
	.links a {
		padding: 0.35rem 0.7rem;
		color: var(--text-muted);
		font-size: 0.92rem;
		font-weight: 500;
		border-bottom: 2px solid transparent;
	}
	.links a:hover {
		color: var(--text);
		text-decoration: none;
	}
	.links a.active {
		color: var(--terracotta);
		border-bottom-color: var(--corn);
	}
</style>
