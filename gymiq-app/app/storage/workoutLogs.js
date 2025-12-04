// storage/workoutLogs.js
const API_BASE_URL = "http://192.168.68.116:8000";

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
      const errorText = await response.text();
      console.error(
        "Failed to send workout log:",
        response.status,
        errorText
      );
      throw new Error(`Failed to send workout log: ${response.status}`);
    }

    const data = await response.json();
    console.log("Workout log sent successfully, backend response:", data);
    return data;
  } catch (error) {
    console.error("Error sending workout log:", error);
    throw error;
  }
}
