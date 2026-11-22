/**
 * Поля названия и дат нового события.
 * Переводит выбранный интервал в формат,
 * который ждёт API.
 */

import { Button, DatePicker, Input, Space } from "antd";
import dayjs from "dayjs";

const { RangePicker } = DatePicker;

export function EventCreateForm({ title, range, onTitle, onRange, onSubmit }) {
  const addDisabled = !title?.trim() || !range?.[0] || !range?.[1];
  const handleRange = (v) => {
    const next =
      v?.[0] && v?.[1]
        ? [v[0].second(0).millisecond(0), v[1].second(0).millisecond(0)]
        : v;
    onRange(next);
  };
  const handleAdd = () => {
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
  return payload;
}

export function defaultRange() {
  const start = dayjs().hour(10).minute(0).second(0).millisecond(0);
  return [start, start.add(1, "hour")];
}