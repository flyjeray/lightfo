<script lang="ts">
	import { API } from "$lib/api";
	import type { Comment } from "$lib/models/Comments";
	import authStore from "$lib/store/authStore";

  export let data: Comment;
  export let onDelete: (id: number) => void;
  export let showPost: boolean = false;
  export let showUser: boolean = true;
  export let isExpanded: boolean = false;
  export let onExpand: (() => void) | undefined = undefined;

  let id: number | null;
  authStore.subscribe(newState => id = newState.id)

  const deleteComment = () => {
    if (confirm(`Are you sure you want to delete comment "${data.text}"?`)) {
      API.comments.delete(data.id).then(() => onDelete(data.id))
    }
  }
</script>

<div class="flex flex-col gap-2 shadow-md p-4 rounded-xl bg-gray-50">
  <div class="flex flex-row justify-between">
    {#if showUser}
      <a href={`/user/${data.user.id}`}>{data.user.username}</a>
    {/if}
    {#if showPost}
      <a href={`/post/${data.post}`}>{data.post_title}</a>
    {/if}
    {#if data.user.id == id}
      <button on:click={deleteComment}>Delete</button>
    {/if}
  </div>
  <small>{new Date(data.created_at).toLocaleString()}</small>
  <p>{data.text}</p>
  {#if onExpand && data.children_comment_amount > 0}
    <button on:click={onExpand}>{data.children_comment_amount} {data.children_comment_amount > 1 ? 'Replies' : 'Reply'} ({isExpanded ? 'Close' : 'Open'})</button>
  {/if}
</div>