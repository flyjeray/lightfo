<script lang="ts">
	import { API } from '$lib/api';
	import store from '$lib/store/authStore';
	
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

<div class="flex full:flex-col phone:flex-row gap-4 full:w-1/6 justify-center items-center">
	{#if localToken && localName}
		<p class="text-center">Logged in as {localName}</p>
		<button class="w-1/2" on:click={signOut}>Sign Out</button>
	{:else}
		<div 
			class="flex full:flex-row phone:flex-col justify-between gap-2 w-full"
		>
			<input class="rounded full:w-1/2 phone:w-full p-1" bind:value={nameInput} placeholder="Username" />
			<input class="rounded full:w-1/2 phone:w-full p-1" bind:value={pwInput} placeholder="Password" />
		</div>
		<div class="flex flex-row full:flex-row phone:flex-col justify-between gap-2 w-full">
			{#if action === 'signin'}
				<button class="rounded full:w-1/2 phone:w-full" on:click={signIn}>Sign In</button>
				<button class="full:w-1/2 phone:w-full border-0 border-b" on:click={() => { action = 'signup' }}>Not registered?</button>
			{:else}
				<button class="rounded full:w-1/2 phone:w-full" on:click={signUp}>Sign Up</button>
				<button class="full:w-1/2 phone:w-full border-0 border-b" on:click={() => { action = 'signin' }}>Already registered?</button>
			{/if}
		</div>
	{/if}
</div>
