import axios from 'axios';

import { get, post } from './test';

export const axiosInstance = axios.create({
	baseURL: import.meta.env.VITE_API_URL
});

export const API = {
	test: {
		get,
		post
	}
};
