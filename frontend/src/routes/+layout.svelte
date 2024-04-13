<script>
	import '../app.css';
	import store from '$lib/store/authStore';
	import Header from '$lib/components/Header/index.svelte';
	import { onMount } from 'svelte';
	import { API, AUTH_TOKEN_LOCALSTORAGE_PATH } from '$lib/api';

	const { token } = $store;

	onMount(() => {
		if (window.localStorage.getItem(AUTH_TOKEN_LOCALSTORAGE_PATH) && !token) {
			API.auth.current();
		}
	});
</script>

<Header />
<div class="p-6 tablet:pt-36 phone:pt-48 min-h-screen">
	<slot />
</div>

<style lang="postcss">
	:global(button, input, textarea) {
		border: 1px solid black;
	}
</style>
