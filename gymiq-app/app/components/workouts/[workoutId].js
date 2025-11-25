import { Text, FlatList, View, ScrollView, Pressable} from 'react-native'
import { useState } from "react";
import { useLocalSearchParams } from 'expo-router'
import ConfirmModal from "../ConfirmModal";

import { WORKOUT_DATA } from "../../lib/exerciseData"

import Screen from "../Screen";
import ExerciseCard from './ExerciseCard';

export default function WorkoutDetails(){
  const { workoutId, isActive } = useLocalSearchParams();
  const editable = isActive === 'true';
  const [modalVisible, setModalVisible] = useState(false);

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
        <View className="flex-1 mb-4">
          <Text className="text-slate-200 text-[30px] font-bold mx-2">
            {workout.name}
          </Text>
        </View>

        <FlatList
          data={workout.exercises}
          keyExtractor={(exercise) => exercise.id}
          scrollEnabled={false}
          renderItem={({ item }) => (
            <ExerciseCard exercise={item} editable={editable} />
          )}
        />

        {
        editable ? (
        <View className="bg-blue-500 mt-2 rounded-md items-center">
            <Pressable
              className="flex-1 w-full items-center justify-center py-3 "
              onPress={() => setModalVisible(true)}
              >
                <Text className="text-slate-200 font-semibold">
                  Complete Workout
                </Text>
            </Pressable>
        </View>
        ) : null
        }

        <ConfirmModal
        visible={modalVisible}
        message="Are you sure you want to mark this workout as completed?"
        onCancel={() => setModalVisible(false)}
        onConfirm={() => {
          setModalVisible(false);
        }}
      />
      </ScrollView>
    </Screen>
  )
}