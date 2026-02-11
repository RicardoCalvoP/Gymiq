import { View, Text, Pressable } from "react-native";

import { useUser } from "../../src/context/UserContext";
import { useAuth } from "../../src/context/AuthContext";

import { WORKOUT_DATA } from "../../src/lib/exerciseData";

import Screen from "../components/Screen";
import Button from "../components/Buttons";


export default function ProfileScreen() {
  const { signOut } = useAuth();

  const USUARIOS = WORKOUT_DATA[0].usuarios;

  const { activeUserId, setActiveUserId } = useUser();
  const activeUser = USUARIOS.find((u) => u.id === activeUserId);

  const perfil = activeUser?.perfil;

  return (
    <Screen>
      {/* Cambiar usuario (temporal) */}
      <View className="flex-row space-x-2 mb-4">
        <Button title="Carlos" onPress={() => setActiveUserId("u1")} />
        <Button title="Ana" onPress={() => setActiveUserId("u2")} />
      </View>

      <Text className="text-slate-200 text-[24px] font-bold mx-2 mb-4">
        Perfil
      </Text>

      <View className="bg-slate-800 p-4 rounded-xl mx-2 mb-4">
        <Text className="text-slate-200 text-[20px] font-bold mb-2">
          {perfil?.nombre} {perfil?.apellido}
        </Text>

        <Text className="text-slate-400">Edad: {perfil?.edad}</Text>
        <Text className="text-slate-400">Género: {perfil?.sexo}</Text>
        <Text className="text-slate-400">Altura: {perfil?.altura_cm} cm</Text>
        <Text className="text-slate-400">Peso: {perfil?.peso_usuario} kg</Text>
        <Text className="text-slate-400">
          Frecuencia: {perfil?.frecuencia_entrenamiento}
        </Text>
      </View>

      <View className="bg-slate-800 p-4 rounded-xl mx-2">
        <Text className="text-slate-200 text-[18px] font-bold mb-2">
          Lesiones
        </Text>
        <Text className="text-slate-400">
          {perfil?.historial_lesion_tipo}
        </Text>
        <Text className="text-slate-400">
          {perfil?.historial_lesion_tiempo_semanas} semanas ago
        </Text>
      </View>

      <Pressable
        onPress={() => signOut()}
        className="bg-red-600 rounded-2xl py-3 items-center mt-8 mx-2"
      >
        <Text className="text-white font-semibold">
          Sign out
        </Text>
      </Pressable>
    </Screen>
  );
}
