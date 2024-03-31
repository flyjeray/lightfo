import type { Pagination } from '$lib/models/Pagination';
import type { PostWithNamedOwner } from '$lib/models/Post';
import { writable } from 'svelte/store';

export type FeedState = {
  feed: PostWithNamedOwner[];
  pagination: Pagination | null;
}

const initialState: FeedState = {
  feed: [],
  pagination: null,
};

const { subscribe, set, update } = writable<FeedState>(initialState);

export default {
  subscribe,
  set,
  update,
};
