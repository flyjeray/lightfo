<script>
	import Auth from './Auth/index.svelte';
</script>

<header class="fixed w-full flex tablet:flex-row phone:flex-col justify-between border-b-2 py-2 px-6 bg-gray-50">
	<a class="font-bold text-xl phone:mx-auto phone:my-4 tablet:mx-0 tablet:my-auto" href="/">
		<h1>Lightfo</h1>
	</a>
	<Auth />
</header>
