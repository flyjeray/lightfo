import type { User } from "./User"

export type Comment = {
  id: number
  text: string
  post: number
  user: User
  created_at: Date
}