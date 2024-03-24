import { axiosInstance } from "..";
import type { Pagination } from "../../../models/Pagination";
import type { Post } from "../../../models/Post";

const prefix = '/posts';

type GetPostsResponse = {
  posts: Post[],
  pagination: Pagination;
}

export const getMany = async (page: number) => {
  const response = await axiosInstance.get<GetPostsResponse>(`${prefix}/`, { params: { page, perPage: 5 }});

  return response;
}