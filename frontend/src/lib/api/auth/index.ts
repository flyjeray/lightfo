import { AUTH_TOKEN_LOCALSTORAGE_PATH, axiosInstance } from "..";

const prefix = '/auth'

type Creds = {
  name: string;
  pw: string;
}

type SignInResponse = {
  access_token: string, 
  token_type: string,
}

type GetCurrentResponse = {
  id: number;
  username: string;
  hashed_pw: string;
}

export const signup = (creds: Creds) => axiosInstance.post<Creds>(`${prefix}/signup`, creds);

export const signin = async (creds: Creds) => {
  const response = await axiosInstance.post<SignInResponse>(`${prefix}/signin`, creds);

  if (response.status === 200) {
    window.localStorage.setItem(AUTH_TOKEN_LOCALSTORAGE_PATH, response.data.access_token);
  }
  
  return response;
}

export const current = () => axiosInstance.get<GetCurrentResponse>(`${prefix}/current`);