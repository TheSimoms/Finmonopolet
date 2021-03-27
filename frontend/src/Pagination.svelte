<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatchEvent = createEventDispatcher();
	const range = (start: number, end: number) => Array.from({length: (1 + end - start)}, (_, k) => k + start);

	export let currentPage: number;
	export let numberOfItems: number;
    export let itemsPerPage: number;

    $: numberOfPages = Math.max(Math.ceil(numberOfItems / itemsPerPage), 1);
	$: pages = currentPage <= 6 ? 
		range(1, 10) : 
		(currentPage >= numberOfPages - 4 ? 
			range(numberOfPages - 9, numberOfPages) : 
			range(currentPage - 5, currentPage + 4));

	function changePage(newPage: number) {
		if (newPage !== currentPage) {
			if (newPage < 1) {
				newPage = 1;
			}

			if (newPage > numberOfPages) {
				newPage = numberOfPages;
			}

			currentPage = newPage;
			
			dispatchEvent('change', newPage);
		}
	}
</script>

<style>
	.pagination {
		text-align: center;
	}

	ul {
		display: inline-flex;
	}

	li {
		list-style: none;

		margin-left: -1px;
		padding: .5em 1em;

		background-color: #fff;
		border: 1px solid #dee2e6;
	}

	li:hover:not(.disabled) {
		background-color: #dee2e6;
		border: 1px solid #dee2e6;

		cursor: pointer;
	}

	li.disabled {
		color: #dee2e6;
	}

	li.current {
		color: #fff;
		background-color: #007bff;
		border-color: #007bff;
	}

	li:first-child {
		border-top-left-radius: .2em;
		border-bottom-left-radius: .2em;
	}

	li:last-child {
		border-top-right-radius: .2em;
		border-bottom-right-radius: .2em;
	}
</style>

{#if numberOfItems > itemsPerPage}
<div class="pagination">
	<ul>
		<li class:disabled="{currentPage === 1}" on:click="{() => changePage(1)}">&laquo;</li>
		<li class:disabled="{currentPage === 1}" on:click="{() => changePage(currentPage - 1)}">&lsaquo;</li>
		{#each pages as page}
			<li class:current="{currentPage === page}" on:click="{() => changePage(page)}">{page}</li>
		{/each}
		<li class:disabled="{currentPage === numberOfPages}" on:click="{() => changePage(currentPage + 1)}">&rsaquo;</li>
		<li class:disabled="{currentPage === numberOfPages}" on:click="{() => changePage(numberOfPages)}">&raquo;</li>
	</ul>
</div>
{/if}
