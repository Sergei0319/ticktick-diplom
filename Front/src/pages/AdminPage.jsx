import { Card, Col, Row, Statistic } from "antd";
import { useEffect, useState } from "react";
import { apiGet, apiSend } from "../api/client";
import { AdminUserTable } from "../components/AdminUserTable";
import { ErrorMessage } from "../components/ErrorMessage";
import { Loader } from "../components/Loader";
import { PageTitle } from "../components/PageTitle";

export function AdminPage() {
  const [users, setUsers] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function load() {
    setLoading(true);
    try {
      const [u, s] = await Promise.all([apiGet("/api/admin/users"), apiGet("/api/admin/stats")]);
      setUsers(u);
      setStats(s);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  if (loading) return <Loader />;

  return (
    <div>
      <PageTitle title="Админ-панель" />
      <ErrorMessage message={error} onClose={() => setError(null)} />
      {stats && (
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={6}>
            <Card>
              <Statistic title="Пользователи" value={stats.users} />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic title="Заметки" value={stats.notes} />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic title="Задачи" value={stats.todos} />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic title="События" value={stats.events} />
            </Card>
          </Col>
        </Row>
      )}
      <AdminUserTable
        users={users}
        loading={loading}
        onRole={async (id, role) => {
          await apiSend("PATCH", `/api/admin/users/${id}/role`, { role });
          load();
        }}
        onDelete={async (id) => {
          await apiSend("DELETE", `/api/admin/users/${id}`);
          load();
        }}
      />
    </div>
  );
}