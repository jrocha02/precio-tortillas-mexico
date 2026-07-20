<script>
	/**
	 * @property {{value:string,label:string}[]} options
	 * @property {string} value  - bindable
	 * @property {string} title
	 */
	let { options = [], value = $bindable(), title = '' } = $props();
</script>

<label class="dd">
	{#if title}<span class="dd-title">{title}</span>{/if}
	<select bind:value>
		{#each options as opt}
			<option value={opt.value}>{opt.label}</option>
		{/each}
	</select>
</label>

<style>
	.dd {
		display: inline-flex;
		flex-direction: column;
		gap: 0.25rem;
		font-size: 0.85rem;
	}
	.dd-title {
		color: var(--text-muted);
		font-weight: 600;
	}
	select {
		padding: 0.5rem 0.75rem;
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		background: var(--surface);
		color: var(--text);
		font-size: 0.9rem;
		min-width: 160px;
		box-shadow: var(--shadow);
	}
	select:focus {
		outline: 2px solid var(--corn);
		outline-offset: 1px;
		border-color: transparent;
	}
</style>
