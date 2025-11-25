import { SafeAreaView } from 'react-native-safe-area-context';

export default function Screen({ children }) {
  return(
    <SafeAreaView className="bg-[#000] flex-1 width-100% px-2">
        {children}
    </SafeAreaView>
  );
}