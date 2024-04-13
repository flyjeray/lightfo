<script lang="ts">
	import { API } from '$lib/api';
	import { onMount } from 'svelte';
	import authStore from '$lib/store/authStore';

	import type { Post } from '$lib/models/Post';
	import type { Pagination } from '$lib/models/Pagination';

	import PostCard from '$lib/components/Feed/Post/index.svelte';
	import CreatePost from '$lib/components/Feed/CreatePost/index.svelte';

	let localToken: string | null;
	let posts: Post[] = [];
	let pagination: Pagination | null;

	authStore.subscribe(data => localToken = data.token)

	let page = 1;

	const fetchData = () => {
		API.posts.getMany(page).then((response) => {
			posts = [...posts, ...response.data.posts];
			pagination = response.data.pagination;
		});
	};

	const nextPage = () => {
		if (pagination && !pagination.is_last) {
			page++;
			fetchData();
		}
	};

	const onPostDeleted = (id: number) => posts = posts.filter(p => p.id !== id);
	
	const onPostAdded = (data: Post) => posts = [data, ...posts];

	onMount(() => {
		fetchData();
	});
</script>

<section class="tablet:w-1/2 phone:w-full mx-auto flex flex-col gap-6">
	{#if localToken}
		<CreatePost
			onCreated={onPostAdded}
		/>
	{/if}
	{#each posts as post}
		<PostCard 
			data={post}
			onDelete={onPostDeleted}
		/>
	{/each}
	{#if pagination && !pagination.is_last}
		<button class="rounded-xl" on:click={nextPage}>Load more</button>
	{/if}
</section>
