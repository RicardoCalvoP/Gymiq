import { Tabs } from "expo-router";
import { HomeIcon, InfoIcon } from "../components/Icons";
import { UserProvider } from "../context/UserContext";

export default function TabsLayout() {
  return (
    <UserProvider>
      <Tabs
      screenOptions={{
          headerStyle: { backgroundColor: "#000"},
          headerTintColor: "#fff",
          headerTitleStyle: { fontSize: 30},
          tabBarStyle: { backgroundColor: "#000"},
        }}

      >
        <Tabs.Screen
          name="index"
          options={{ title: "Workouts" ,tabBarIcon: ({ color }) => <HomeIcon color={color} />}
        }
        />
        <Tabs.Screen
          name="profile"
          options={{ title: "Profile", tabBarIcon: ({ color }) => <InfoIcon color={color} />, }}
        />
      </Tabs>
  </UserProvider>

  );
}
