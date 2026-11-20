import { Input } from "antd";

export function SearchBar({ value, onChange, placeholder = "Поиск..." }) {
  return <Input.Search allowClear placeholder={placeholder} value={value} onChange={(e) => onChange(e.target.value)} />;
}