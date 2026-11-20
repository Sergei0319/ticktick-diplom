/**
 * Это почтальон между экраном и сервером.
 * Все запросы идут через Axios на адрес из .env; в каждое письмо кладётся пропуск Bearer.
 * Если пропуск протух (401), пытается взять новый через refresh, как продлить абонемент.
 * Если сервер ругается — показывает понятное сообщение, а не загадочный код.
 */
import axios from "axios";
import { useAuthStore } from "../store/authStore";

const baseURL = import.meta.env.VITE_API_URL || "";

export const http = axios.create({
  baseURL,
  timeout: 15000,
});

http.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

http.interceptors.response.use(
  (r) => r,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = useAuthStore.getState().refreshToken;
      if (refresh) {
        try {
          const { data } = await axios.post(`${baseURL}/api/auth/refresh`, JSON.stringify(refresh), {
            headers: { "Content-Type": "application/json" },
          });
          useAuthStore.getState().setSession(data);
          original.headers.Authorization = `Bearer ${data.accessToken}`;
          return http(original);
        } catch {
          useAuthStore.getState().logout();
        }
      }
    }
    const msg =
      error.response?.data?.detail?.message ||
      error.response?.data?.message ||
      error.response?.data?.detail ||
      error.message;
    return Promise.reject(new Error(typeof msg === "string" ? msg : "Ошибка сервера"));
  }
);

export async function apiGet(url) {
  const { data } = await http.get(url);
  return data;
}

export async function apiSend(method, url, body) {
  const { data } = await http.request({ method, url, data: body });
  return data;
}