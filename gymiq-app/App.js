import { StatusBar } from 'expo-status-bar';
import { View } from 'react-native';
import Main  from './app/components/Main.jsx';
import { SafeAreaProvider } from "react-native-safe-area-context";
import { UserProvider } from './app/context/UserContext';


export default function App() {
  return (
      <SafeAreaProvider>
        <View className="flex-1 items-center justify-center">
          <StatusBar style="light" />
          <Main />
        </View>
      </SafeAreaProvider>
  );
}
