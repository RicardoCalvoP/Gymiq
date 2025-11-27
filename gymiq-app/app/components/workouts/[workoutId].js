import { Text, FlatList, View, ScrollView, Pressable} from 'react-native'
import { useState } from "react";
import { useLocalSearchParams, useRouter } from 'expo-router'

import { WORKOUT_DATA } from "../../lib/exerciseData"

import { buildWorkoutLog } from '../../context/buildWorkoutLog';
import { saveWorkoutLog } from '../../storage/workoutLogs';

import ConfirmModal from "../ConfirmModal";
import Screen from "../Screen";
import ExerciseCard from './ExerciseCard';
import { ActionButton } from '../Button';

const generarIdUnico = () => Math.random().toString(36).slice(2);

export default function WorkoutDetails(){
  const { workoutId, isActive } = useLocalSearchParams();
  const editable = isActive === 'true';
  const [modalVisible, setModalVisible] = useState(false);
  const router = useRouter();


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

const [session, setSession] = useState(() =>
  workout
    ? workout.exercises.map((exercise) => ({
        exerciseId: exercise.id,
        sets: exercise.sets.map((set) => ({
          id: generarIdUnico(),
          recommendedWeight: set.weight,
          recommendedReps: set.reps,
          weight: '',
          reps: '',
          completed: false,
        })),
      }))
    : []
);

  const handleConfirmEndWorkout = async () => {
    const log = buildWorkoutLog(workout, session);
    await saveWorkoutLog(log);
    setModalVisible(false);
    router.push('/(tabs)');
  };

  const handleChangeSet = (exerciseId, setId, changes) => {
  setSession(prev =>
    prev.map(ex => {
      if (ex.exerciseId !== exerciseId) return ex;
      return {
        ...ex,
        sets: ex.sets.map(set =>
          set.id === setId ? { ...set, ...changes } : set
        ),
      };
    })
  );
};

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
          renderItem={({ item }) => {
            const sessionExercise = session.find(ex => ex.exerciseId === item.id);
            return (
              <ExerciseCard
                exercise={item}
                editable={editable}
                sessionExercise={sessionExercise}
                onChangeSet={handleChangeSet}
              />
            );
          }}
        />


        {
        editable ? (
        <ActionButton
          title="End Workout"
          onPress={() => setModalVisible(true)}
        />
        ) : null
        }

        <ConfirmModal
        visible={modalVisible}
        message="Are you sure you want to mark this workout as completed?"
        onCancel={() => setModalVisible(false)}
        onConfirm={() => {
          handleConfirmEndWorkout();
        }}
      />
      </ScrollView>
    </Screen>
  )
}