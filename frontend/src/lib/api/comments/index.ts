import type { Comment } from "$lib/models/Comments";
import type { Pagination } from "$lib/models/Pagination";
import { axiosInstance } from "..";

const prefix = '/comments';

type GetCommentsResponse = {
  comments: Comment[];
  pagination: Pagination;
}

export class CommentsAPI {
  static getForPost = async (postID: number, page: number) => {
    const response = await axiosInstance.get<GetCommentsResponse>(`${prefix}/${postID}`, { params: { page, perPage: 5 }});
  
    return response;
  }

  static add = async (postID: number, text: string) => {
    const response = await axiosInstance.post<Comment>(`${prefix}/add/${postID}`, { text });

    return response;
  }

  static delete = async (id: number) => {
    const response = await axiosInstance.delete(`${prefix}/delete/${id}`);

    return response;
  }
}