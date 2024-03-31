import { writable } from 'svelte/store';

type State = {
  token: string | null;
  name: string | null;
}

const initialState: State = {
  token: null,
  name: null,
};

const { subscribe, set } = writable<State>(initialState);

export default {
  subscribe,
  set,
};
