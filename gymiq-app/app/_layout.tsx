import { Stack, useRouter, useSegments } from "expo-router";
import { View } from "react-native";

import { SafeAreaProvider } from "react-native-safe-area-context";
import { UserProvider  } from "../src/context/UserContext";
import { WorkoutDataProvider  } from "../src/context/WorkoutDataContext";
import { AuthProvider, useAuth } from "../src/context/AuthContext";

import Button from "./components/Button";
import { useEffect } from "react";

import "../global.css";

function RootNavigator() {
  const { user, isLoaded } = useAuth();
  const  segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    if (!isLoaded) return;

    const inAuthGroup = segments[0] === "(auth)";

    if (!user && !inAuthGroup){
      router.replace("/(auth)/landing")
    }
    else if (user && inAuthGroup) {
      router.replace("/(tabs)")
    }
  },
  [user, isLoaded, segments, router]
);
  return (
    <View className="flex-1">
              <Stack
                screenOptions={{
                  headerStyle: { backgroundColor: "#000" },
                  headerTintColor: "#fff",
                  headerLeft: () => <Button title="Back" onPress={() => router.back()} />,
                  headerRight: () => null,
                  headerShown: true
                }}>

                <Stack.Screen
                  name="(tabs)"
                  options={{ headerShown: false }}
                />

                <Stack.Screen
                  name="(auth)/landing"
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
  )
}
export default function Layout() {
  return (
    <AuthProvider>
      <UserProvider>
        <WorkoutDataProvider>
          <SafeAreaProvider>
            <RootNavigator />
          </SafeAreaProvider>
        </WorkoutDataProvider>
      </UserProvider>
    </AuthProvider>
  );
}
