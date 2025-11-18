import {  Stack } from "expo-router";
import { View } from "react-native";

export default function Layout() {
  return (
    <View className="flex-1">
      <Stack
        screenOptions={{
          headerStyle: {backgroundColor: "black"},
          headerTintColor: "#fff",
        }}>

        <Stack.Screen
          name="(tabs)"
          options={{ headerShown: false }}
        />

        {/* Pantalla de detalle, aquí sí quieres header + back */}
        <Stack.Screen
          name="[workoutId]"
          options={{ title: "Workout" }}
        />
      </Stack>
    </View>
  );
}