/**
 * Это страница с событиями по датам.
 * Форма создаёт «встречу» с началом и концом; список показывает карточки EventItem.
 * Даты переводятся в формат, понятный серверу.
 * Удаление убирает событие с сервера.
 */
import { useEffect, useState } from "react";
import { apiGet, apiSend } from "../api/client";
import { ErrorMessage } from "../components/ErrorMessage";
import { EventCreateForm, defaultRange, rangeToIso } from "../components/EventCreateForm";
import { EventItem } from "../components/EventItem";
import { Loader } from "../components/Loader";
import { PageTitle } from "../components/PageTitle";

export function CalendarPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [title, setTitle] = useState("");
  const [range, setRange] = useState(defaultRange());

  async function load() {
    setLoading(true);
    try {
      setEvents(await apiGet("/api/calendar"));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function add() {
    try {
      const body = { title, allDay: false, ...rangeToIso(range) };
      // #region agent log
      fetch("http://127.0.0.1:7414/ingest/2d110755-a68c-4c09-97b8-79313e1cbe07", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "bca6d9" },
        body: JSON.stringify({
          sessionId: "bca6d9",
          hypothesisId: "C",
          location: "CalendarPage.jsx:add",
          message: "POST calendar body",
          data: body,
          timestamp: Date.now(),
        }),
      }).catch(() => {});
      // #endregion
      await apiSend("POST", "/api/calendar", body);
      setTitle("");
      setRange(defaultRange());
      load();
    } catch (e) {
      // #region agent log
      fetch("http://127.0.0.1:7414/ingest/2d110755-a68c-4c09-97b8-79313e1cbe07", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "bca6d9" },
        body: JSON.stringify({
          sessionId: "bca6d9",
          hypothesisId: "C",
          location: "CalendarPage.jsx:add",
          message: "POST calendar error",
          data: { err: String(e.message) },
          timestamp: Date.now(),
        }),
      }).catch(() => {});
      // #endregion
      setError(e.message);
    }
  }

  if (loading) return <Loader />;

  return (
    <div>
      <PageTitle title="Календарь" />
      <ErrorMessage message={error} onClose={() => setError(null)} />
      <EventCreateForm title={title} range={range} onTitle={setTitle} onRange={setRange} onSubmit={add} />
      {events.map((e) => (
        <EventItem
          key={e.id}
          event={e}
          onDelete={async (eventId) => {
            await apiSend("DELETE", `/api/calendar/${eventId}`);
            load();
          }}
        />
      ))}
    </div>
  );
}