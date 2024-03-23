<script lang="ts">
	import { API } from '$lib/api';
	import store from '../../../store/store';
	
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

<div class="flex flex-col gap-4 w-1/4">
	{#if localToken && localName}
		<p>Logged in as {localName}</p>
		<button on:click={signOut}>Sign Out</button>
	{:else}
		<input bind:value={nameInput} placeholder="Username" />
		<input bind:value={pwInput} placeholder="Password" />
		{#if action === 'signin'}
			<button on:click={signIn}>Sign In</button>
			<button on:click={() => { action = 'signup' }}>Or maybe Sign Up</button>
		{:else}
			<button on:click={signUp}>Sign Up</button>
			<button on:click={() => { action = 'signin' }}>Or maybe Sign In</button>
		{/if}
	{/if}
</div>
