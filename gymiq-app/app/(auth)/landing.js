// app/(auth)/landing.js  (o login.js, como lo tengas)
import { useState, useRef  } from "react";
import {
  View,
  Text,
  Pressable,
  ScrollView,
  Animated
} from "react-native";
import { Redirect } from "expo-router";

import Screen from "../components/Screen";
import LoginCard from "./login"
import SignupCard from "./signup"
import { useAuth } from "../context/AuthContext";

export default function LandingScreen() {
  const { signIn, signUp, user, isLoaded } = useAuth();
  const [mode, setMode] = useState("login"); // "login" | "signup"

  const [tabsWidth, setTabsWidth] = useState(0);
  const anim = useRef(new Animated.Value(0)).current;

  if (isLoaded && user) {
    return <Redirect href="/(tabs)" />;
  }

  const isLogin = mode === "login";

  const handleModeChange = (newMode) => {
    setMode(newMode);
    Animated.spring(anim, {
      toValue: newMode === "login" ? 0 : 1,
      useNativeDriver: true,
    }).start();
  };

  const translateX =
    tabsWidth === 0
      ? 0
      : anim.interpolate({
          inputRange: [0, 1],
          outputRange: [0, tabsWidth / 2 ], // slide across half the container
        });

  return (
    <Screen>
      <ScrollView
        className="flex-1"
        contentContainerStyle={{ flexGrow: 1 }}
        keyboardShouldPersistTaps="handled"
      >
        <View className="flex-1 bg-[#050208] py-8">
          {/* LOGO / BRAND */}
          <View className="items-center mb-10">
            <View className="flex-row items-center space-x-1">
              <Text className="text-slate-100 text-2xl font-bold">
                Gym
              </Text>
              <View className="h-16 w-16 rounded-3xl bg-[#6d28d9]/25 border items-center justify-center shadow-xl shadow-[#a855f7]">
                <Text className="text-[#e879f9] text-xl font-bold">IQ</Text>
              </View>
            </View>

            <Text className="mt-3 text-xs uppercase tracking-widest text-slate-400">
              Training harder is training smarter
            </Text>
          </View>

          {/* Tabs Log in / Sign up (MISMA PANTALLA) */}
          <View
            className="flex-row bg-[#6d28d9]/25 border shadow-md shadow-[#a855f7] rounded-xl p-1 mb-4"
            onLayout={(e) => setTabsWidth(e.nativeEvent.layout.width)}
          >
            {/* Animated selection background */}
            {tabsWidth > 0 && (
              <Animated.View
                style={{
                  position: "absolute",
                  left: 4,
                  right: 4,
                  top: 4,
                  bottom: 4,
                  width: tabsWidth /  2 - 9,
                  backgroundColor: "#170730",
                  transform: [{ translateX }],
                }}
                className="rounded-xl "
              />
            )}

            {/* Botón LOGIN */}
            <Pressable
              className="flex-1 rounded-xl py-3 items-center"
              onPress={() => handleModeChange("login")}
            >
              <Text
                className={`font-semibold text-base ${
                  isLogin ? "text-white" : "text-slate-400"
                }`}
              >
                Log in
              </Text>
            </Pressable>

            {/* Botón SIGNUP */}
            <Pressable
              className="flex-1 rounded-xl py-3 items-center"
              onPress={() => handleModeChange("signup")}
            >
              <Text
                className={`font-semibold text-base ${
                  !isLogin ? "text-white" : "text-slate-400"
                }`}
              >
                Sign up
              </Text>
            </Pressable>
          </View>

          {/* CARD PRINCIPAL */}
          {isLogin ? <LoginCard /> : <SignupCard />}
        </View>
      </ScrollView>
    </Screen>
  );
}
