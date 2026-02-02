import { GestureResponderEvent, Pressable, Text } from "react-native";
import { useNavigation } from "@react-navigation/native";


type ButtonProps = {
  title: string;
  onPress: (event: GestureResponderEvent) => void;
  flex?: boolean;
};

export default function Button({ title, onPress, flex }: ButtonProps) {
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

export function ActionButton({ title, onPress, flex }: ButtonProps) {
  return (
    <Pressable
      onPress={onPress}
      className={`
        bg-blue-600 p-4 rounded-xl mx-2 my-5 ${flex ? "flex-1" : ""}
        `}
    >
      <Text numberOfLines={1} className="text-white font-semibold text-center">
        {title}
      </Text>
    </Pressable>
  );
}

export function CancelButton({ title, onPress, flex }: ButtonProps) {
  return (
    <Pressable
      onPress={onPress}
      className={`
        bg-red-600 p-4 rounded-xl mx-2 my-5 ${flex ? "flex-1" : ""}
        `}
    >
      <Text numberOfLines={1} className="text-white font-semibold text-center">
        {title}
      </Text>
    </Pressable>
  );
}