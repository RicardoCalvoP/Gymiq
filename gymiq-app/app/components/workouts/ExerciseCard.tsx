import { Pressable, Text, View, FlatList, GestureResponderEvent } from "react-native";
import { ChangeIcon } from "../Icons";
import SetCard from "./SetCard";

type Set = {
  id?: string;
  index: number;
  weight: number;
  reps: number;
  [key: string]: any;
};

type Exercise = {
  id: string;
  name: string;
  sets: Set[];
};

type SessionExercise = {
  sets: Array<{
    id: string;
    [key: string]: any;
  }>;
};

type ExerciseCardProps = {
  exercise: Exercise;
  editable?: boolean;
  sessionExercise?: SessionExercise;
  onChangeSet: (exerciseId: string, setId: string, changes: any) => void;
};

export default function ExerciseCard({
  exercise,
  editable = false,
  sessionExercise,
  onChangeSet
}: ExerciseCardProps) {
  const sets = sessionExercise?.sets ?? exercise.sets ?? [];

  return (
      <View className="my-5">
          <View className="flex-row items-center justify-between">
            <Text className="text-slate-200 text-[22px] font-semibold mx-2">
              {exercise.name}
            </Text>
            <View className="pr-4">
              <ChangeIcon color={'white'}/>
            </View>
          </View>

          <Text className="text-slate-500 mx-2">
            {sets.length} sets x{" "}
            {sets.length > 0
              ? (sets[0].recommendedReps ?? sets[0].reps ?? "-")
              : "-"}{" "}
            reps
          </Text>

          <View className="px-4 mt-4 rounded-xl flex-row items-center space-x-2">
            <View style={{ width: 40 }} className="items-center">
              <Text className="text-slate-200 font-medium">
                Set
              </Text>
            </View>

            {!editable ? (
              <View className="flex-1 items-center">
                <Text className="text-slate-200 font-medium">
                  Vol. (kg)
                </Text>
              </View>
            ) : null}

            <View className="flex-1 items-end">
              <Text className="text-slate-200 font-medium">
                Weight (kg)
              </Text>
            </View>

            <View className="flex-1 items-center">
              <Text className="text-slate-200 font-medium">
                Reps
              </Text>
            </View>

            {editable && (
              <View style={{ width: 40 }} className="items-center">
                <Text className="text-slate-200 font-medium">
                  Done
                </Text>
              </View>
            )}
          </View>



          <FlatList
            data={sets}
            keyExtractor={(set: any) => set.id?.toString() ?? String(set.index)}
            scrollEnabled={false}
            renderItem={({ item, index }) => (
              <SetCard
                set={item}
                rowIndex={index}
                editable={editable}
                onChange={(changes) =>
                  onChangeSet(exercise.id, item.id, changes)
                }
              />
            )}
          />
      </View>

    )
  }
