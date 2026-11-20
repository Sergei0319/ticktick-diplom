/**
 * Это карман, где лежат твои билетики после входа.
 * Zustand хранит токены, имя и роль; persist записывает в localStorage, чтобы не логиниться каждый раз.
 * setSession — положить билеты после login; logout — выбросить и забыть.
 * Меню и охрана маршрутов смотрят сюда: пустишь ли ты или нет.
 */
import { create } from "zustand";
import { persist } from "zustand/middleware";

export const useAuthStore = create(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      userId: null,
      displayName: null,
      role: "user",
      setSession: (data) =>
        set({
          accessToken: data.accessToken,
          refreshToken: data.refreshToken,
          userId: data.userId,
          displayName: data.displayName,
          role: data.role || "user",
        }),
      logout: () =>
        set({
          accessToken: null,
          refreshToken: null,
          userId: null,
          displayName: null,
          role: "user",
        }),
      isAuth: () => !!useAuthStore.getState().accessToken,
    }),
    { name: "ticktick-auth" }
  )
);