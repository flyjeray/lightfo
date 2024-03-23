import { AUTH_TOKEN_LOCALSTORAGE_PATH, axiosInstance } from "..";
import store from "../../../store/store";

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
  hashed_pw: string;
}

export const current = () => axiosInstance.get<GetCurrentResponse>(`${prefix}/current`);

export const signup = async (creds: Creds) => {
  const response = await axiosInstance.post<SignResponse>(`${prefix}/signup`, creds);
  
  if (response.status === 200) {
    window.localStorage.setItem(AUTH_TOKEN_LOCALSTORAGE_PATH, response.data.access_token);
    store.set({ token: response.data.access_token, name: response.data.name })
  }
  
  return response;
};

export const signin = async (creds: Creds) => {
  const response = await axiosInstance.post<SignResponse>(`${prefix}/signin`, creds);

  if (response.status === 200) {
    window.localStorage.setItem(AUTH_TOKEN_LOCALSTORAGE_PATH, response.data.access_token);
    store.set({ token: response.data.access_token, name: response.data.name })
  }
  
  return response;
}

export const signout = () => {
  window.localStorage.removeItem(AUTH_TOKEN_LOCALSTORAGE_PATH);
  store.set({ token: null, name: null })
}
