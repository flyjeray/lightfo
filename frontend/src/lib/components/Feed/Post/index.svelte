<script lang="ts">
	import type { PostWithNamedOwner } from '$lib/models/Post';

	export let data: PostWithNamedOwner;
</script>

<a href={`/post/${data.id}`}>
	<div class="flex flex-col gap-2 shadow-md p-4 hover:shadow-xl rounded-xl bg-gray-50">
		<h2>{data.title}</h2>
		<small>{new Date(data.created_at).toLocaleString()} by {data.owner}</small>
		<p>{data.text}</p>
	</div>
</a>
