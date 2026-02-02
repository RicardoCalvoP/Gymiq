type Workout = {
  id: string;
  exercises: Array<{
    id: string;
    name: string;
    reps_objetivo: number;
    rpe_objetivo: number;
    sets: Array<{
      weight: number;
      reps: number;
      index: number;
      [key: string]: any;
    }>;
  }>;
  sesion_num?: number;
};

type SessionExercise = {
  exerciseId: string;
  sets: Array<{
    completed: boolean;
    reps: string | number | undefined;
    rpe?: string | number | undefined;
    weight: string | number | undefined;
    recommendedWeight?: number;
    [key: string]: any;
  }>;
};

type UserProfile = {
  [key: string]: any;
};

type ActiveUser = {
  perfil: UserProfile;
};

export function buildWorkoutLog(workout: Workout, session: SessionExercise[], activeUser: ActiveUser) {
  const perfil = activeUser.perfil;

  return {
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
