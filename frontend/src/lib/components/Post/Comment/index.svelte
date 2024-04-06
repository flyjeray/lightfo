<script lang="ts">
	import type { Comment } from "$lib/models/Comments";

  export let data: Comment;
</script>

<div class="flex flex-col gap-2 shadow-md p-4 rounded-xl bg-gray-50">
  <a href={`/user/${data.user.id}`}>{data.user.username}</a>
  <small>{new Date(data.created_at).toLocaleString()}</small>
  <p>{data.text}</p>
</div>