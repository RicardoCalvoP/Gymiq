import { FontAwesome, FontAwesome6 } from "@expo/vector-icons";
import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import Feather from '@expo/vector-icons/Feather';

export const CircleInfoIcon = (props) => (
  <FontAwesome6 name="circle-info" size={24} color="white" {...props} />
);

export const HomeIcon = (props) => (
  <FontAwesome name="home" size={32} color="white" {...props} />
);

export const InfoIcon = (props) => (
  <FontAwesome name="info" size={32} color="white" {...props} />
);

export const ChangeIcon = (props) => (
  <FontAwesome name="refresh" size={16} color="white" {...props} />
);

export const CheckIcon = (props) => (
  <FontAwesome name="check-circle" size={24} color="green" {...props}/>
);

export const UnCheckIcon = (props) => (
  <MaterialIcons name="radio-button-unchecked" size={24} color="white" {...props}/>
);

export default {
  CircleInfoIcon,
  HomeIcon,
  InfoIcon,
  ChangeIcon,
};