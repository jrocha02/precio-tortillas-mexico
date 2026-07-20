<script>
	/**
	 * @property {string[]} options
	 * @property {string[]} selected - bindable
	 * @property {string} title
	 */
	let { options = [], selected = $bindable([]), title = '' } = $props();
	let open = $state(false);

	function toggle(opt) {
		if (selected.includes(opt)) selected = selected.filter((s) => s !== opt);
		else selected = [...selected, opt];
	}
</script>

<div class="md">
	{#if title}<span class="md-title">{title}</span>{/if}
	<button type="button" class="md-toggle" onclick={() => (open = !open)}>
		{selected.length ? `${selected.length} seleccionadas` : 'Seleccionar…'}
		<span class="caret">{open ? '▲' : '▼'}</span>
	</button>
	{#if open}
		<div class="md-panel">
			{#each options as opt}
				<label class="md-opt">
					<input type="checkbox" checked={selected.includes(opt)} onchange={() => toggle(opt)} />
					{opt}
				</label>
			{/each}
		</div>
	{/if}
	{#if selected.length}
		<div class="chips">
			{#each selected as s}
				<button type="button" class="chip" onclick={() => toggle(s)}>{s} ✕</button>
			{/each}
		</div>
	{/if}
</div>

<style>
	.md {
		display: inline-flex;
		flex-direction: column;
		gap: 0.3rem;
		font-size: 0.85rem;
		position: relative;
	}
	.md-title {
		color: var(--text-muted);
		font-weight: 600;
	}
	.md-toggle {
		padding: 0.5rem 0.75rem;
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		background: var(--surface);
		color: var(--text);
		font-size: 0.9rem;
		min-width: 200px;
		text-align: left;
		display: flex;
		justify-content: space-between;
		cursor: pointer;
		box-shadow: var(--shadow);
	}
	.md-toggle:focus {
		outline: 2px solid var(--corn);
		outline-offset: 1px;
	}
	.md-panel {
		position: absolute;
		top: 3.6rem;
		z-index: 5;
		max-height: 260px;
		overflow-y: auto;
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: 8px;
		padding: 0.4rem;
		min-width: 220px;
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
	}
	.md-opt {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.25rem 0.4rem;
		border-radius: 6px;
		cursor: pointer;
	}
	.md-opt:hover {
		background: var(--surface-2);
	}
	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.35rem;
	}
	.chip {
		border: 1px solid color-mix(in srgb, var(--terracotta) 40%, var(--border));
		background: color-mix(in srgb, var(--terracotta) 14%, transparent);
		color: var(--text);
		border-radius: 999px;
		padding: 0.18rem 0.65rem;
		font-size: 0.8rem;
		cursor: pointer;
	}
	.chip:hover {
		background: color-mix(in srgb, var(--terracotta) 24%, transparent);
	}
</style>
