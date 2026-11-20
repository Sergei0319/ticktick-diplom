/**
 * Это форма «запланировать событие».
 * Название и два календаря — с какого по какое время.
 * Помогает перевести выбранные даты в формат для сервера (rangeToIso).
 */
import { Button, DatePicker, Input, Space } from "antd";
import dayjs from "dayjs";

const { RangePicker } = DatePicker;

function logDbg(hypothesisId, message, data) {
  // #region agent log
  fetch("http://127.0.0.1:7414/ingest/2d110755-a68c-4c09-97b8-79313e1cbe07", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "bca6d9" },
    body: JSON.stringify({
      sessionId: "bca6d9",
      hypothesisId,
      location: "EventCreateForm.jsx",
      message,
      data,
      timestamp: Date.now(),
    }),
  }).catch(() => {});
  // #endregion
}

export function EventCreateForm({ title, range, onTitle, onRange, onSubmit }) {
  const addDisabled = !title?.trim() || !range?.[0] || !range?.[1];
  const handleRange = (v) => {
    const next =
      v?.[0] && v?.[1]
        ? [v[0].second(0).millisecond(0), v[1].second(0).millisecond(0)]
        : v;
  // #region agent log
    logDbg("A", "range onChange", {
      hasStart: !!next?.[0],
      hasEnd: !!next?.[1],
      start: next?.[0]?.format?.() ?? null,
      end: next?.[1]?.format?.() ?? null,
    });
  // #endregion
    onRange(next);
  };
  const handleAdd = () => {
  // #region agent log
    logDbg("D", "add click", { title: title?.trim(), addDisabled, hasRange: !!range });
  // #endregion
    onSubmit();
  };
  return (
    <Space direction="vertical" style={{ width: "100%", marginBottom: 16 }}>
      <Input placeholder="Название события" value={title} onChange={(e) => onTitle(e.target.value)} />
      <RangePicker
        showTime={{ format: "HH:mm" }}
        style={{ width: "100%" }}
        value={range}
        onChange={handleRange}
        format="DD.MM.YYYY HH:mm"
      />
      <Button
        type="primary"
        onClick={handleAdd}
        disabled={addDisabled}
      >
        Добавить
      </Button>
    </Space>
  );
}

export function rangeToIso(range) {
  const start = dayjs(range[0]).second(0).millisecond(0);
  const end = dayjs(range[1]).second(0).millisecond(0);
  const payload = { startAt: start.toISOString(), endAt: end.toISOString() };
  // #region agent log
  logDbg("F", "rangeToIso", {
    runId: "post-fix",
    startAt: payload.startAt,
    endAt: payload.endAt,
    startSec: start.second(),
    endSec: end.second(),
  });
  // #endregion
  return payload;
}

export function defaultRange() {
  const start = dayjs().hour(10).minute(0).second(0).millisecond(0);
  return [start, start.add(1, "hour")];
}