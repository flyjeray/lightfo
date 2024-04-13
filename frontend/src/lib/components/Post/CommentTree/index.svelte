<script lang="ts">
	import { API } from "$lib/api";
	import type { Comment } from "$lib/models/Comments";
	import type { Pagination } from "$lib/models/Pagination";
	import { onMount } from "svelte";
  import CommentCard from './Comment/index.svelte';

  export let postID: number;
  export let parentID: number | undefined;
  export let depth: number;
  
  let comments: Comment[] = [];
  let commentPage = 1;
  let commentPagination: Pagination | null = null;
  let expanded: Record<number, boolean> = {};

  const getComments = async () => {
    const response = await API.comments.getForPost({
      post_id: postID, 
      page: commentPage,
      parent_comment_id: parentID,
    });

    if (response.status === 200) {
      comments = [...comments, ...response.data.comments];
      commentPagination = response.data.pagination;
    }
  }

  const onCommentDeleted = (id: number) => {
    comments = comments.filter(c => c.id !== id)
  }

  const nextPage = () => {
    commentPage++; 
    getComments()
  }

  onMount(() => {
    getComments()
  })
</script>

<div class="flex flex-row">
  {#each {length: depth > 0 ? 1 : 0} as _, i}
    <div class="w-4 border-l border-slate-300"></div>
  {/each}
  <div class="flex-1">
    {#each comments as comment}
      <div class="mb-2">
        <CommentCard 
          data={comment} 
          onDelete={onCommentDeleted}
          isExpanded={expanded[comment.id]}
          onExpand={() => expanded[comment.id] = (expanded[comment.id] == undefined ? true : !expanded[comment.id])}
        />
      </div>
      {#if expanded[comment.id]}
        <svelte:self postID={postID} parentID={comment.id} depth={depth + 1} />
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