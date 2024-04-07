import { axiosInstance } from "..";
import type { Pagination } from "$lib/models/Pagination";
import type { Post } from "$lib/models/Post";

const prefix = '/posts';

type GetPostsResponse = {
  posts: Post[],
  pagination: Pagination;
}

export class PostsAPI {
  static getMany = async (page: number, uid?: number) => {
    const response = await axiosInstance.get<GetPostsResponse>(`${prefix}/`, { params: { page, perPage: 5, uid }});
  
    return response;
  }

  static getSingle = async (id: number) => {
    const response = await axiosInstance.get<Post>(`${prefix}/${id}`);
  
    return response;
  }

  static create = async (title: string, text: string) => {
    const response = await axiosInstance.post<Post>(`${prefix}/create`, { title, text });
  
    return response;
  }

  static delete = async (id: number) => {
    const response = await axiosInstance.delete(`${prefix}/delete`, { params: { id }});

    return response;
  }
}