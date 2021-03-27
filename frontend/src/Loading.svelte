<script lang="ts">
    import Fa from 'svelte-fa'
    import { faSpinner } from '@fortawesome/free-solid-svg-icons'
</script>

<style>
    .rotate {
        text-align: center;
        animation: rotation 3s infinite linear;
    }

    @keyframes rotation {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>

<div class="rotate">
    <Fa icon={faSpinner} />
</div>
