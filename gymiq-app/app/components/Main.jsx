import {  FlatList, View, Text, ActivityIndicator} from "react-native";
import Button  from "./Button";
import { useUser } from "../context/UserContext";

import { useWorkoutData } from "../context/WorkoutDataContext";

import WorkoutCard from "./WorkoutCard";
import Screen from "./Screen";

export default function Main() {
  const { workoutData } = useWorkoutData();
  const USUARIOS = workoutData[0].usuarios;

  const { activeUserId, setActiveUserId } = useUser();
  const activeUser = USUARIOS.find((u) => u.id === activeUserId);
  const workouts = activeUser?.workouts ?? [];


  return (
    <Screen>

      {workouts.length === 0 ? (
        <ActivityIndicator color = {"fff"}/>
      ) : (

        <View>
          <View>
            <Text className="text-slate-200 text-[20px] font-bold mx-2">
              Quick Training
            </Text>
            <Button title="Quick Workout (soon)" onPress={() => {}} />
          </View>

          <View>
            <Text className="text-slate-200 text-[20px] font-bold mx-2">
              Workouts
            </Text>
            <View className="flex-row space-x-2 items-center">
              <Button title="New Workout (soon)" flex onPress={() => {}} />
              <Button title="Explore Workout (soon)" flex onPress={() => {}} />
            </View>
          </View>

          <Text className="text-slate-200 text-[20px] font-bold mx-2">
            My Workouts ({workouts.length})
          </Text>

          <FlatList
            data={workouts}
            keyExtractor={(workout) => workout.id}
            renderItem={({ item }) => <WorkoutCard workout={item} />}
          />
        </View>

        )}

      </Screen>
  );
}
