<script lang="ts">
	import { API } from "$lib/api";
	import type { Post } from "$lib/models/Post";

  let title = '';
  let text = '';

  export let onCreated: (post: Post) => void;

  const send = () => {
    if (title && text) {
      API.posts.create(title, text).then(response => onCreated(response.data));
    }
  }
</script>

<div class="flex flex-col gap-2 p-4 shadow-xl rounded-xl bg-gray-100">
  <input bind:value={title} placeholder="Title" class="w-full h-8 rounded-t-xl p-2" />
  <textarea bind:value={text} placeholder="Content" class="w-full h-32 rounded-b-xl p-2" />
  <button class="ml-auto px-4 py-2" on:click={send}>Send</button>
</div>