import type { User } from "./User"

export type Comment = {
  id: number
  text: string
  post: number
  parent_comment?: number 
  post_title: string
  children_comment_amount: number
  user: User
  created_at: Date
}