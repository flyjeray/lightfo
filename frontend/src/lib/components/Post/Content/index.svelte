<script lang="ts">
	import type { Post } from "$lib/models/Post";

  export let data: Post;
</script>

<div class="flex flex-col gap-2 shadow-md p-4 rounded-xl bg-gray-50">
  <h1>{data.title}</h1>
  <small>{data.created_at}</small>
  <p>{data.text}</p>
</div>