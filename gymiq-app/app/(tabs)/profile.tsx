import { View, Text, Pressable } from "react-native";

import { useUser } from "../../src/context/UserContext";
import { useAuth } from "../../src/context/AuthContext";

import { WORKOUT_DATA } from "../../src/lib/exerciseData";

import Screen from "../components/Screen";
import MainInfo from "../components/profile/MainInfo";

export default function ProfileScreen() {
  const { signOut } = useAuth();

  const USERS = WORKOUT_DATA[0].users;

  const { activeUserId, setActiveUserId } = useUser();
  const activeUser = USERS.find((u) => u.id === activeUserId);

  const profile = activeUser?.profile;

  return (
    <Screen>
      <MainInfo
        displayName={profile?.displayName || "user"}
        username={profile?.username || "user" }
        profilePicture={profile?.profilePicture || undefined}
        followers={activeUser?.followers.length || 0}
        following={activeUser?.following.length || 0}
        />
    </Screen>
  );
}
