<script>
	import '../app.css';
	import store from '../store/store';
	import Header from '../components/Header/index.svelte';
	import { onMount } from 'svelte';
	import { API, AUTH_TOKEN_LOCALSTORAGE_PATH } from '$lib/api';

	const { token } = $store;

	onMount(() => {
		if (window.localStorage.getItem(AUTH_TOKEN_LOCALSTORAGE_PATH) && !token) {
			API.auth.current();
		}
	})
</script>

<Header />
<div class="p-6">
	<slot />
</div>

<style lang="postcss">
	:global(button, input) {
		border: 1px solid black;
	}
</style>
