import { Modal, View, Text, Pressable } from "react-native";
import { ActionButton, CancelButton } from "./Button";

export default function ConfirmModal({
  visible,
  onCancel,
  onConfirm,
  message = "¿Estás seguro?",
}) {
  return (
    <Modal
      transparent
      animationType="fade"
      visible={visible}
      onRequestClose={onCancel}
    >
      <View className="flex-1 bg-black/75 justify-center items-center">
        <View className="bg-[#1c1c1e] p-4 rounded-xl w-4/5">
          <Text className="text-slate-200 text-[20px] font-semibold mb-5">{message}</Text>

          <View className="flex-row items-center mt-5">

            <CancelButton
              title="Cancel"
              onPress={onCancel}
            />
            <ActionButton
              title="Confirm"
              onPress={onConfirm}
            />
          </View>
        </View>
      </View>
    </Modal>
  );
}
