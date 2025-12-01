const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function saveWorkoutLog(log) {
  console.log("Workout log (local):", JSON.stringify(log, null, 2));

  try {
    const response = await fetch(`${API_BASE_URL}/log/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(log),
    });

    if (!response.ok) {
      console.error("Failed to send workout log:", response.status, await response.text());
    } else {
      console.log("Workout log sent successfully");
    }
  } catch (error) {
    console.error("Error sending workout log:", error);
  }
}
