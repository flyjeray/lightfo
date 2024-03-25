<script lang="ts">
	import { API } from '$lib/api/index.js';
	import type { Post } from '$lib/models/Post.js';
	import { onMount } from 'svelte';

  export let data;

  let postData: Post | null = null;

  const fetchData = async () => {
    const response = await API.posts.getSingle(parseInt(data.slug))

    if (response.status === 200) {
      postData = response.data;
    }
  }

  onMount(() => {
    fetchData()
  })
</script>

{#if postData}
  <h1>{postData.title}</h1>
  <small>{postData.created_at}</small>
  <p>{postData.text}</p>
{/if}