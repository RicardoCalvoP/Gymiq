import { Pressable, Text, View} from "react-native";
import { Link } from "expo-router";

export default function WorkoutCard({ workout }) {

  return (
      <View className="bg-[#1c1c1e] p-4 rounded-xl mx-2 my-3">
        <Link href={`/components/workouts/${workout.id}?isActive=false`} asChild>
          <Pressable key={workout.id}

          >
            <Text className="text-slate-200 text-[20px] font-semibold">
              {workout.name}
            </Text>

            <Text className="text-slate-500 my-2">
              {workout.exercises.length} exercises
            </Text>
        </Pressable>
        </Link>

        <View className="bg-blue-500 mt-2 rounded-md items-center">
          <Link href={`/components/workouts/${workout.id}?isActive=true`} asChild>
            <Pressable key={workout.id} className="flex-1 w-full items-center justify-center py-3">
              <Text className="text-slate-200 font-semibold">
                Start Workout
              </Text>
            </Pressable>
          </Link>
        </View>

      </View>

    )
  }