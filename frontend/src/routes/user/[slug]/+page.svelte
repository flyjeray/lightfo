<script lang="ts">
	import { API } from '$lib/api';
	import { onMount } from 'svelte';

	import type { Post } from '$lib/models/Post';
	import type { Pagination } from '$lib/models/Pagination';
	import type { Comment } from '$lib/models/Comments';

	import PostCard from '$lib/components/Feed/Post/index.svelte';
	import CommentCard from '$lib/components/Post/CommentTree/Comment/index.svelte';

  export let data;

	let posts: Post[] = [];
	let postsPagination: Pagination | null;

	let comments: Comment[] = [];
	let commentsPagination: Pagination | null = null;

  let username: string | null = null;

	const tabs = ['POSTS', 'COMMENTS'] as const;
	let activeTab: typeof tabs[number] = 'POSTS';

	let feedPage = 1;
	let commentsPage = 1;

	const fetchFeed = () => {
		API.posts.getMany(feedPage, parseInt(data.slug)).then((response) => {
			posts = [...posts, ...response.data.posts];
			postsPagination = response.data.pagination;
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
		if (postsPagination && !postsPagination.is_last) {
			feedPage++;
			fetchFeed();
		}
	};

	const nextPageComments = () => {
		if (commentsPagination && !commentsPagination.is_last) {
			commentsPage++;
			fetchComments();
		}
	};

	const onPostDeleted = (id: number) => posts = posts.filter(p => p.id != id)

	const onCommentDeleted = (id: number) => comments = comments.filter(c => c.id !== id)

	onMount(() => {
		fetchFeed();
		fetchComments();
    fetchUser();
	});
</script>

<section class="tablet:w-1/2 phone:w-full mx-auto flex flex-col gap-6">
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
			{#each posts as post}
				<PostCard 
					data={post}
					onDelete={onPostDeleted}
				/>
			{/each}
			{#if postsPagination && !postsPagination.is_last}
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
