import { Alert } from "antd";

// Сообщение об ошибке
export function ErrorMessage({ message, onClose }) {
  if (!message) return null;
  return <Alert type="error" message={message} closable onClose={onClose} style={{ marginBottom: 16 }} />;
}
