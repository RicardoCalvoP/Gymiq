import { useState } from "react";
import { View, Text, TextInput, Pressable, Alert } from "react-native";
import { Feather } from "@expo/vector-icons";
import { useAuth } from "../context/AuthContext";

export default function SignupCard() {
  const { signUp } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const isFormValid =
    email.trim().length > 0 &&
    password.trim().length > 0 &&
    password2.trim().length > 0;

  const handleSignup = async () => {
    if (!isFormValid) {
      Alert.alert("Missing fields", "Please fill in all the fields.");
      return;
    }

    if (password !== password2) {
      Alert.alert("Passwords do not match", "Please make sure both passwords are the same.");
      return;
    }

    try {
      await signUp({ email: email.trim(), password: password.trim() });
    } catch (err) {
      console.log("Error al registrarse", err);
      Alert.alert("Login failed", err?.message || "Invalid credentials");
    }
  };

  return (
    <View className="bg-[#050208] rounded-3xl border border-[#262636] p-6 shadow-lg shadow-black/50">
      {/* Título / descripción */}
      <Text className="text-slate-100 text-xl font-semibold mb-1">
        Create your GymIQ account
      </Text>
      <Text className="text-slate-400 text-sm mb-6">
        Sign up to start tracking and optimizing your workouts.
      </Text>

      {/* Email */}
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

      {/* Password */}
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

      {/* Confirm password */}
      <View className="mb-6">
        <Text className="text-slate-300 text-sm mb-2">
          Confirm password
        </Text>
        <View className="flex-row items-center bg-[#050208] border border-[#27273a] rounded-2xl px-3 py-3">
          <Feather name="lock" size={18} color="#9ca3af" />
          <TextInput
            className="flex-1 text-slate-200 ml-3"
            placeholder="Repeat your password"
            placeholderTextColor="#6b7280"
            secureTextEntry={!showPassword}
            value={password2}
            onChangeText={setPassword2}
          />
        </View>
      </View>

      {/* Botón principal */}
      <Pressable
        onPress={handleSignup}
        disabled={!isFormValid}
        className={`rounded-2xl py-3 items-center mb-2 shadow-lg
          ${ isFormValid ? "shadow-[#7c3aed]/40" : ""}
          ${ isFormValid ? "bg-[#7c3aed]" : "bg-[#4b4b63] opacity-60"}`
        }
      >
        <Text className="text-white font-semibold text-base">Sign up</Text>
      </Pressable>
    </View>
  );
}
