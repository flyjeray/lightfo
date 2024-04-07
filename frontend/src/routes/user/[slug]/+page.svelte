<script lang="ts">
	import { API } from '$lib/api';
	import { onMount } from 'svelte';
	import feedStore from '$lib/store/feedStore';

	import type { PostWithNamedOwner } from '$lib/models/Post';
	import type { Pagination } from '$lib/models/Pagination';
	import type { Comment } from '$lib/models/Comments';

	import PostCard from '$lib/components/Feed/Post/index.svelte';
	import CommentCard from '$lib/components/Post/Comment/index.svelte';

  export let data;

	let feed: PostWithNamedOwner[] = [];
	let feedPagination: Pagination | null;

	let comments: Comment[] = [];
	let commentsPagination: Pagination | null = null;

  let username: string | null = null;

	const tabs = ['POSTS', 'COMMENTS'] as const;
	let activeTab: typeof tabs[number] = 'POSTS';

	feedStore.subscribe(data => {
		feed = data.feed;
		feedPagination = data.pagination
	});

	let feedPage = 1;
	let commentsPage = 1;

	const fetchFeed = (firstLoad: boolean) => {
		API.posts.getMany(feedPage, parseInt(data.slug)).then((response) => {
			feedStore.update(state => ({ 
				...state,
				feed: firstLoad ? response.data.posts : [...state.feed, ...response.data.posts], 
				feedPagination: response.data.pagination
			}))
		});
	};

	const fetchComments = () => {
		API.comments.getForUser(parseInt(data.slug), commentsPage).then((response) => {
			comments = [...comments, ...response.data.comments];
			commentsPagination = response.data.pagination;
		})
	}

  const fetchUser = () => {
    API.users.get(parseInt(data.slug)).then((response) => {
      username = response.data.username;
    })
  }

	const nextPageFeed = () => {
		if (feedPagination && !feedPagination.is_last) {
			feedPage++;
			fetchFeed(false);
		}
	};

	const nextPageComments = () => {
		if (commentsPagination && !commentsPagination.is_last) {
			commentsPage++;
			fetchComments();
		}
	};

	const onCommentDeleted = (id: number) => {
		comments = comments.filter(c => c.id !== id)
	}

	onMount(() => {
		fetchFeed(true);
		fetchComments();
    fetchUser();
	});
</script>

<section class="w-1/2 mx-auto flex flex-col gap-6">
  {#if username}
    <h1 class="text-4xl mb-6 font-bold">{username}</h1>
		<div class="flex flex-row gap-2">
			{#each tabs as tab}
				<button 
					class={`border-0 border-b-2 ${activeTab == tab ? 'border-emerald-400' : 'border-black'}`} 
					on:click={() => activeTab = tab}
				>
					{tab}
				</button>
			{/each}
		</div>
		{#if activeTab == 'POSTS'}
			{#each feed as post}
				<PostCard data={post} />
			{/each}
			{#if feedPagination && !feedPagination.is_last}
				<button class="rounded-xl" on:click={nextPageFeed}>Load more</button>
			{/if}
		{:else if activeTab == 'COMMENTS'}
			{#each comments as comment}
				<CommentCard 
					data={comment} 
					showPost={true} 
					showUser={false}
					onDelete={onCommentDeleted} 
				/>
			{/each}
			{#if commentsPagination && !commentsPagination.is_last}
				<button class="rounded-xl" on:click={nextPageComments}>Load more</button>
			{/if}
		{/if}
  {/if}
</section>
