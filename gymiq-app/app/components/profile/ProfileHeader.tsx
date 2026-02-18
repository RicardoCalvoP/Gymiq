import { View, Pressable } from "react-native";
import { SettingsIcon, EditIcon} from "../Icons";
import { useRouter } from "expo-router";

export default function ProfileHeader() {
  const router = useRouter();
  return (
    <View className="flex-row items-center justify-between px-2">
      <Pressable onPress={() => router.push("/screens/EditProfile")} className="-mt-12">
        <EditIcon className="px-2"/>
      </Pressable>

      <Pressable onPress={() => router.push("/screens/Settings")} className="-mt-12">
         <SettingsIcon className="px-2" />
      </Pressable>
    </View>
  );
}