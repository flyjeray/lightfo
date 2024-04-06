export type Post = {
  id: number
  title: string
  text: string
  created_at: Date
  owner: number
  comment_amount: number
};

export type PostWithNamedOwner = Post & {
  owner_name: string;
}