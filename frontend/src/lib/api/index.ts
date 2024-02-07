import axios from 'axios';

import { signin, signup, current } from './auth';

export const axiosInstance = axios.create({
	baseURL: import.meta.env.VITE_API_URL
});

export const AUTH_TOKEN_LOCALSTORAGE_PATH = 'lightfo_auth_token';

axiosInstance.interceptors.request.use(config => {
  const token = window.localStorage.getItem(AUTH_TOKEN_LOCALSTORAGE_PATH);
  config.headers["Authorization"] = `Bearer ${token}`;
  return config;
});

export const API = {
	auth: {
		signin,
		signup,
		current
	}
};
