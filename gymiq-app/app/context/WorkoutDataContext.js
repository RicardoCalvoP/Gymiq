import { createContext, useContext, useState, useMemo } from "react";
import { WORKOUT_DATA as WORKOUT_DATA_SEED } from "../lib/exerciseData";
import { applyBackendRecommendationsToWorkoutData } from "../storage/updateWorkoutData";

const WorkoutDataContext = createContext(null);

export function WorkoutDataProvider({ children }) {
  const [workoutData, setWorkoutData] = useState(WORKOUT_DATA_SEED);

  const value = useMemo(
    () => ({
      workoutData,
      setWorkoutData,
      applyBackendUpdate: (backendResponse) => {
        setWorkoutData((prev) =>
          applyBackendRecommendationsToWorkoutData(prev, backendResponse)
        );
      },
    }),
    [workoutData]
  );

  return (
    <WorkoutDataContext.Provider value={value}>
      {children}
    </WorkoutDataContext.Provider>
  );
}

export function useWorkoutData() {
  const ctx = useContext(WorkoutDataContext);
  if (!ctx) {
    throw new Error("useWorkoutData must be used within WorkoutDataProvider");
  }
  return ctx;
}
