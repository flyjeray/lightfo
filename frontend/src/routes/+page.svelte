<script lang="ts">
  import { API } from '$lib/api'
	import { onMount } from 'svelte';

  import type { Post } from '$lib/models/Post';
	import type { Pagination } from '$lib/models/Pagination';

  let page = 1;
  let posts: Post[] = [];
  let pagination: Pagination | null = null;

  const fetchData = () => {
    API.posts.getMany(page).then((response) => {
      posts = [...posts, ...response.data.posts];
      pagination = response.data.pagination;
    })
  }

  const nextPage = () => {
    if (pagination && !pagination.is_last) {
      page++;
      fetchData();
    }
  }

  onMount(() => {
    fetchData();
  });
</script>

<section class="flex flex-col gap-6">
  {#each posts as { id, title, text, created_at }}
    <div class="flex flex-col gap-2">
      <a href={`/post/${id}`}>
        <h2>{title}</h2>
      </a>
      <small>{created_at}</small>
      <p>{text}</p>
    </div>
  {/each}
  {#if (pagination && !pagination.is_last)}
    <button on:click={nextPage}>Load more</button>
  {/if}
</section>
