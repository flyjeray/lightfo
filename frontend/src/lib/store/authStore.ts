import { writable } from 'svelte/store';

type State = {
  token: string | null;
  id: number | null;
  name: string | null;
}

const initialState: State = {
  id: null,
  token: null,
  name: null,
};

const { subscribe, set } = writable<State>(initialState);

export default {
  subscribe,
  set,
};
