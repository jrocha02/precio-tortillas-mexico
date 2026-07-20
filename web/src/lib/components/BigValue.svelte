<script>
	import { currency, pct1 } from '$lib/format.js';
	let { value, title = '', fmt = 'currency', featured = false, note = '' } = $props();

	const shown = $derived(
		value == null ? '—' : fmt === 'pct1' ? pct1(value) : currency(value)
	);
	const isPct = $derived(fmt === 'pct1');
	const up = $derived(isPct && value != null && value >= 0);
</script>

<div class="bigvalue card" class:featured>
	<div class="title">{title}</div>
	<div class="value tnum">
		{shown}
		{#if isPct && value != null}
			<span class="delta" class:up class:down={!up}>{up ? '▲' : '▼'}</span>
		{/if}
	</div>
	{#if note}<div class="note">{note}</div>{/if}
</div>

<style>
	.bigvalue {
		flex: 1 1 200px;
		min-width: 180px;
		position: relative;
		overflow: hidden;
	}
	.bigvalue::before {
		content: '';
		position: absolute;
		left: 0;
		top: 0;
		bottom: 0;
		width: 5px;
		background: var(--corn);
		opacity: 0.6;
	}
	.featured {
		flex: 2 1 320px;
		background: linear-gradient(135deg, var(--surface), var(--surface-2));
		box-shadow: var(--shadow-lg);
	}
	.featured::before {
		width: 7px;
		background: var(--terracotta);
		opacity: 1;
	}
	.title {
		font-size: 0.82rem;
		color: var(--text-muted);
		margin-bottom: 0.4rem;
		letter-spacing: 0.02em;
	}
	.value {
		font-family: 'Fraunces Variable', Georgia, serif;
		font-weight: 600;
		font-size: 2.1rem;
		line-height: 1.05;
		display: flex;
		align-items: baseline;
		gap: 0.5rem;
	}
	.featured .value {
		font-size: clamp(2.8rem, 8vw, 3.8rem);
	}
	.delta {
		font-family: 'Inter Variable', sans-serif;
		font-size: 1rem;
	}
	.delta.up {
		color: var(--chili);
	}
	.delta.down {
		color: var(--agave);
	}
	.note {
		font-size: 0.8rem;
		color: var(--text-muted);
		margin-top: 0.35rem;
	}
</style>
