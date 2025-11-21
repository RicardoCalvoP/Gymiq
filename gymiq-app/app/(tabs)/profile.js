import { View, Text } from "react-native";
import { useUser } from "../context/UserContext";
import Screen from "../components/Screen";
import { WORKOUT_DATA } from "../lib/exerciseData";
import Button from "../components/Button";

export default function ProfileScreen() {
  const USUARIOS = WORKOUT_DATA[0].usuarios;

  const { activeUserId, setActiveUserId } = useUser();
  const activeUser = USUARIOS.find((u) => u.id === activeUserId);

  const perfil = activeUser.perfil;

  return (
    <Screen>
      {/* Cambiar usuario (temporal) */}
      <View className="flex-row space-x-2 mb-4">
        <Button title="Carlos" onPress={() => setActiveUserId("u1")} />
        <Button title="Ana" onPress={() => setActiveUserId("u2")} />
        <Button title="Luis" onPress={() => setActiveUserId("u3")} />
      </View>

      <Text className="text-slate-200 text-[24px] font-bold mx-2 mb-4">
        Perfil
      </Text>

      <View className="bg-slate-800 p-4 rounded-xl mx-2 mb-4">
        <Text className="text-slate-200 text-[20px] font-bold mb-2">
          {perfil.nombre} {perfil.apellido}
        </Text>

        <Text className="text-slate-400">Edad: {perfil.edad}</Text>
        <Text className="text-slate-400">Género: {perfil.genero}</Text>
        <Text className="text-slate-400">Altura: {perfil.altura_cm} cm</Text>
        <Text className="text-slate-400">Peso: {perfil.peso_kg} kg</Text>
        <Text className="text-slate-400">
          Frecuencia: {perfil.frecuencia_entrenamiento}
        </Text>
      </View>

      <View className="bg-slate-800 p-4 rounded-xl mx-2">
        <Text className="text-slate-200 text-[18px] font-bold mb-2">
          Lesiones
        </Text>

        {perfil.historial_lesiones ? (
          <Text className="text-red-300">Lesión en: {perfil.zona_lesion}</Text>
        ) : (
          <Text className="text-green-300">Sin lesiones registradas</Text>
        )}
      </View>
    </Screen>
  );
}
