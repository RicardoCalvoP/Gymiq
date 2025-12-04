import { Stack } from "expo-router";
import { View } from "react-native";
import { UserProvider  } from "./context/UserContext";
import { WorkoutDataProvider  } from "./context/WorkoutDataContext";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { BackButton } from "./components/Button";

export default function Layout() {
  return (
    <UserProvider>
      <WorkoutDataProvider>
        <SafeAreaProvider>
          <View className="flex-1">
            <Stack
              screenOptions={{
                headerStyle: { backgroundColor: "#000" },
                headerTintColor: "#fff",
                headerLeft: () => <BackButton />,
                headerRight: () => null,
                headerShown: true
              }}>

              <Stack.Screen
                name="(tabs)"
                options={{ headerShown: false }}
              />

              <Stack.Screen
                name="components/workouts/[workoutId]"
                options={{
                  title: "Workout",
                }}
              />
            </Stack>
          </View>
        </SafeAreaProvider>
      </WorkoutDataProvider>
    </UserProvider>
  );
}