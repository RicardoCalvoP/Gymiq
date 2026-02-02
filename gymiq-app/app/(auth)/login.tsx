import { useState } from "react";
import { View, Text, TextInput, Pressable, Alert } from "react-native";
import { Feather } from "@expo/vector-icons";

import { useAuth } from "../../src/context/AuthContext";

export default function LoginCard() {
  const { signIn } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  const isFormValid = email.trim().length > 0 && password.trim().length > 0;

  const handleLogin = async () => {
    if (!isFormValid) {
      Alert.alert("Missing fields", "Please enter both email and password.");
      return;
    }

    try {
      await signIn({ email: email.trim(), password: password.trim() });
    } catch (err) {
      console.log("Error al iniciar sesión", err);
      Alert.alert(
        "Login failed",
        (err as any)?.message || "Invalid credentials");
    }
  };

  return (
    <View className="bg-[#050208] rounded-3xl border border-[#262636] p-6 shadow-lg shadow-black/50">
      <Text className="text-slate-100 text-xl font-semibold mb-1">
        Welcome back to GymIQ
      </Text>
      <Text className="text-slate-400 text-sm mb-6">
        Enter your credentials to access your training dashboard.
      </Text>

      <View className="mb-4">
        <Text className="text-slate-300 text-sm mb-2">Email</Text>
        <View className="flex-row items-center bg-[#050208] border border-[#27273a] rounded-2xl px-3 py-3">
          <Feather name="mail" size={18} color="#9ca3af" />
          <TextInput
            className="flex-1 text-slate-200 ml-3"
            placeholder="Enter your email"
            placeholderTextColor="#6b7280"
            keyboardType="email-address"
            autoCapitalize="none"
            value={email}
            onChangeText={setEmail}
          />
        </View>
      </View>

      <View className="mb-3">
        <Text className="text-slate-300 text-sm mb-2">Password</Text>
        <View className="flex-row items-center bg-[#050208] border border-[#27273a] rounded-2xl px-3 py-3">
          <Feather name="lock" size={18} color="#9ca3af" />
          <TextInput
            className="flex-1 text-slate-200 ml-3"
            placeholder="Enter your password"
            placeholderTextColor="#6b7280"
            secureTextEntry={!showPassword}
            value={password}
            onChangeText={setPassword}
          />
          <Pressable
            onPress={() => setShowPassword((prev) => !prev)}
            hitSlop={8}
          >
            <Feather
              name={showPassword ? "eye-off" : "eye"}
              size={18}
              color="#9ca3af"
            />
          </Pressable>
        </View>
      </View>

      <View className="flex-row items-center justify-between mb-6 mt-1">
        <Pressable
          onPress={() => setRememberMe((prev) => !prev)}
          className="flex-row items-center"
        >
          <View
            className={`h-4 w-4 rounded-md mr-2 border ${
              rememberMe
                ? "bg-[#7c3aed] border-[#7c3aed]"
                : "border-[#4b4b63]"
            } items-center justify-center`}
          >
            {rememberMe ? (
              <View className="h-2 w-2 rounded-sm bg-white" />
            ) : null}
          </View>
          <Text className="text-xs text-slate-400">Remember me</Text>
        </Pressable>

        <Text className="text-xs text-slate-400 underline">
          Forgot password?
        </Text>
      </View>

      <Pressable
        onPress={handleLogin}
        className="bg-[#7c3aed] rounded-2xl py-3 items-center mb-3"
      >
        <Text className="text-white font-semibold">
          Log in
        </Text>
      </Pressable>
    </View>
  );
}
