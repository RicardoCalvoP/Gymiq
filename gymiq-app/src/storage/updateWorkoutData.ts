type WorkoutData = {
  users: Array<{
    id: string;
    perfil?: any;
    workouts: Array<{
      id: string;
      exercises: Array<{
        name: string;
        sets: Array<{
          index: number;
          weight: number;
          [key: string]: any;
        }>;
        [key: string]: any;
      }>;
      [key: string]: any;
    }>;
    [key: string]: any;
  }>;
  [key: string]: any;
}[];

type BackendResponse = {
  workout_id: string;
  ejercicios: Array<{
    name: string;
    sets_recomendados: Array<{
      index: number;
      peso_kg: number;
    }>;
  }>;
};

export function applyBackendRecommendationsToWorkoutData(
  workoutData: WorkoutData,
  backendResponse: BackendResponse | null
): WorkoutData {
  if (!backendResponse) return workoutData;

  const { workout_id, ejercicios } = backendResponse;
  if (!workout_id || !Array.isArray(ejercicios)) return workoutData;

  const [, userId] = workout_id.split("_");

  const recPorEjercicio = new Map<string, Record<number, number>>();

  ejercicios.forEach((ej) => {
    const byIndex: Record<number, number> = {};
    if (Array.isArray(ej.sets_recomendados)) {
      ej.sets_recomendados.forEach((s) => {
        if (s && typeof s.index === "number") {
          byIndex[s.index] = s.peso_kg;
        }
      });
    }
    recPorEjercicio.set(ej.name, byIndex);
  });

  return workoutData.map((block) => ({
    ...block,
    users: block.users.map((usuario) => {
      if (usuario.id !== userId) return usuario;

      return {
        ...usuario,
        workouts: usuario.workouts.map((workout) => {
          if (workout.id !== workout_id) return workout;

          return {
            ...workout,
            exercises: workout.exercises.map((exercise) => {
              const recSetPorIndex = recPorEjercicio.get(exercise.name);
              if (!recSetPorIndex) return exercise;

              const newSets = exercise.sets.map((set) => {
                const nuevoPeso = recSetPorIndex[set.index];
                if (nuevoPeso == null) return set;

                return {
                  ...set,
                  weight: nuevoPeso,
                  peso_kg_actual: nuevoPeso,
                };
              });

              return {
                ...exercise,
                sets: newSets,
              };
            }),
          };
        }),
      };
    }),
  }));
}
