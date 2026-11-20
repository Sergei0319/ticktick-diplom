/**
 * Это одна карточка события в календаре.
 * Показывает когда начало и конец; кнопка — убрать событие.
 * Как стикер на календаре на холодильнике.
 */
import { Button, Card } from "antd";

export function EventItem({ event, onDelete }) {
  return (
    <Card
      size="small"
      style={{ marginBottom: 12, borderLeft: `4px solid ${event.color}` }}
      title={event.title}
    >
      <EventDates start={event.startAt} end={event.endAt} />
      {event.description && <p>{event.description}</p>}
      <Button size="small" danger onClick={() => onDelete(event.id)}>
        Удалить
      </Button>
    </Card>
  );
}

const dateTimeFmt = new Intl.DateTimeFormat("ru", {
  day: "2-digit",
  month: "2-digit",
  year: "numeric",
  hour: "2-digit",
  minute: "2-digit",
});

function EventDates({ start, end }) {
  return (
    <div style={{ color: "#666", marginBottom: 8 }}>
      {dateTimeFmt.format(new Date(start))} — {dateTimeFmt.format(new Date(end))}
    </div>
  );
}