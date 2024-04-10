import type { Comment } from "$lib/models/Comments";
import type { Pagination } from "$lib/models/Pagination";
import { axiosInstance } from "..";

const prefix = '/comments';

type GetCommentsPayload = {
  post_id: number
  parent_comment_id?: number
  page: number
  perPage?: number
}

type GetCommentsResponse = {
  comments: Comment[];
  pagination: Pagination;
}

type AddCommentPayload = {
  post_id: number
  parent_comment_id?: number
  text: string
}

export class CommentsAPI {
  static getForPost = async (payload: GetCommentsPayload) => {
    const response = await axiosInstance.get<GetCommentsResponse>(`${prefix}/`, { params: { perPage: 5, ...payload }});
  
    return response;
  }

  static getForUser = async (userID: number, page: number) => {
    const response = await axiosInstance.get<GetCommentsResponse>(`${prefix}/user/${userID}`, { params: { page, perPage: 5 }});
  
    return response;
  }

  static add = async (payload: AddCommentPayload) => {
    const response = await axiosInstance.post<Comment>(`${prefix}/add`, { ...payload });

    return response;
  }

  static delete = async (id: number) => {
    const response = await axiosInstance.delete(`${prefix}/delete/${id}`);

    return response;
  }
}