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
        <View className="bg-white p-6 rounded-xl w-4/5">
          <Text className="text-lg font-semibold mb-4">{message}</Text>

          <View className="flex-row justify-between mt-4">
            <Pressable
              onPress={onCancel}
              className="bg-gray-300 px-4 py-2 rounded-md"
            >
              <Text>Cancelar</Text>
            </Pressable>

            <Pressable
              onPress={onConfirm}
              className="bg-blue-500 px-4 py-2 rounded-md"
            >
              <Text className="text-white">Confirmar</Text>
            </Pressable>
          </View>
        </View>
      </View>
    </Modal>
  );
}
