import { FontAwesome, FontAwesome6 } from "@expo/vector-icons";
import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import Feather from '@expo/vector-icons/Feather';

type IconProps = { color?: string; size?: number; [key: string]: any };

export const CircleInfoIcon = (props: IconProps) => (
  <FontAwesome6 name="circle-info" size={24} color="white" {...props} />
);

export const HomeIcon = (props: IconProps) => (
  <FontAwesome name="home" size={32} color="white" {...props} />
);

export const InfoIcon = (props: IconProps) => (
  <FontAwesome name="info" size={32} color="white" {...props} />
);

export const ChangeIcon = (props: IconProps) => (
  <FontAwesome name="refresh" size={16} color="white" {...props} />
);

export const CheckIcon = (props: IconProps) => (
  <FontAwesome name="check-circle" size={24} color="green" {...props}/>
);

export const UnCheckIcon = (props: IconProps) => (
  <MaterialIcons name="radio-button-unchecked" size={24} color="white" {...props}/>
);

export default {
  CircleInfoIcon,
  HomeIcon,
  InfoIcon,
  ChangeIcon,
};
