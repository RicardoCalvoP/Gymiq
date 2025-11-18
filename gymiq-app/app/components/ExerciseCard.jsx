import { Pressable, Text} from "react-native";
import { Link } from "expo-router";


export default function ExerciseCard({ exercise }) {

  return (
      <Link href={`/${exercise.id}`} asChild>
        <Pressable key={exercise.id}
        className="bg-[#1c1c1e] p-4 rounded-xl mx-2 my-3"
        >
          <Text className="text-slate-200 text-[18px] font-semibold">
            {exercise.name}
          </Text>

          <Text className="text-slate-500 my-2">
            {exercise.sets.length} sets
          </Text>
      </Pressable>
      </Link>

    )
  }