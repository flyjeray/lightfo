<script lang="ts">
	import { API } from '$lib/api/index.js';
	import CommentCard from '$lib/components/Post/Comment/index.svelte';
  import PostContent from '$lib/components/Post/Content/index.svelte';
  import CreateComment from '$lib/components/Post/CreateComment/index.svelte';
	import type { Comment } from '$lib/models/Comments.js';
	import type { Pagination } from '$lib/models/Pagination.js';
	import type { Post } from '$lib/models/Post.js';
	import { onMount } from 'svelte';
  import authStore from '$lib/store/authStore';

  let localToken: string | null = null;
	authStore.subscribe(data => localToken = data.token)

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
    getComments()
  }

  const fetchData = async () => {
    const response = await API.posts.getSingle(parseInt(data.slug))

    if (response.status === 200) {
      postData = response.data;
      getComments();
    }
  }

  const onCommentDeleted = (id: number) => {
    comments = comments.filter(c => c.id !== id)
  }

  onMount(() => {
    fetchData()
  })
</script>

<section class="w-1/2 mx-auto flex flex-col gap-6">
  {#if postData}
    <PostContent data={postData} />
    <p>{postData.comment_amount} {postData.comment_amount != 1 ? 'comments' : 'comment'}</p>
    {#if localToken}
      <CreateComment 
        postID={parseInt(data.slug)} 
        addComment={newComment => comments = [newComment, ...comments]}
      />
    {/if}
    {#each comments as comment}
      <CommentCard data={comment} onDelete={onCommentDeleted} />
    {/each}
    {#if commentPagination && !commentPagination.is_last}
		  <button class="rounded-xl" on:click={nextPage}>Load more</button>
    {/if}
  {/if}
</section>