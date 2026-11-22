/**
 * Красное сообщение об ошибке запроса.
 * Его можно закрыть.
 */

import { Alert } from "antd";

export function ErrorMessage({ message, onClose }) {
  if (!message) return null;
  return <Alert type="error" message={message} closable onClose={onClose} style={{ marginBottom: 16 }} />;
}