import { AUTH_TOKEN_LOCALSTORAGE_PATH, axiosInstance } from "..";
import store from "$lib/store/authStore";

const prefix = '/auth'

type Creds = {
  name: string;
  password: string;
}

type SignResponse = {
  access_token: string, 
  token_type: string,
  name: string
}

type GetCurrentResponse = {
  id: number;
  username: string;
  access_token: string;
}

export class AuthAPI {
  static current = () => {
    axiosInstance.get<GetCurrentResponse>(`${prefix}/current`)
      .then(res => {
        store.set({ token: res.data.access_token, name: res.data.username })
      })
      .catch(() => {
        window.localStorage.removeItem(AUTH_TOKEN_LOCALSTORAGE_PATH);
        store.set({ token: null, name: null })
      });
  };

  static signup = async (creds: Creds) => {
    const response = await axiosInstance.post<SignResponse>(`${prefix}/signup`, creds);
    
    if (response.status === 200) {
      window.localStorage.setItem(AUTH_TOKEN_LOCALSTORAGE_PATH, response.data.access_token);
      store.set({ token: response.data.access_token, name: response.data.name })
    }
    
    return response;
  };

  static signin = async (creds: Creds) => {
    const response = await axiosInstance.post<SignResponse>(`${prefix}/signin`, creds);
  
    if (response.status === 200) {
      window.localStorage.setItem(AUTH_TOKEN_LOCALSTORAGE_PATH, response.data.access_token);
      store.set({ token: response.data.access_token, name: response.data.name })
    }
    
    return response;
  }

  static signout = () => {
    window.localStorage.removeItem(AUTH_TOKEN_LOCALSTORAGE_PATH);
    store.set({ token: null, name: null })
  }
}