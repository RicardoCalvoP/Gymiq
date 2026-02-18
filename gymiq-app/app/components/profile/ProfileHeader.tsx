import { View, Text } from "react-native";
import { SettingsIcon, EditIcon} from "../Icons";
export default function ProfileHeader() {
  return (
    <View className="flex-row items-center justify-between px-2">
      <EditIcon className="px-2"/>
      <SettingsIcon className="px-2" />
    </View>
  );
}