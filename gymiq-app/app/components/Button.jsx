import { Pressable, Text } from "react-native";
import { useNavigation } from "@react-navigation/native";

export default function Button({ title, onPress, flex }) {
  return (
    <Pressable
      onPress={onPress}
      className={`
        bg-[#1c1c1e] p-4 rounded-xl mx-2 my-5 ${flex ? "flex-1" : ""}
        `}
    >
      <Text numberOfLines={1} className="text-white font-semibold text-center">
        {title}
      </Text>
    </Pressable>
  );
}


export function BackButton() {
  const navigation = useNavigation();
  return (
    <Pressable onPress={() => navigation.goBack()} className="px-4 rounded-md">
      <Text className="text-white text-[16px]">← Back</Text>
    </Pressable>
  );
}

export function ActionButton({ title, onPress }) {
  return (
    <Pressable
      onPress={onPress}
      className="bg-blue-500 flex-1 py-3 mx-2 rounded-md items-center"
    >
      <Text className="text-slate-200 font-semibold">{title}</Text>
    </Pressable>
  );
}

export function CancelButton({ title, onPress }) {
  return (
    <Pressable
      onPress={onPress}
      className="bg-slate-200 flex-1 py-3 mx-2 rounded-md items-center"
    >
      <Text className="font-semibold">{title}</Text>
    </Pressable>
  );
}