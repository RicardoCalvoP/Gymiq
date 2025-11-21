import { Text, View, TextInput, Pressable } from 'react-native'
import { useState, useRef } from 'react'

export default function SetCard({ set, editable = false }) {
  const bg = set && set.index % 2 === 1 ? 'bg-[#1c1c1e]' : 'bg-[#000]';

  // Local editable states (start empty so placeholder shows current value)
  const [weightValue, setWeightValue] = useState('');
  const [repsValue, setRepsValue] = useState('');

  const weightPlaceholder = set ? String(set.weight) : '-';
  const repsPlaceholder = set ? String(set.reps) : '-';

  // Refs to focus inputs when their column is pressed
  const weightRef = useRef(null);
  const repsRef = useRef(null);

  // Compute volume dynamically from weight and reps (prefer user input, fallback to placeholders)
  const parsedWeight = weightValue !== '' ? Number(weightValue) : (set?.weight ?? 0);
  const parsedReps = repsValue !== '' ? Number(repsValue) : (set?.reps ?? 0);
  const computedVol = Number.isFinite(parsedWeight) && Number.isFinite(parsedReps)
    ? parsedWeight * parsedReps
    : '-';

  return (
    // Use items-center + spacing so internal columns can be flex-1
    <View className={`${bg} p-4 rounded-md my-1 flex-row items-center space-x-2`}>
      <View >
        <Text className="text-slate-300 text-[15px] font-medium text-center">
          {set?.index ?? '-'}
        </Text>
      </View>

      {/* Volume column (read-only) */}
      <View className="flex-1 items-center">
        {editable ? (
          <TextInput
            className="text-slate-400 text-[15px] w-full"
            value={computedVol === '-' ? '' : String(computedVol)}
            editable={false}
            placeholder={computedVol === '-' ? '-' : undefined}
            placeholderTextColor="#515761ff"
            style={{ color: '#E2E8F0', textAlign: 'center' }}
          />
        ) : (
          <Text className="text-slate-400 text-[15px]">
            {computedVol === '-' ? '-' : String(computedVol)}
          </Text>
        )}
      </View>

      <Pressable onPress={() => weightRef.current?.focus()}  >
        {editable ? (
          <TextInput
            ref={weightRef}
            className="text-slate-400 text-[15px] w-full"
            keyboardType="numeric"
            value={weightValue}
            onChangeText={setWeightValue}
            placeholder={weightPlaceholder}
            placeholderTextColor="#676d76ff"
            selectionColor="#60A5FA"
            style={{ color: '#E2E8F0', textAlign: 'center', width: '100%' }}
          />
        ) : (
          <Text className="text-slate-400 text-[15px]">
            {weightPlaceholder}
          </Text>
        )}
      </Pressable>

      {/* Reps column - full column is tappable to focus */}
      <Pressable onPress={() => repsRef.current?.focus()} className="flex-1 items-center">
        {editable ? (
          <TextInput
            ref={repsRef}
            className="text-slate-400 text-[15px] w-full"
            keyboardType="numeric"
            value={repsValue}
            onChangeText={setRepsValue}
            placeholder={repsPlaceholder}
            selectionColor="#60A5FA"
            placeholderTextColor="#676d76ff"
            style={{ color: '#E2E8F0', textAlign: 'center', width: '100%' }}
          />
        ) : (
          <Text className="text-slate-400 text-[15px] ">
            {repsPlaceholder}
          </Text>
        )}
      </Pressable>
    </View>
  );
}