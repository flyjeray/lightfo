<script lang="ts">
	import { API } from '$lib/api';
	import { onMount } from 'svelte';
	import authStore from '$lib/store/authStore';
	import feedStore from '$lib/store/feedStore';

	import type { PostWithNamedOwner } from '$lib/models/Post';
	import type { Pagination } from '$lib/models/Pagination';

	import PostCard from '$lib/components/Feed/Post/index.svelte';
	import CreatePost from '$lib/components/Feed/CreatePost/index.svelte';

	let localToken: string | null;
	let feed: PostWithNamedOwner[] = [];
	let pagination: Pagination | null;

	authStore.subscribe(data => localToken = data.token)
	feedStore.subscribe(data => {
		feed = data.feed;
		pagination = data.pagination
	});

	let page = 1;

	const fetchData = (firstLoad: boolean) => {
		API.posts.getMany(page).then((response) => {
			feedStore.update(state => ({ 
				...state,
				feed: firstLoad ? response.data.posts : [...state.feed, ...response.data.posts], 
				pagination: response.data.pagination
			}))
		});
	};

	const nextPage = () => {
		if (pagination && !pagination.is_last) {
			page++;
			fetchData(false);
		}
	};

	onMount(() => {
		fetchData(true);
	});
</script>

<section class="w-1/2 mx-auto flex flex-col gap-6">
	{#if localToken}
		<CreatePost />
	{/if}
	{#each feed as post}
		<PostCard data={post} />
	{/each}
	{#if pagination && !pagination.is_last}
		<button class="rounded-xl" on:click={nextPage}>Load more</button>
	{/if}
</section>
