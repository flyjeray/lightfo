<script lang="ts">
	import { API } from '$lib/api/index.js';
	import type { Comment } from '$lib/models/Comments.js';
	import type { Pagination } from '$lib/models/Pagination.js';
	import type { Post } from '$lib/models/Post.js';
	import { onMount } from 'svelte';

  export let data;

  let postData: Post | null = null;

  let comments: Comment[] = [];
  let commentPage = 1;
  let commentPagination: Pagination | null = null;

  const getComments = async () => {
    const response = await API.comments.getForPost(parseInt(data.slug), commentPage);

    if (response.status === 200) {
      comments = [...comments, ...response.data.comments];
      commentPagination = response.data.pagination;
    }
  }

  const nextPage = () => {
    commentPage++; 
  }

  const fetchData = async () => {
    const response = await API.posts.getSingle(parseInt(data.slug))

    if (response.status === 200) {
      postData = response.data;
      getComments();
    }
  }

  onMount(() => {
    fetchData()
  })
</script>

<section class="w-1/2 mx-auto flex flex-col gap-6">
  {#if postData}
    <div class="flex flex-col gap-2 shadow-md p-4 rounded-xl bg-gray-50">
      <h1>{postData.title}</h1>
      <small>{postData.created_at}</small>
      <p>{postData.text}</p>
    </div>
    <p>{postData.comment_amount} {postData.comment_amount > 1 ? 'comments' : 'comment'}</p>
    {#each comments as comment}
      <div class="flex flex-col gap-2 shadow-md p-4 rounded-xl bg-gray-50">
        <p>{comment.user.username}</p>
        <p>{comment.text}</p>
      </div>
    {/each}
    {#if commentPagination && !commentPagination.is_last}
		  <button class="rounded-xl" on:click={nextPage}>Load more</button>
    {/if}
  {/if}
</section>