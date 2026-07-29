const API_BASE_URL = "http://127.0.0.1:8000";

// Basic email list API call
export async function getEmails() {
  const response = await fetch(`${API_BASE_URL}/emails`);
  if (!response.ok) {
    throw new Error("Failed to fetch emails from backend");
  }
  return response.json();
}