import type { User } from "$lib/models/User";
import { axiosInstance } from ".."

const prefix = '/users';

export class UserAPI {
  static get = (id: number) => axiosInstance.get<User>(`${prefix}/${id}`);
}