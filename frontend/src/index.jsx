import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./screens/MainPage/MainPage";
import MemoPage from "./screens/MemoPage/Memo";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/memo" element={<MemoPage />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
