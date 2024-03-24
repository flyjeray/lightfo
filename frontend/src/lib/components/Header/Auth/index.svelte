<script lang="ts">
	import { API } from '$lib/api';
	import store from '$lib/store/store';
	
	let localToken: string | null;
	let localName: string | null;

	store.subscribe(data => {
		localToken = data.token;
		localName = data.name;
	})

	let nameInput: string = '';
	let pwInput: string = '';
	let action: 'signin' | 'signup' = 'signin';

	const signIn = () => API.auth.signin({ name: nameInput, password: pwInput });

	const signUp = () => API.auth.signup({ name: nameInput, password: pwInput });

	const signOut = () => API.auth.signout()
</script>

<div class="flex flex-col gap-4 w-1/6 justify-center items-center">
	{#if localToken && localName}
		<p class="text-center">Logged in as {localName}</p>
		<button class="w-1/2" on:click={signOut}>Sign Out</button>
	{:else}
		<div class="flex flex-row justify-between gap-2 w-full">
			<input class="w-1/2" bind:value={nameInput} placeholder="Username" />
			<input class="w-1/2" bind:value={pwInput} placeholder="Password" />
		</div>
		<div class="flex flex-row justify-between gap-2 w-full">
			{#if action === 'signin'}
				<button class="w-1/2" on:click={signIn}>Sign In</button>
				<button class="w-1/2 border-0 border-b-2" on:click={() => { action = 'signup' }}>Or maybe Sign Up</button>
			{:else}
				<button class="w-1/2" on:click={signUp}>Sign Up</button>
				<button class="w-1/2 border-0 border-b-2" on:click={() => { action = 'signin' }}>Or maybe Sign In</button>
			{/if}
		</div>
	{/if}
</div>
