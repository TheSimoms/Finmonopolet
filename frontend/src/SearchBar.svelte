<script lang="ts">
    export let search: string;
</script>

<style>
    .search-bar {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;

        margin-top: 1.25em;
        margin-bottom: 2em;
    }
</style>

<input class="search-bar" placeholder="Søk…" bind:value={search} on:change />
