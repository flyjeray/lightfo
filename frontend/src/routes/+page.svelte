<script lang="ts">
	import { API } from '$lib/api';
	import { onMount } from 'svelte';

	import type { Post } from '$lib/models/Post';
	import type { Pagination } from '$lib/models/Pagination';

	import PostCard from '$lib/components/Feed/Post/index.svelte';

	let page = 1;
	let posts: Post[] = [];
	let pagination: Pagination | null = null;

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

	onMount(() => {
		fetchData();
	});
</script>

<section class="w-1/2 mx-auto flex flex-col gap-6">
	{#each posts as post}
		<PostCard data={post} />
	{/each}
	{#if pagination && !pagination.is_last}
		<button class="rounded-xl" on:click={nextPage}>Load more</button>
	{/if}
</section>
