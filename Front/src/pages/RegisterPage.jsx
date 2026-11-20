/**
 * Это страница «завести новый аккаунт».
 * Пишешь почту, пароль и как тебя звать; сервер создаёт нового пользователя.
 * Если email занят — скажет об этом, не создавая дубликат.
 * После успеха сразу можно работать, как после login.
 */
import { Button, Form, Input } from "antd";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiSend } from "../api/client";
import { AuthLayout } from "../components/AuthLayout";
import { ErrorMessage } from "../components/ErrorMessage";
import { useAuthStore } from "../store/authStore";

export function RegisterPage() {
  const nav = useNavigate();
  const setSession = useAuthStore((s) => s.setSession);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function onFinish(values) {
    setLoading(true);
    setError(null);
    try {
      const data = await apiSend("POST", "/api/auth/register", values);
      setSession(data);
      nav("/");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthLayout title="Регистрация">
      <ErrorMessage message={error} onClose={() => setError(null)} />
      <Form layout="vertical" onFinish={onFinish}>
        <Form.Item name="displayName" label="Имя">
          <Input />
        </Form.Item>
        <Form.Item name="email" label="Email" rules={[{ required: true, type: "email" }]}>
          <Input />
        </Form.Item>
        <Form.Item name="password" label="Пароль" rules={[{ required: true, min: 6 }]}>
          <Input.Password />
        </Form.Item>
        <Button type="primary" htmlType="submit" loading={loading} block>
          Создать аккаунт
        </Button>
      </Form>
      <p style={{ marginTop: 16 }}>
        Уже есть аккаунт? <Link to="/auth/login">Войти</Link>
      </p>
    </AuthLayout>
  );
}