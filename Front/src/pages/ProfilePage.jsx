/**
 * Это страница «про меня».
 * Показывает email и имя из /api/users/me.
 * Кнопка выхода говорит серверу «забудь refresh» и чистит карман с билетиками.
 * После выхода снова попадёшь на login.
 */
import { Button, message } from "antd";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiGet, http } from "../api/client";
import { ErrorMessage } from "../components/ErrorMessage";
import { Loader } from "../components/Loader";
import { PageTitle } from "../components/PageTitle";
import { ProfileCard } from "../components/ProfileCard";
import { useAuthStore } from "../store/authStore";

export function ProfilePage() {
  const nav = useNavigate();
  const logoutStore = useAuthStore((s) => s.logout);
  const refreshToken = useAuthStore((s) => s.refreshToken);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        setProfile(await apiGet("/api/users/me"));
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  async function logout() {
    try {
      if (refreshToken) {
        await http.post("/api/auth/logout", JSON.stringify(refreshToken), {
          headers: { "Content-Type": "application/json" },
        });
      }
    } catch {
      /* ignore */
    }
    logoutStore();
    message.info("Вы вышли из аккаунта");
    nav("/auth/login");
  }

  if (loading) return <Loader />;

  return (
    <div>
      <PageTitle title="Личный кабинет" extra={<Button danger onClick={logout}>Выйти</Button>} />
      <ErrorMessage message={error} onClose={() => setError(null)} />
      <ProfileCard profile={profile} />
    </div>
  );
}