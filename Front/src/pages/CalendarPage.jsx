/**
 * Экран событий.
 * Загружает список, создаёт событие
 * по названию и датам и удаляет выбранное.
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
      await apiSend("POST", "/api/calendar", body);
      setTitle("");
      setRange(defaultRange());
      load();
    } catch (e) {
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