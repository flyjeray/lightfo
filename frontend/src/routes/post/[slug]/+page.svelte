<script lang="ts">
	import { API } from '$lib/api/index.js';
	import CommentTree from '$lib/components/Post/CommentTree/index.svelte';
  import PostContent from '$lib/components/Post/Content/index.svelte';
  import CreateComment from '$lib/components/Post/CreateComment/index.svelte';
	import type { Comment } from '$lib/models/Comments.js';
	import type { Pagination } from '$lib/models/Pagination.js';
	import type { Post } from '$lib/models/Post.js';
	import { onMount } from 'svelte';
  import authStore from '$lib/store/authStore';

  type CommentWithChildren = {
    data: Comment;
    children: Comment[];
  }

  let localToken: string | null = null;
	authStore.subscribe(data => localToken = data.token)

  export let data;

  let postData: Post | null = null;

  let comments: Comment[] = [];

  const fetchData = async () => {
    const response = await API.posts.getSingle(parseInt(data.slug))

    if (response.status === 200) {
      postData = response.data;
    }
  }

  onMount(() => {
    fetchData()
  })
</script>

<section class="tablet:w-1/2 phone:w-full mx-auto flex flex-col gap-6">
  {#if postData}
    <PostContent data={postData} />
    <p>{postData.comment_amount} {postData.comment_amount != 1 ? 'comments' : 'comment'}</p>
    {#if localToken}
      <CreateComment 
        postID={parseInt(data.slug)} 
        addComment={newComment => comments = [newComment, ...comments]}
      />
    {/if}
    <CommentTree postID={parseInt(data.slug)} depth={1} parentID={undefined} />
  {/if}
</section>