import { axiosInstance } from "..";
import type { Pagination } from "$lib/models/Pagination";
import type { PostWithIDdOwner, PostWithNamedOwner } from "$lib/models/Post";
import feedStore from "$lib/store/feedStore";
import authStore from "$lib/store/authStore";
import { get } from "svelte/store";

const prefix = '/posts';

type GetPostsResponse = {
  posts: PostWithNamedOwner[],
  pagination: Pagination;
}

export class PostsAPI {
  static getMany = async (page: number) => {
    const response = await axiosInstance.get<GetPostsResponse>(`${prefix}/`, { params: { page, perPage: 5 }});
  
    return response;
  }

  static getSingle = async (id: number) => {
    const response = await axiosInstance.get<PostWithNamedOwner>(`${prefix}/${id}`);
  
    return response;
  }

  static create = async (title: string, text: string) => {
    const response = await axiosInstance.post<PostWithIDdOwner>(`${prefix}/create`, { title, text });

    if (response.status == 201) {
      feedStore.update(state => ({
        ...state,
        feed: [{...response.data, owner: get(authStore).name || '' }, ...state.feed],
      }))
    }
  
    return response;
  }
}