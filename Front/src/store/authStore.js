/**
 * Память о текущем входе: токены, id, имя и роль.
 * Данные пишутся в localStorage и стираются при выходе.
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