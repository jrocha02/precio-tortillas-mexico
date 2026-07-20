<script>
	import { currency, pct1, monthYear, colorScale, contrastText } from '$lib/format.js';

	/**
	 * @property {any[]} data
	 * @property {{id:string,title:string,fmt?:'currency'|'pct1'|'monthYear',colorscale?:boolean,align?:string}[]} columns
	 * @property {number} [rows]     - max rows to show
	 * @property {boolean} [search]
	 */
	let { data = [], columns = [], rows = 20, search = false } = $props();

	let query = $state('');
	let sortId = $state(null);
	let sortDir = $state(1); // 1 asc, -1 desc

	function fmtCell(v, fmt) {
		if (v == null) return '—';
		if (fmt === 'currency') return currency(v);
		if (fmt === 'pct1') return pct1(v);
		if (fmt === 'monthYear') return monthYear(v);
		return v;
	}

	// per-column min/max for colorscale
	const ranges = $derived.by(() => {
		const r = {};
		for (const c of columns) {
			if (!c.colorscale) continue;
			const vals = data.map((d) => d[c.id]).filter((v) => v != null && !Number.isNaN(v));
			r[c.id] = vals.length ? [Math.min(...vals), Math.max(...vals)] : [0, 1];
		}
		return r;
	});

	const filtered = $derived.by(() => {
		let out = data;
		if (search && query.trim()) {
			const q = query.toLowerCase();
			out = out.filter((row) =>
				columns.some((c) => String(row[c.id] ?? '').toLowerCase().includes(q))
			);
		}
		if (sortId) {
			out = [...out].sort((a, b) => {
				const av = a[sortId];
				const bv = b[sortId];
				if (av == null) return 1;
				if (bv == null) return -1;
				if (typeof av === 'number' && typeof bv === 'number') return (av - bv) * sortDir;
				return String(av).localeCompare(String(bv)) * sortDir;
			});
		}
		return out.slice(0, rows);
	});

	function toggleSort(id) {
		if (sortId === id) sortDir = -sortDir;
		else {
			sortId = id;
			sortDir = 1;
		}
	}

	function cellStyle(c, v) {
		if (!c.colorscale || v == null) return '';
		const [min, max] = ranges[c.id];
		const t = max > min ? (v - min) / (max - min) : 0.5;
		return `background:${colorScale(t)};color:${contrastText(t)};`;
	}
</script>

{#if search}
	<input class="search" placeholder="Buscar…" bind:value={query} />
{/if}
<div class="table-wrap">
	<table>
		<thead>
			<tr>
				{#each columns as c}
					<th
						class:num={c.align === 'right'}
						class:active={sortId === c.id}
						onclick={() => toggleSort(c.id)}
					>
						{c.title}
						<span class="arrow">{sortId === c.id ? (sortDir === 1 ? '▲' : '▼') : ''}</span>
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each filtered as row}
				<tr>
					{#each columns as c}
						<td class:num={c.align === 'right' || c.fmt} style={cellStyle(c, row[c.id])}>
							{fmtCell(row[c.id], c.fmt)}
						</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	.search {
		width: 100%;
		max-width: 260px;
		padding: 0.5rem 0.8rem;
		margin-bottom: 0.7rem;
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		background: var(--surface);
		color: var(--text);
		font-size: 0.9rem;
	}
	.search:focus {
		outline: 2px solid var(--corn);
		outline-offset: 1px;
		border-color: transparent;
	}
	.table-wrap {
		overflow-x: auto;
		border: 1px solid var(--border);
		border-radius: var(--radius);
		box-shadow: var(--shadow);
		background: var(--surface);
	}
	table {
		font-size: 0.9rem;
	}
	th,
	td {
		padding: 0.55rem 0.8rem;
		text-align: left;
		border-bottom: 1px solid var(--border);
		white-space: nowrap;
	}
	th {
		background: var(--surface-2);
		cursor: pointer;
		user-select: none;
		font-weight: 600;
		font-size: 0.82rem;
		letter-spacing: 0.02em;
		color: var(--text-muted);
		position: sticky;
		top: 0;
	}
	th.active {
		color: var(--terracotta);
	}
	.arrow {
		font-size: 0.7rem;
	}
	.num {
		text-align: right;
		font-variant-numeric: tabular-nums;
	}
	tbody tr:nth-child(even) td {
		background: color-mix(in srgb, var(--surface-2) 45%, transparent);
	}
	tbody tr:last-child td {
		border-bottom: none;
	}
	tbody tr:hover td {
		background: color-mix(in srgb, var(--corn) 12%, transparent);
	}
	/* colorscale cells set their own inline background — don't let hover/zebra override */
	tbody td[style] {
		background-clip: padding-box;
	}
</style>
