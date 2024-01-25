<script lang="ts">
  import { API } from "$lib/api";
	import type { APITestValue } from "$lib/api/test";

  let values: APITestValue[] = [];
  let input = '';
  let error: string | null = null;

  const getValues = async () => {
    console.log('getValues start')
    const response = await API.test.get();

    if (response.status === 200) {
      console.log('getValues success end');
      values = response.data;
      error = null;
    } else {
      console.log('getValues error end');
      error = `Error ${response.status}`;
    }
  }

  const postValue = async () => {
    if (input === '') {
      error = 'Please, enter some text first';
      return;
    }

    const response = await API.test.post(input);

    if (response.status === 200) {
      error = null;
    } else {
      error = `Error ${response.status}`;
    }
  }
</script>

<section>
  <h1>LightFo</h1>

  <button on:click={getValues}>Get Values</button>
  <input type="text" placeholder="Text for new value" bind:value={input} />
  <button on:click={postValue}>Post Value</button>

  {#if error}
    <p style="color: red">{error}</p>
  {/if}

  {#each values as { id, value }}
    <p>{id}: {value}</p>
  {/each}
</section>
