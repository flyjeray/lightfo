<script lang="ts">
	import { API } from '$lib/api';
	import { onMount } from 'svelte';
	import feedStore from '$lib/store/feedStore';

	import type { PostWithNamedOwner } from '$lib/models/Post';
	import type { Pagination } from '$lib/models/Pagination';

	import PostCard from '$lib/components/Feed/Post/index.svelte';

  export let data;

	let feed: PostWithNamedOwner[] = [];
	let pagination: Pagination | null;

  let username: string | null = null;

	feedStore.subscribe(data => {
		feed = data.feed;
		pagination = data.pagination
	});

	let page = 1;

	const fetchFeed = (firstLoad: boolean) => {
		API.posts.getMany(page, parseInt(data.slug)).then((response) => {
			feedStore.update(state => ({ 
				...state,
				feed: firstLoad ? response.data.posts : [...state.feed, ...response.data.posts], 
				pagination: response.data.pagination
			}))
		});
	};

  const fetchUser = () => {
    API.users.get(parseInt(data.slug)).then((response) => {
      username = response.data.username;
    })
  }

	const nextPage = () => {
		if (pagination && !pagination.is_last) {
			page++;
			fetchFeed(false);
		}
	};

	onMount(() => {
		fetchFeed(true);
    fetchUser();
	});
</script>

<section class="w-1/2 mx-auto flex flex-col gap-6">
  {#if username}
    <h1 class="text-4xl mb-6 font-bold">{username}</h1>
    {#each feed as post}
      <PostCard data={post} />
    {/each}
    {#if pagination && !pagination.is_last}
      <button class="rounded-xl" on:click={nextPage}>Load more</button>
    {/if}
  {/if}
</section>
