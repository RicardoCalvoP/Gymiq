// SetCard.jsx
import { Text, View, TextInput, Pressable, Vibration } from "react-native";
import { useRef } from "react";
import { CheckIcon, UnCheckIcon } from "../Icons";

export default function SetCard({ set, editable = false, onChange, rowIndex = 0 }) {
  // Alternar fondo por fila (ya no usamos set.index para eso)
  const bg = rowIndex % 2 === 0 ? "bg-[#1c1c1e]" : "bg-[#000]";

  const weightRef = useRef(null);
  const repsRef = useRef(null);

  // valores que vienen del estado de sesión
  const weightValue = set.weight ?? "";
  const repsValue = set.reps ?? "";
  const recommendedWeight = set.recommendedWeight ?? set.weight ?? 0;
  const recommendedReps = set.recommendedReps ?? set.reps ?? 0;

  const weightPlaceholder =
    weightValue === "" ? String(recommendedWeight || "-") : "";
  const repsPlaceholder =
    repsValue === "" ? String(recommendedReps || "-") : "";

  const effectiveWeight =
    weightValue !== "" ? Number(weightValue) : Number(recommendedWeight || 0);
  const effectiveReps =
    repsValue !== "" ? Number(repsValue) : Number(recommendedReps || 0);

  const computedVol =
    Number.isFinite(effectiveWeight) && Number.isFinite(effectiveReps)
      ? effectiveWeight * effectiveReps
      : "-";

  return (
    <View
      className={`${bg} px-4 mt-4 rounded-xl flex-row items-center space-x-2`}
    >
      {/* Set */}
      <View style={{ width: 40 }} className="items-center">
        <Text className="text-slate-200 text-[15px]">
          {set.label ?? set.index ?? rowIndex + 1}
        </Text>
      </View>

      {/* Volumen */}
      {!editable ? (
        <View className="flex-1 items-center">
          <Text className="text-slate-200 text-[15px]">
            {computedVol === "-" ? "-" : String(computedVol)}
          </Text>
        </View>
      ) : null}

      {/* Weight */}
      <View className="flex-1 items-end">
        <Pressable
        onPress={() => weightRef.current?.focus()}
        className="flex-1 items-center">
          {editable && !set.completed? (
            <TextInput
              ref={weightRef}
              className="text-slate-400 text-[15px] py-4 px-6"
              keyboardType="numeric"
              value={weightValue}
              onChangeText={(value) =>
                onChange && onChange({ weight: value })
              }
              placeholder={weightPlaceholder}
              placeholderTextColor="#676d76ff"
              selectionColor="#60A5FA"
              style={{
                color: "#E2E8F0",
                width: "100%",
                textAlign: weightValue === "" ? "left" : "center",
              }}
            />
          ) : (
            <Text className="text-slate-200 text-[15px] py-4 px-6">
              {String(
                weightValue === "" ? recommendedWeight ?? "-" : weightValue
              )}
            </Text>
          )}
        </Pressable>
      </View>

      {/* Reps */}
      <View className="flex-1 items-center">
        <Pressable
          onPress={() => repsRef.current?.focus()}
          className="flex-1 items-center"
        >
          {editable && !set.completed ? (
            <TextInput
              ref={repsRef}
              className="text-slate-400 text-[15px] w-full py-4 px-6"
              keyboardType="numeric"
              value={repsValue}
              onChangeText={(value) => onChange && onChange({ reps: value })}
              placeholder={repsPlaceholder}
              selectionColor="#60A5FA"
              placeholderTextColor="#676d76ff"
              style={{
                color: "#E2E8F0",
                width: "100%",
                textAlign: repsValue === "" ? "left" : "center",
              }}
            />
          ) : (
            <Text className="text-slate-200 text-[15px] py-4 px-6">
              {String(
                repsValue === "" ? recommendedReps ?? "-" : repsValue
              )}
            </Text>
          )}
        </Pressable>
      </View>

      <Pressable
        className="items-center justify-center py-2"
        onPress={() => {

          Vibration.vibrate();

          if (editable && onChange) {
            onChange({ completed: !set.completed });
          }
        }}
      >
        {editable ? (
          <View style={{ width: 40 }} className="items-center">
            {set.completed ? <CheckIcon /> : <UnCheckIcon />}
          </View>
        ) : null}
      </Pressable>
    </View>
  );
}
