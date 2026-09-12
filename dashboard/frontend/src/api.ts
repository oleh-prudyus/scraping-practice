const API_BASE = "http://localhost:8001";

export interface RunLog {
  started_at: string;
  finished_at: string | null;
  status: string;
  message: string;
}

export interface Status {
  scheduler_enabled: boolean;
  last_run: RunLog | null;
}

export interface Quote {
  text: string;
  author: string;
  scraped_at: string;
}

export interface NotificationsConfig {
  telegram_token_set: boolean;
  telegram_token_masked: string;
  telegram_chat_id: string;
}

export async function getStatus(): Promise<Status> {
  const res = await fetch(`${API_BASE}/status`);
  return res.json();
}

export async function toggleScheduler(enabled: boolean): Promise<{ scheduler_enabled: boolean }> {
  const res = await fetch(`${API_BASE}/toggle`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ enabled }),
  });
  return res.json();
}

export async function triggerRun(): Promise<{ message: string }> {
  const res = await fetch(`${API_BASE}/run`, { method: "POST" });
  return res.json();
}

export async function getData(limit = 200): Promise<Quote[]> {
  const res = await fetch(`${API_BASE}/data?limit=${limit}`);
  return res.json();
}

export async function getNotifications(): Promise<NotificationsConfig> {
  const res = await fetch(`${API_BASE}/notifications`);
  return res.json();
}

export async function setNotifications(
  telegramToken: string,
  telegramChatId: string
): Promise<{ message: string }> {
  const res = await fetch(`${API_BASE}/notifications`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      telegram_token: telegramToken,
      telegram_chat_id: telegramChatId,
    }),
  });
  return res.json();
}
