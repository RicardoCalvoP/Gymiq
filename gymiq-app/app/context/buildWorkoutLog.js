// buildWorkoutLog.js

export function buildWorkoutLog(workout, session, activeUser) {
  const perfil = activeUser.perfil; // perfil unificado

  return {
    // CAMPOS QUE ESPERA TU BACKEND (ANTES):
    workoutId: workout.id,
    date: new Date().toISOString(),

    perfil: perfil,
    sesion_num: workout.sesion_num ?? 0,
    ejercicios: workout.exercises.map((exercise) => {
      const sessionExercise = session.find(
        (se) => se.exerciseId === exercise.id
      );

      const sets = sessionExercise
        ? sessionExercise.sets
            .filter((s) => s.completed)
            .map((s) => ({
              reps:
                s.reps !== "" && s.reps !== undefined
                  ? Number(s.reps)
                  : Number(exercise.reps_objetivo),

              rpe:
                s.rpe !== "" && s.rpe !== undefined
                  ? Number(s.rpe)
                  : Number(exercise.rpe_objetivo),

              peso_kg:
                s.weight !== "" && s.weight !== undefined
                  ? Number(s.weight)
                  : Number(
                      s.recommendedWeight ??
                        (exercise.sets?.[0]?.weight ?? 0)
                    ),
            }))
        : [];

      return {
        name: exercise.name,
        reps_objetivo: exercise.reps_objetivo,
        rpe_objetivo: exercise.rpe_objetivo,
        sets,
      };
    }),
  };
}
