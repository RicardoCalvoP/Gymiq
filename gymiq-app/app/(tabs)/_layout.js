import { Tabs } from "expo-router";
import { HomeIcon, InfoIcon } from "../components/Icons";


export default function TabsLayout() {
  return (
    <Tabs
    screenOptions={{
        tabBarStyle: { backgroundColor: "#000" },
      }}

    >
      <Tabs.Screen
        name="profile"
        options={{ title: "Perfil" ,tabBarIcon: ({ color }) => <HomeIcon color={color} />}
      }
      />
      <Tabs.Screen
        name="workout"
        options={{ title: "Workout", tabBarIcon: ({ color }) => <InfoIcon color={color} />, }}
      />
    </Tabs>
  );
}
