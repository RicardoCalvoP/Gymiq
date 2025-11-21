import { Text, FlatList, View, ScrollView} from 'react-native'
import { useLocalSearchParams } from 'expo-router'

import { WORKOUT_DATA } from "../../lib/exerciseData"

import Screen from "../Screen";
import Button from '../Button';
import ExerciseCard from './ExerciseCard';

export default function WorkoutDetails(){
  const { workoutId, isActive } = useLocalSearchParams();
  const editable = isActive === 'true';
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
      <ScrollView>
        <View className="flex-1 items-center mb-4 mt-12">
          {editable ? (
            <Text className="text-slate-200 text-[25px] font-bold mx-2">
              Is Active: {workout.name}
            </Text>
          ) : (
            <Text className="text-slate-200 text-[25px] font-bold mx-2">
              {workout.name}
            </Text>
          )}
        </View>

        <FlatList
          data={workout.exercises}
          keyExtractor={(exercise) => exercise.id}
          scrollEnabled={false}
          renderItem={({ item }) => (
            <ExerciseCard exercise={item} editable={editable} />
          )}
        />

        <View>
          <Button />
        </View>
      </ScrollView>
    </Screen>
  )
}