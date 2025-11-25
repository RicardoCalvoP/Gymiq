import { Text, View, TextInput, Pressable } from 'react-native'
import { useState, useRef } from 'react'

export default function SetCard({ set, editable = false }) {
  const bg = set && set.index % 2 === 1 ? 'bg-[#1c1c1e]' : 'bg-[#000]';

  const [weightValue, setWeightValue] = useState('');
  const [repsValue, setRepsValue] = useState('');

  const weightPlaceholder = set ? String(set.weight) : '-';
  const repsPlaceholder = set ? String(set.reps) : '-';

  const weightRef = useRef(null);
  const repsRef = useRef(null);

  const parsedWeight = weightValue !== '' ? Number(weightValue) : (set?.weight ?? 0);
  const parsedReps = repsValue !== '' ? Number(repsValue) : (set?.reps ?? 0);
  const computedVol = Number.isFinite(parsedWeight) && Number.isFinite(parsedReps)
    ? parsedWeight * parsedReps
    : '-';

  return (
    <View className={`${bg} px-4 rounded-md my-1 flex-row items-center space-x-2`}>

      <View style={{ width: 40 }}>
        <Text className="text-slate-200 text-[15px] font-medium text-center">
          {set?.index ?? '-'}
        </Text>
      </View>

      <View className="flex-1 items-center">
        <Text className="text-slate-200 text-[15px]">
          {computedVol === '-' ? '-' : String(computedVol)}
         </Text>
      </View>

      <View className="flex-1 items-center">
        <Pressable onPress={() => weightRef.current?.focus()}  >
          {editable ? (
            <TextInput
              ref={weightRef}
              className="text-slate-400 text-[15px] py-4 px-6"
              keyboardType="numeric"
              value={weightValue}
              onChangeText={setWeightValue}
              placeholder={weightPlaceholder}
              placeholderTextColor="#676d76ff"
              selectionColor="#60A5FA"
              style={{
                color: '#E2E8F0',
                width: '100%',
                textAlign: weightValue === '' ? 'left' : 'center',
              }}
              />
            ) : (
              <Text className="text-slate-200 text-[15px] py-4 px-6">
              {weightPlaceholder}
            </Text>
          )}
        </Pressable>
      </View>

      <View className="flex-1 items-center">
      <Pressable onPress={() => repsRef.current?.focus()} className="flex-1 items-center">
        {editable ? (
          <TextInput
          ref={repsRef}
          className="text-slate-400 text-[15px] w-full py-4 px-6"
          keyboardType="numeric"
          value={repsValue}
          onChangeText={setRepsValue}
          placeholder={repsPlaceholder}
          selectionColor="#60A5FA"
            placeholderTextColor="#676d76ff"
            style={{
              color: '#E2E8F0',
              width: '100%',
              textAlign: repsValue === '' ? 'left' : 'center',
            }}
          />
        ) : (
          <Text className="text-slate-200 text-[15px] py-4 px-6">
            {repsPlaceholder}
          </Text>
        )}
      </Pressable>
      </View>
    </View>
  );
}