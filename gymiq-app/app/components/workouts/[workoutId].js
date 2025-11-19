import { Text, FlatList, View } from 'react-native'
import { Link } from 'expo-router'
import { useLocalSearchParams } from 'expo-router'
import Screen from "../Screen";
import { WORKOUT_DATA } from "../../lib/exerciseData"

export default function WorkoutDetails(){
  const { workoutId } = useLocalSearchParams();
  // WORKOUT_DATA stores workouts nested under usuarios. Search all users for the workout id.
  let workout;
  for (const entry of WORKOUT_DATA) {
    if (!entry.usuarios) continue;
    for (const user of entry.usuarios) {
      const found = (user.workouts || []).find((w) => w.id === workoutId);
      if (found) {
        workout = found;
        break;
      }
    }
    if (workout) break;
  }

  if (!workout) {
    return (
      <Screen>
        <Text className="text-slate-200">Workout not found.</Text>
      </Screen>
    );
  }


  return (
    <Screen>
      <Text className="text-slate-200 text-[20px] font-bold mx-2">
        {workout.name}
      </Text>

       <FlatList
        data={workout.exercises}
        keyExtractor={(exercise) => exercise.id}
        renderItem={({ item }) => (
          <View className="mx-2 my-2">
            <Text className="text-slate-200 text-[18px] font-semibold">
              {item.name}
            </Text>
            <Text className="text-slate-400 text-[14px]">
              {item.description}
            </Text>

            {item.sets?.map((set) => (
              <Text
                key={set.index}
                className="text-slate-300 text-[12px]"
              >
                Set {set.index}: {set.weight} kg x {set.reps} reps
              </Text>
            ))}
          </View>
        )}
      />

      <Link href="/" >
        Return Home
      </Link>
    </Screen>
  )
}