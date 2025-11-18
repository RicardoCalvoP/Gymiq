import { Pressable, Text} from "react-native";
import { Link } from "expo-router";


export default function WorkoutCard({ workout }) {

  return (
      <Link href={`/${workout.id}`} asChild>
        <Pressable key={workout.id}
        className="bg-[#1c1c1e] p-4 rounded-xl mx-2 my-3"
        >
          <Text className="text-slate-200 text-[18px] font-semibold">
            {workout.name}
          </Text>

          <Text className="text-slate-500 my-2">
            {workout.exercises.length} exercises
          </Text>
      </Pressable>
      </Link>

    )
  }