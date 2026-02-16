import { View, Text, Pressable } from "react-native";

import { useUser } from "../../src/context/UserContext";
import { useAuth } from "../../src/context/AuthContext";

import { WORKOUT_DATA } from "../../src/lib/exerciseData";

import Screen from "../components/Screen";
import MainInfo from "../components/profile/MainInfo";

export default function ProfileScreen() {
  const { signOut } = useAuth();

  const USUARIOS = WORKOUT_DATA[0].usuarios;

  const { activeUserId, setActiveUserId } = useUser();
  const activeUser = USUARIOS.find((u) => u.id === activeUserId);

  const perfil = activeUser?.perfil;

  return (
    <Screen>
      <MainInfo displayName={perfil?.displayName || "Usuario"} username={perfil?.username || "usuario"} />
    </Screen>
  );
}
