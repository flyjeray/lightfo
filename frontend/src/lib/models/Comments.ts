import type { User } from "./User"

export type Comment = {
  id: number
  text: string
  post: number
  post_title: string
  user: User
  created_at: Date
}