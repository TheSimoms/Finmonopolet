<script lang="ts">
    import type { Product } from './Product';

    export let product: Product;
</script>

<style>
    .product-info {
        text-align: center;
        margin: 0 .5em 1em .5em;
        max-width: 463.5px;

        box-sizing: border-box;
        border: 1px solid rgba(0, 0, 0, .125);
        border-radius: .25rem;

        padding: .5em .25em .5em .25em;
    }

    .product-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        max-height: 200px;
    }

    .product-name {
        margin-top: .25em;
        margin-bottom: .25em;
    }
</style>

<div class="product-info">
    <img class="product-image"
        src="https://bilder.vinmonopolet.no/cache/300x300-0/{product.productNumber}-1.jpg" 
        alt="{product.name}">

    <a class="product-name"
        href="http://www.vinmonopolet.no/vareutvalg/varedetaljer/sku-{product.productNumber}"
        target="_blank">
        {product.name}
    </a>
</div>
