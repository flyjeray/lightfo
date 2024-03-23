<script>
	import Auth from '../components/Header/Auth/index.svelte';
</script>

<section>
	<Auth />
</section>

<style lang="postcss">
	:global(html) {
		background-color: theme(colors.blue.100);
	}
	:global(p, h1, button) {
		color: black;
	}
	:global(button) {
		background-color: theme(colors.white);
	}
</style>
