/**
 * Форма входа.
 * Отправляет почту и пароль, сохраняет токены
 * и открывает главную страницу.
 */

import { Button, Form, Input } from "antd";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiSend } from "../api/client";
import { AuthLayout } from "../components/AuthLayout";
import { ErrorMessage } from "../components/ErrorMessage";
import { useAuthStore } from "../store/authStore";

export function LoginPage() {
  const nav = useNavigate();
  const setSession = useAuthStore((s) => s.setSession);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function onFinish(values) {
    setLoading(true);
    setError(null);
    try {
      const data = await apiSend("POST", "/api/auth/login", values);
      setSession(data);
      nav("/");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthLayout title="Вход">
      <ErrorMessage message={error} onClose={() => setError(null)} />
      <Form layout="vertical" onFinish={onFinish}>
        <Form.Item name="email" label="Email" rules={[{ required: true, type: "email" }]}>
          <Input />
        </Form.Item>
        <Form.Item name="password" label="Пароль" rules={[{ required: true }]}>
          <Input.Password />
        </Form.Item>
        <Button type="primary" htmlType="submit" loading={loading} block>
          Войти
        </Button>
      </Form>
      <p style={{ marginTop: 16 }}>
        Нет аккаунта? <Link to="/auth/register">Регистрация</Link>
      </p>
    </AuthLayout>
  );
}