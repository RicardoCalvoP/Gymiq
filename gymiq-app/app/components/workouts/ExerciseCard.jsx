import { Pressable, Text, View, FlatList} from "react-native";
import { Link } from "expo-router";

import { ChangeIcon } from "../Icons";
import SetCard from "./SetCard";

export default function ExerciseCard({ exercise, editable = false }) {

  return (
      <View className="my-5">
          <View className="flex-row items-center justify-between">
            <Text className="text-slate-300 text-[22px] font-semibold mx-2">
              {exercise.name}
            </Text>
            <View className="pr-4">
              <ChangeIcon color={'white'}/>
            </View>
          </View>

          <Text className="text-slate-500 mx-2">
            {exercise.sets?.length ?? 0} sets x {exercise.sets?.[0]?.reps ?? '-'} reps
          </Text>

          <View className="p-2 mx-2 mt-4 rounded-xl flex-row items-center">
            <Text className="text-slate-300 font-medium" style={{ width: 40, textAlign: 'center' }}>
              Set
            </Text>

            <Text className="text-slate-300 font-medium flex-1 text-center">
              Vol. (kg)
            </Text>

            <Text className="text-slate-300 font-medium flex-1 text-center">
              Weight (kg)
            </Text>

            <Text className="text-slate-300 font-medium flex-1 text-center">
              Reps
            </Text>
          </View>

          <FlatList
            data={exercise.sets}
            keyExtractor={(set) => set.index}
            scrollEnabled={false}
            renderItem={({ item }) => (
              <SetCard set={item} editable={editable}/>
            )}
          />
      </View>

    )
  }