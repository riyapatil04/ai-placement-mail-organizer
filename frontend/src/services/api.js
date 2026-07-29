const API_BASE_URL = "http://127.0.0.1:8000";

export async function getEmails() {
  const response = await fetch(`${API_BASE_URL}/emails`);
  if (!response.ok) {
    throw new Error("Failed to fetch emails from backend");
  }
  return response.json();
}

export async function syncEmails() {
  const response = await fetch(`${API_BASE_URL}/sync`, {
    method: "POST",
  });
  if (!response.ok) {
    throw new Error("Failed to sync emails");
  }
  return response.json();
}