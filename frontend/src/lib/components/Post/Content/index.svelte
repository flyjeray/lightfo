<script lang="ts">
	import type { Post } from "$lib/models/Post";

  export let data: Post;
</script>

<div class="flex flex-col gap-2 shadow-md p-4 rounded-xl bg-gray-50">
  <h1 class="text-xl mb-2">{data.title}</h1>
  <small class="mb-6">{new Date(data.created_at).toLocaleString()} by <a class="underline" href={`/user/${data.owner}`}>{data.owner_name}</a></small>
  <p>{data.text}</p>
</div>