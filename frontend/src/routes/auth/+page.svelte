<script lang="ts">
	import { API } from '$lib/api';

	let name: string = '';
	let pw: string = '';

	const signIn = () => {
		API.auth
			.signin({ name, pw })
			.then((data) => {
				console.log('Sign in successful:', data);
			})
			.catch((err) => {
				console.error('Error:', err);
			});
	};

	const signUp = () => {
		API.auth
			.signup({ name, pw })
			.then((data) => {
				console.log('Sign up successful:', data);
			})
			.catch((err) => {
				console.error('Error:', err);
			});
	};

	const current = () => {
		API.auth
			.current()
			.then((data) => {
				console.log('Current user:', data);
			})
			.catch((err) => {
				console.error('Error:', err);
			});
	};
</script>

<section>
	<input bind:value={name} placeholder="Username" />
	<input bind:value={pw} placeholder="Password" type="password" />
	<button on:click={signIn}>Sign In</button>
	<button on:click={signUp}>Sign Up</button>
	<button on:click={current}>Current</button>
</section>
