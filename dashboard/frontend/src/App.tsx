import { useEffect, useMemo, useState } from "react";
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

function timeAgo(iso: string | null): string {
  if (!iso) return "never";
  const seconds = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (seconds < 60) return `${seconds}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  return `${Math.floor(seconds / 3600)}h ago`;
}

function App() {
  const [status, setStatus] = useState<Status | null>(null);
  const [quotes, setQuotes] = useState<Quote[]>([]);
  const [notifications, setNotificationsState] = useState<NotificationsConfig | null>(null);
  const [tokenInput, setTokenInput] = useState("");
  const [chatIdInput, setChatIdInput] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [search, setSearch] = useState("");
  const [lastRefreshed, setLastRefreshed] = useState<Date | null>(null);

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
    setLastRefreshed(new Date());
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

  const stats = useMemo(() => {
    const authors = new Set(quotes.map((q) => q.author));
    const counts: Record<string, number> = {};
    for (const q of quotes) counts[q.author] = (counts[q.author] || 0) + 1;
    const topEntry = Object.entries(counts).sort((a, b) => b[1] - a[1])[0];
    return {
      total: quotes.length,
      uniqueAuthors: authors.size,
      topAuthor: topEntry ? `${topEntry[0]} (${topEntry[1]})` : "—",
    };
  }, [quotes]);

  const filteredQuotes = useMemo(() => {
    if (!search.trim()) return quotes;
    const q = search.toLowerCase();
    return quotes.filter(
      (item) => item.text.toLowerCase().includes(q) || item.author.toLowerCase().includes(q)
    );
  }, [quotes, search]);

  const isSuccess = status?.last_run?.status === "success";
  const isFailed = status?.last_run?.status === "failed";

  return (
    <div className="console">
      <header className="topbar">
        <div className="brand">
          <span className="brand-dot" />
          <span className="brand-name">scraper-console</span>
        </div>
        <div className="topbar-right">
          <span className={`status-pill ${status?.scheduler_enabled ? "live" : "idle"}`}>
            <span className="dot" />
            {status?.scheduler_enabled ? "AUTO-RUN ON" : "AUTO-RUN OFF"}
          </span>
          <span className="refreshed">synced {lastRefreshed ? timeAgo(lastRefreshed.toISOString()) : "…"}</span>
        </div>
      </header>

      <main className="content">
        <section className="stats-grid">
          <div className="stat-tile">
            <span className="stat-label">Total Records</span>
            <span className="stat-value">{stats.total}</span>
          </div>
          <div className="stat-tile">
            <span className="stat-label">Unique Authors</span>
            <span className="stat-value">{stats.uniqueAuthors}</span>
          </div>
          <div className="stat-tile">
            <span className="stat-label">Top Author</span>
            <span className="stat-value small">{stats.topAuthor}</span>
          </div>
          <div className="stat-tile">
            <span className="stat-label">Last Run</span>
            <span className={`stat-value small ${isSuccess ? "ok" : isFailed ? "fail" : ""}`}>
              {status?.last_run ? status.last_run.status.toUpperCase() : "N/A"}
            </span>
          </div>
        </section>

        <section className="panels">
          <div className="card">
            <div className="card-header">
              <h2>Job Control</h2>
            </div>
            <div className="row">
              <span>Scheduled run (every 30 min)</span>
              <button
                onClick={handleToggle}
                className={`toggle ${status?.scheduler_enabled ? "on" : "off"}`}
              >
                {status?.scheduler_enabled ? "ON" : "OFF"}
              </button>
            </div>
            <div className="row">
              <span>Last run message</span>
              <span className="mono">{status?.last_run?.message ?? "—"}</span>
            </div>
            <button onClick={handleRunNow} disabled={isRunning} className="primary-button">
              {isRunning ? "Running…" : "▶ Run now"}
            </button>
          </div>

          <div className="card">
            <div className="card-header">
              <h2>Notifications</h2>
              <span className={`badge ${notifications?.telegram_token_set ? "badge-ok" : "badge-off"}`}>
                {notifications?.telegram_token_set ? "Telegram connected" : "Not configured"}
              </span>
            </div>
            {notifications?.telegram_token_set && (
              <p className="hint mono">token: {notifications.telegram_token_masked}</p>
            )}
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
              <button type="submit" className="primary-button">
                Save
              </button>
            </form>
          </div>
        </section>

        <section className="card">
          <div className="card-header">
            <h2>Scraped Data ({filteredQuotes.length}/{quotes.length})</h2>
            <input
              type="text"
              className="search"
              placeholder="Filter by text or author…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Quote</th>
                  <th>Author</th>
                </tr>
              </thead>
              <tbody>
                {filteredQuotes.map((q, i) => (
                  <tr key={i}>
                    <td>{q.text}</td>
                    <td>{q.author}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
