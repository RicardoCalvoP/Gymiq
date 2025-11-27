export async function saveWorkoutLog(log) {
  // Opción 1: solo log en consola
  console.log('Workout log:', JSON.stringify(log, null, 2));

  // Si quieres un txt, aquí metes RNFS.writeFile(...)
  // Pero lo importante es que esta función sea el ÚNICO lugar
  // donde tocas archivos o base de datos.
}
