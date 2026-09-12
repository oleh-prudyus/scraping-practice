import { useEffect, useState } from "react";
import {
  getStatus,
  toggleScheduler,
  triggerRun,
  getData,
  getNotifications,
  setNotifications,
  type Status,
  type Quote,
  type NotificationsConfig,
} from "./api";
import "./App.css";

function App() {
  const [status, setStatus] = useState<Status | null>(null);
  const [quotes, setQuotes] = useState<Quote[]>([]);
  const [notifications, setNotificationsState] = useState<NotificationsConfig | null>(null);
  const [tokenInput, setTokenInput] = useState("");
  const [chatIdInput, setChatIdInput] = useState("");
  const [isRunning, setIsRunning] = useState(false);

  async function refresh() {
    const [statusRes, dataRes, notifRes] = await Promise.all([
      getStatus(),
      getData(),
      getNotifications(),
    ]);
    setStatus(statusRes);
    setQuotes(dataRes);
    setNotificationsState(notifRes);
    setChatIdInput(notifRes.telegram_chat_id);
  }

  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, 5000);
    return () => clearInterval(interval);
  }, []);

  async function handleToggle() {
    if (!status) return;
    await toggleScheduler(!status.scheduler_enabled);
    await refresh();
  }

  async function handleRunNow() {
    setIsRunning(true);
    await triggerRun();
    setTimeout(async () => {
      await refresh();
      setIsRunning(false);
    }, 8000);
  }

  async function handleSaveNotifications(e: React.FormEvent) {
    e.preventDefault();
    await setNotifications(tokenInput, chatIdInput);
    setTokenInput("");
    await refresh();
  }

  return (
    <div className="dashboard">
      <h1>Scraping Dashboard</h1>

      <section className="card">
        <h2>Стан</h2>
        <div className="row">
          <span>Автозапуск (кожні 30 хв):</span>
          <button onClick={handleToggle} className={status?.scheduler_enabled ? "on" : "off"}>
            {status?.scheduler_enabled ? "Увімкнено" : "Вимкнено"}
          </button>
        </div>
        <div className="row">
          <span>Останній запуск:</span>
          <span>
            {status?.last_run
              ? `${status.last_run.status} — ${status.last_run.message}`
              : "ще не запускався"}
          </span>
        </div>
        <button onClick={handleRunNow} disabled={isRunning} className="run-button">
          {isRunning ? "Виконується..." : "Запустити зараз"}
        </button>
      </section>

      <section className="card">
        <h2>Сповіщення (Telegram)</h2>
        <p className="hint">
          {notifications?.telegram_token_set
            ? `Токен збережено: ${notifications.telegram_token_masked}`
            : "Токен ще не налаштований"}
        </p>
        <form onSubmit={handleSaveNotifications} className="notif-form">
          <input
            type="text"
            placeholder="Telegram bot token"
            value={tokenInput}
            onChange={(e) => setTokenInput(e.target.value)}
          />
          <input
            type="text"
            placeholder="Chat ID"
            value={chatIdInput}
            onChange={(e) => setChatIdInput(e.target.value)}
          />
          <button type="submit">Зберегти</button>
        </form>
      </section>

      <section className="card">
        <h2>Дані ({quotes.length})</h2>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Цитата</th>
                <th>Автор</th>
              </tr>
            </thead>
            <tbody>
              {quotes.map((q, i) => (
                <tr key={i}>
                  <td>{q.text}</td>
                  <td>{q.author}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default App;
