import { axiosInstance } from "..";
import type { Pagination } from "$lib/models/Pagination";
import type { Post } from "$lib/models/Post";

const prefix = '/posts';

type GetPostsResponse = {
  posts: Post[],
  pagination: Pagination;
}

export const getMany = async (page: number) => {
  const response = await axiosInstance.get<GetPostsResponse>(`${prefix}/`, { params: { page, perPage: 5 }});

  return response;
}

export const getSingle = async (id: number) => {
  const response = await axiosInstance.get<Post>(`${prefix}/${id}`);

  return response;
}