/**
 * Главный экран со счётчиками.
 * Запрашивает заметки, задачи, просроченные
 * и события и показывает их количество.
 */

import { Card, Col, Row, Statistic } from "antd";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiGet } from "../api/client";
import { ErrorMessage } from "../components/ErrorMessage";
import { Loader } from "../components/Loader";
import { PageTitle } from "../components/PageTitle";

export function HomePage() {
  const [data, setData] = useState({ notes: 0, todos: 0, overdue: 0, events: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const [notes, todos, overdue, events] = await Promise.all([
          apiGet("/api/notes"),
          apiGet("/api/todos"),
          apiGet("/api/todos/overdue"),
          apiGet("/api/calendar"),
        ]);
        setData({ notes: notes.length, todos: todos.length, overdue: overdue.length, events: events.length });
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <Loader />;
  return (
    <div>
      <PageTitle title="Главная" />
      <ErrorMessage message={error} onClose={() => setError(null)} />
      <Row gutter={16}>
        <Col span={6}>
          <Card>
            <Statistic title="Заметки" value={data.notes} />
            <Link to="/notes">Открыть →</Link>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Задачи" value={data.todos} />
            <Link to="/todos">Открыть →</Link>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Просрочено" value={data.overdue} valueStyle={{ color: "#cf1322" }} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="События" value={data.events} />
            <Link to="/calendar">Открыть →</Link>
          </Card>
        </Col>
      </Row>
    </div>
  );
}