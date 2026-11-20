/**
 * Это кнопка «Пуск» для сайта в браузере.
 * Втыкает React в пустую страницу и включает переключатель страниц (Router).
 * Ставит русский язык для кнопок Ant Design.
 * Без этого файла на экране ничего бы не появилось.
 */
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { ConfigProvider } from "antd";
import ruRU from "antd/locale/ru_RU";
import { App } from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ConfigProvider locale={ruRU}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ConfigProvider>
  </React.StrictMode>
);