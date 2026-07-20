<script>
	import meta from '$lib/data/meta.json';
	import { dateTime, monthYear } from '$lib/format.js';
</script>

<div class="updated">
	<span class="dot" aria-hidden="true"></span>
	<span>
		<strong>Última actualización:</strong> {dateTime(meta.built_at)}
		<span class="sep">·</span>
		<strong>Datos hasta:</strong> {monthYear(meta.latest_mes)}
	</span>
</div>

<style>
	.updated {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		font-size: 0.85rem;
		color: var(--text-muted);
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: 999px;
		padding: 0.4rem 0.9rem;
		width: fit-content;
	}
	.updated strong {
		color: var(--text);
		font-weight: 600;
	}
	.dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: var(--positive);
		flex: none;
	}
	.sep {
		margin: 0 0.3rem;
		opacity: 0.5;
	}
</style>
