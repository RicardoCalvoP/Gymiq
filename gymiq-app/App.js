import { StatusBar } from 'expo-status-bar';
import { View } from 'react-native';
import WorkoutScreen  from './app/(tabs)/workout';
import { SafeAreaProvider } from "react-native-safe-area-context";


export default function App() {
  return (
        <SafeAreaProvider>
        <View className="flex-1 items-center justify-center">
            <StatusBar style="light" />
            <WorkoutScreen />
          </View>
        </SafeAreaProvider>


  );
}
