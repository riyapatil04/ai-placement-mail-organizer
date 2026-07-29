import { useEffect, useState } from "react";
import { getEmails, syncEmails } from "../services/api";

function EmailCard({ email, onClick }) {
  return (
    <div
      style={{
        border: "1px solid #444",
        borderRadius: 8,
        padding: 12,
        marginBottom: 8,
        cursor: "pointer",
      }}
      onClick={() => onClick(email)}
    >
      <h3 style={{ margin: 0 }}>{email.subject || "(No subject)"}</h3>
      <p style={{ margin: "4px 0 0", fontSize: 14, color: "#ccc" }}>
        From: {email.sender}
      </p>
      <p style={{ margin: "4px 0 0", fontSize: 12, color: "#aaa" }}>
        {email.received_at ? new Date(email.received_at).toLocaleString() : ""}
      </p>
    </div>
  );
}

function EmailList({ emails, onEmailClick }) {
  if (!emails || emails.length === 0) {
    return <p>No emails found.</p>;
  }
  return (
    <div>
      {emails.map((email) => (
        <EmailCard key={email.id} email={email} onClick={onEmailClick} />
      ))}
    </div>
  );
}

export default function Dashboard() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [syncing, setSyncing] = useState(false);
  const [selectedEmail, setSelectedEmail] = useState(null);

  async function loadEmails() {
    try {
      setLoading(true);
      setError(null);
      const data = await getEmails();
      setEmails(data);
    } catch (err) {
      setError("Unable to connect to server.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadEmails();
  }, []);

  async function handleSync() {
    try {
      setSyncing(true);
      await syncEmails();
      await loadEmails();
    } catch (err) {
      setError("Sync failed.");
    } finally {
      setSyncing(false);
    }
  }

  return (
    <div style={{ padding: "1rem" }}>
      <h1 style={{ margin: "0 0 1rem" }}>AI Placement Organizer</h1>

      <button
        onClick={handleSync}
        disabled={syncing}
        style={{ marginBottom: "1rem", padding: "6px 12px" }}
      >
        {syncing ? "Syncing..." : "🔄 Sync Emails"}
      </button>

      {loading && <p>Loading emails...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && (
        <div style={{ display: "flex", gap: "1rem" }}>
          <div style={{ flex: 1 }}>
            <h2>Emails</h2>
            <EmailList emails={emails} onEmailClick={setSelectedEmail} />
          </div>

          <div style={{ flex: 1, borderLeft: "1px solid #444", paddingLeft: "1rem" }}>
            <h2>Email Details</h2>
            {!selectedEmail && <p>Select an email to view details.</p>}
            {selectedEmail && (
              <div>
                <h3>{selectedEmail.subject || "(No subject)"}</h3>
                <p><strong>From:</strong> {selectedEmail.sender}</p>
                <p>
                  <strong>Received:</strong>{" "}
                  {selectedEmail.received_at
                    ? new Date(selectedEmail.received_at).toLocaleString()
                    : "—"}
                </p>
                <pre
                  style={{
                    whiteSpace: "pre-wrap",
                    fontSize: 13,
                    background: "#111",
                    padding: 8,
                    borderRadius: 4,
                  }}
                >
                  {selectedEmail.body || "(No body)"}
                </pre>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}