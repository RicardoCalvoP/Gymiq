import { View, Text, Image, Pressable } from "react-native";
import { useRouter } from "expo-router";
import defaultPfp from "../../../assets/default_pfp.png";

type MainInfoProps = {
  displayName: string;
  username: string;
  profilePicture?: string;
};

export default function MainInfo({ displayName, username, profilePicture }: MainInfoProps) {
  const router = useRouter();

  return (
    <View className="justify-center items-center ">
      <Pressable onPress={() => router.push("/screens/EditProfile")} className="-mt-12">
        <Image
          source={profilePicture ? { uri: profilePicture } : defaultPfp}
          className="w-32 h-32 rounded-full"
          />
      </Pressable>
      <Text className="text-white text-[24px] font-bold mt-6">
        {displayName}
      </Text>

      <Text className="text-gray-400 text-[16px] font-normal my-2">
        @{username}
      </Text>
    </View>
  );
}