import { FontAwesome, FontAwesome6 } from "@expo/vector-icons";

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
export default {
  CircleInfoIcon,
  HomeIcon,
  InfoIcon,
  ChangeIcon,
};