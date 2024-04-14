<script lang="ts">
	import { API } from "$lib/api";
	import type { Comment } from "$lib/models/Comments";
	import type { Pagination } from "$lib/models/Pagination";
	import { onMount } from "svelte";

  import CommentCard from './Comment/index.svelte';
  import CreateCommentBlock from '../CreateComment/index.svelte';
	import authStore from "$lib/store/authStore";

  export let postID: number;
  export let parentID: number | undefined;
  export let depth: number;
  export let passedAmountOfCommentsAsTrigger: number | undefined = undefined;
  
  let comments: Comment[] = [];
  let commentPage = 1;
  let commentPagination: Pagination | null = null;
  let expanded: Record<number, boolean> = {};
  let commentToReply: number | null = null;
  let isMounted = false;

  let userToken: string | null = null;
  authStore.subscribe(data => userToken = data.token);

  const getComments = async (clearData: boolean) => {
    const response = await API.comments.getForPost({
      post_id: postID, 
      page: commentPage,
      parent_comment_id: parentID,
    });

    if (response.status === 200) {
      if (clearData) {
        comments = response.data.comments
      } else {
        comments = [...comments, ...response.data.comments];
      }
      commentPagination = response.data.pagination;
    }
  }

  const onReplyCreated = (data: Comment) => {
    if (data.parent_comment) {
      const i = comments.findIndex(c => c.id === data.parent_comment);
      if (i !== -1) {
        comments[i].children_comment_amount = comments[i].children_comment_amount + 1;
      }
      commentToReply = null;
    }
  }

  const onCommentDeleted = (id: number) => {
    comments = comments.filter(c => c.id !== id)
  }

  const nextPage = () => {
    commentPage++; 
    getComments(false)
  }

  $: if (passedAmountOfCommentsAsTrigger) getComments(true);

  onMount(() => {
    if (!passedAmountOfCommentsAsTrigger) {
      getComments(true)
    }
  })
</script>

<div class="flex flex-row">
  {#if depth > 0}
    <div class="w-4 border-l border-slate-300"></div>
  {/if}
  <div class="flex-1">
    {#each comments as comment}
      <div class="mb-2">
        <CommentCard 
          data={comment} 
          onDelete={onCommentDeleted}
          isExpanded={expanded[comment.id]}
          onExpand={() => expanded[comment.id] = (expanded[comment.id] == undefined ? true : !expanded[comment.id])}
          isReplySelected={commentToReply == comment.id}
          onReplySelect={() => commentToReply = commentToReply == comment.id ? null : comment.id}
        />
      </div>
      {#if commentToReply == comment.id && !!userToken}
        <div class="pb-6">
          <CreateCommentBlock 
            postID={postID}
            parentCommentID={comment.id}
            addComment={onReplyCreated}
          />
        </div>
      {/if}
      {#if expanded[comment.id]}
        <svelte:self 
          postID={postID} 
          parentID={comment.id} 
          depth={depth + 1}
          passedAmountOfCommentsAsTrigger={comment.children_comment_amount}
        />
      {/if}
    {/each}
    {#if commentPagination && !commentPagination.is_last}
      <button 
        class="w-fit border-slate-300 p-2 rounded-md my-4" 
        on:click={nextPage}
      >
        <p class="text-sm">Load more</p>
      </button>
    {/if}
  </div>
</div>