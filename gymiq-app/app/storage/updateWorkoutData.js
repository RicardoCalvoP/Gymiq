export function applyBackendRecommendationsToWorkoutData(workoutData, backendResponse) {
  if (!backendResponse) return workoutData;

  const { workout_id, ejercicios } = backendResponse;
  if (!workout_id || !Array.isArray(ejercicios)) return workoutData;

  const [, userId] = workout_id.split("_");

  const recPorEjercicio = new Map();

  ejercicios.forEach((ej) => {
    const byIndex = {};
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
    usuarios: block.usuarios.map((usuario) => {
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
