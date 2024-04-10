<script lang="ts">
	import { API } from "$lib/api";
	import type { Comment } from "$lib/models/Comments";

  export let postID: number;
  export let addComment: (data: Comment) => void;

  let text = '';

  const send = () => {
    if (text) {
      API.comments.add({ post_id: postID, text }).then(res => {
        addComment(res.data)
      })
    }
  }
</script>

<div class="flex flex-col gap-2 p-4 shadow-xl rounded-xl bg-gray-100">
  <textarea bind:value={text} placeholder="Add comment" class="w-full h-32 rounded-xl p-2" />
  <button class="ml-auto px-4 py-2" on:click={send}>Send</button>
</div>