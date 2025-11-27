export function buildWorkoutLog(workout, session) {
  return {
    workoutId: workout.id,
    date: new Date().toISOString(),
    exercises: session.map(ex => ({
      exerciseId: ex.exerciseId,
      sets: ex.sets
        .filter(s => s.completed)
        .map(s => {
          const weight = s.weight !== '' ? Number(s.weight) : s.recommendedWeight;
          const reps = s.reps !== '' ? Number(s.reps) : s.recommendedReps;

          return {
            weight,
            reps,
          };
        }),
    })),
  };
}
