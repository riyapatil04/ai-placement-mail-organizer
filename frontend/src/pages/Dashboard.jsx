import { useEffect, useState } from "react";
import { getEmails } from "../services/api";

function EmailCard({ email }) {
  return (
    <div style={{ border: "1px solid #444", borderRadius: 8, padding: 12, marginBottom: 8 }}>
      <h3 style={{ margin: 0 }}>{email.company || email.subject}</h3>
      <p style={{ margin: "4px 0 0" }}>{email.subject}</p>
      <p style={{ margin: "4px 0 0", fontSize: 12, color: "#aaa" }}>
        From: {email.sender} • {email.received_at}
      </p>
    </div>
  );
}

function EmailList({ emails }) {
  if (!emails || emails.length === 0) {
    return <p>No emails found.</p>;
  }
  return (
    <div>
      {emails.map((email) => (
        <EmailCard key={email.id} email={email} />
      ))}
    </div>
  );
}

export default function Dashboard() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function loadEmails() {
      try {
        setLoading(true);
        setError(null);
        const data = await getEmails();
        if (!cancelled) {
          setEmails(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError("Unable to connect to server.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadEmails();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div style={{ padding: "1rem" }}>
      <h1 style={{ margin: "0 0 1rem" }}>AI Placement Organizer</h1>
      {loading && <p>Loading emails...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {!loading && !error && <EmailList emails={emails} />}
    </div>
  );
}