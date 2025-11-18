import { Pressable, Text } from "react-native";

export function Button({ title, onPress, flex }) {
  return (
    <Pressable
      onPress={onPress}
      className={`
        bg-[#1c1c1e] p-4 rounded-xl mx-2 my-5 ${flex ? "flex-1" : ""}
        `}
    >
      <Text className="text-white font-semibold text-center">
        {title}
      </Text>
    </Pressable>
  );
}
