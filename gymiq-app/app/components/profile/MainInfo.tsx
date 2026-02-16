import { View, Text } from "react-native";

type MainInfoProps = {
  displayName: string;
  username: string;
};

export default function MainInfo({ displayName, username }: MainInfoProps) {
  return (
    <View className="justify-center items-center py-4">

      <Text className="text-white text-[24px] font-bold my-2">
        {displayName}
      </Text>

      <Text className="text-gray-400 text-[16px] font-normal my-2">
        @{username}
      </Text>
    </View>
  );
}