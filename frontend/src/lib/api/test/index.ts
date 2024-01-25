import { axiosInstance } from '..';

const prefix = '/test';

export type APITestValue = {
	id: number;
	value: string;
};

export const get = () => axiosInstance.get<APITestValue[]>(`${prefix}/`);

export const post = (value: string) => axiosInstance.post<unknown>(`${prefix}/`, { value });
