import { Modal, View, Text, Pressable } from "react-native";

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
      <View className="flex-1 bg-black/50 justify-center items-center">
        <View className="bg-[#1c1c1e] p-6 rounded-xl w-4/5">
          <Text className="text-slate-200 text-[20px] font-semibold mb-5">{message}</Text>

          <View className="flex-row items-center space-x-4 mt-5">
            <Pressable
              onPress={onCancel}
              className="bg-gray-300 py-2 rounded-md flex-1 items-center"
            >
              <Text>Cancel</Text>
            </Pressable>

            <Pressable
              onPress={onConfirm}
              className="bg-blue-500 py-2 rounded-md flex-1 items-center"
            >
              <Text className="text-white">Confirm</Text>
            </Pressable>
          </View>
        </View>
      </View>
    </Modal>
  );
}
