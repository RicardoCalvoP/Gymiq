import React from "react";
import { createContext, useContext, useState, useMemo, ReactNode } from "react";
import { WORKOUT_DATA as WORKOUT_DATA_SEED } from "../lib/exerciseData";
import { applyBackendRecommendationsToWorkoutData } from "../storage/updateWorkoutData";

type WorkoutDataContextType = {
  workoutData: any;
  setWorkoutData: (data: any) => void;
  applyBackendUpdate: (backendResponse: any) => void;
};

const WorkoutDataContext = createContext<WorkoutDataContextType | null>(null);

type WorkoutDataProviderProps = {
  children: ReactNode;
};

export function WorkoutDataProvider({ children }: WorkoutDataProviderProps): React.ReactElement {
  const [workoutData, setWorkoutData] = useState(WORKOUT_DATA_SEED);

  const value = useMemo(
    () => ({
      workoutData,
      setWorkoutData,
      applyBackendUpdate: (backendResponse: any) => {
        (setWorkoutData as any)((prev: any) =>
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
