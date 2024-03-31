type Post = {
  id: number
  title: string
  text: string
  created_at: Date
};

export type PostWithNamedOwner = Post & {
  owner: string;
}

export type PostWithIDdOwner = Post & {
  owner: number;
}