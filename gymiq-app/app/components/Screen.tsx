import { ReactNode } from 'react';
import { SafeAreaView } from 'react-native-safe-area-context';

type ScreenProps = {
  children: ReactNode;
};

export default function Screen({ children }: ScreenProps) {
  return(
    <SafeAreaView className="bg-[#000] flex-1 width-100% px-2">
        {children}
    </SafeAreaView>
  );
}
