<script lang="ts">
	import { API } from '$lib/api';
	import type { PostWithNamedOwner } from '$lib/models/Post';
	import authStore from '$lib/store/authStore';

	export let data: PostWithNamedOwner;

	let id: number | null = null;
	authStore.subscribe(data => id = data.id)

	const deletePost = (e: MouseEvent & { currentTarget: EventTarget & HTMLButtonElement }) => {
		e.stopPropagation()
		e.preventDefault()
		if (confirm(`Are you sure you want to delete post "${data.title}"?`)) {
			API.posts.delete(data.id)
		}
	}
</script>

<a href={`/post/${data.id}`}>
	<div class="flex flex-col gap-2 shadow-md p-4 hover:shadow-xl rounded-xl bg-gray-50">
		<div class="flex flex-row justify-between">
			<h2>{data.title}</h2>
			{#if data.owner == id}
				<button class="z-20 hover:bg-gray-300" on:click={e => deletePost(e)}>Delete</button>
			{/if}
		</div>
		<small>
			{new Date(data.created_at).toLocaleString()} by <a class="underline" href={`/user/${data.owner}`}>{data.owner_name}</a>
		</small>
		<p>{data.text}</p>
		{#if data.comment_amount > 0}
			<small>{data.comment_amount} {data.comment_amount > 1 ? 'comments' : 'comment'}</small>
		{/if}
	</div>
</a>
