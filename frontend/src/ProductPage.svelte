<script lang="ts">
    import axios from 'axios';

	import Loading from './Loading.svelte';
    import Pagination from './Pagination.svelte';
    import ProductInfo from './ProductInfo.svelte';
    import SearchBar from './SearchBar.svelte';

    import type { ApiResponse } from './Api';
    import { Product } from './Product';

    const itemsPerPage = 12;

	let currentPage = 1;
	let numberOfItems = 0;
    let search = '';

    let products: Product[] = [];
    let loading = true;

    function loadData() {
        loading = true;

        axios.get<ApiResponse>(`${process.env.API_HOST}/api/products/`, {
            params: {
                search,
                page: currentPage,
            },
        })
        .then(response => {
            numberOfItems = response.data.count;
            products = response.data.results.map(product => new Product(product.name, product.product_number));
        })
        .finally(() => {
            loading = false;
        });
    }

    loadData();
</script>

<style>
    .product-container {
        display: grid;

        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    }
</style>

<SearchBar bind:search on:change="{() => loadData()}" />

{#if loading}
    <Loading />
{:else}
    <div class="product-container">
    {#each products as product}
        <ProductInfo {product} />
    {/each}
    </div>
{/if}

<Pagination bind:currentPage {numberOfItems} {itemsPerPage} on:change="{() => loadData()}" />
