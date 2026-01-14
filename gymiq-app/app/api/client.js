import { API_URL } from "@env";

export async function apiRequest(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  let data = null;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  if (!res.ok) {
    let msg = "Request failed";

    if (data?.detail) {
      const detail = data.detail;
      if (typeof detail === "string") {
        msg = detail;
      } else if (Array.isArray(detail)) {
        // FastAPI 422 validation errors
        msg = detail
          .map((d) => d.msg || JSON.stringify(d))
          .join("\n");
      } else if (typeof detail === "object") {
        msg = detail.msg || JSON.stringify(detail);
      }
    }

    throw new Error(msg);
  }

  return data;
}
