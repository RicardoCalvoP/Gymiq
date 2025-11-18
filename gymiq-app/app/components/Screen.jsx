import { View } from "react-native";

export default function Screen({ children}) {
  return(
    <View className="bg-[#000] width-100% px-2">
      {children}
    </View>
  );
}