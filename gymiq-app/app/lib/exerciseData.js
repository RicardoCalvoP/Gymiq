export const WORKOUT_DATA = [
 {
  "usuarios": [
    {
      "id": "u1",
      "perfil": {
        "nombre": "Carlos",
        "apellido": "Ramírez",
        "edad": 28,
        "genero": "Masculino",
        "peso_kg": 78,
        "altura_cm": 180,
        "frecuencia_entrenamiento": "4 veces por semana",
        "historial_lesiones": true,
        "zona_lesion": "Rodilla derecha"
      },
      "workouts": [
        {
          "id": "w_u1_0",
          "name": "Push personalizado Carlos",
          "exercises": [
            {
              "id": "e_u1_0",
              "name": "Press banca con barra",
              "description": "Movimiento principal de empuje horizontal.",
              "sets": [
                { "index": 1, "weight": 55, "reps": 10 },
                { "index": 2, "weight": 70, "reps": 8 },
                { "index": 3, "weight": 70, "reps": 6 }
              ]
            },
            {
              "id": "e_u1_1",
              "name": "Press militar con barra",
              "description": "Empuje vertical para hombro.",
              "sets": [
                { "index": 1, "weight": 30, "reps": 10 },
                { "index": 2, "weight": 40, "reps": 8 }
              ]
            },
            {
              "id": "e_u1_2",
              "name": "Fondos en paralelas asistidos",
              "description": "Trabajo de tríceps y pecho con asistencia.",
              "sets": [
                { "index": 1, "weight": -10, "reps": 12 },
                { "index": 2, "weight": -5, "reps": 10 }
              ]
            }
          ]
        },
        {
          "id": "w_u1_1",
          "name": "Legs (adaptado rodilla)",
          "exercises": [
            {
              "id": "e_u1_3",
              "name": "Prensa inclinada",
              "description": "Menos carga en rodilla que la sentadilla libre.",
              "sets": [
                { "index": 1, "weight": 90, "reps": 12 },
                { "index": 2, "weight": 110, "reps": 10 }
              ]
            },
            {
              "id": "e_u1_4",
              "name": "Peso muerto rumano",
              "description": "Trabajo de isquios y glúteo.",
              "sets": [
                { "index": 1, "weight": 40, "reps": 12 },
                { "index": 2, "weight": 50, "reps": 10 }
              ]
            },
            {
              "id": "e_u1_5",
              "name": "Curl femoral en máquina",
              "description": "Aislamiento de isquios.",
              "sets": [
                { "index": 1, "weight": 25, "reps": 12 },
                { "index": 2, "weight": 30, "reps": 10 }
              ]
            }
          ]
        }
      ]
    },
    {
      "id": "u2",
      "perfil": {
        "nombre": "Ana",
        "apellido": "García",
        "edad": 32,
        "genero": "Femenino",
        "peso_kg": 62,
        "altura_cm": 165,
        "frecuencia_entrenamiento": "3 veces por semana",
        "historial_lesiones": false,
        "zona_lesion": null
      },
      "workouts": [
        {
          "id": "w_u2_0",
          "name": "Upper body Ana",
          "exercises": [
            {
              "id": "e_u2_0",
              "name": "Press banca inclinado con mancuernas",
              "description": "Pecho superior con menor estrés en hombro.",
              "sets": [
                { "index": 1, "weight": 12, "reps": 12 },
                { "index": 2, "weight": 14, "reps": 10 }
              ]
            },
            {
              "id": "e_u2_1",
              "name": "Remo en máquina",
              "description": "Trabajo de espalda media.",
              "sets": [
                { "index": 1, "weight": 35, "reps": 12 },
                { "index": 2, "weight": 40, "reps": 10 }
              ]
            },
            {
              "id": "e_u2_2",
              "name": "Elevaciones laterales",
              "description": "Aislamiento del deltoide medio.",
              "sets": [
                { "index": 1, "weight": 4, "reps": 15 },
                { "index": 2, "weight": 6, "reps": 12 }
              ]
            }
          ]
        },
        {
          "id": "w_u2_1",
          "name": "Lower body Ana",
          "exercises": [
            {
              "id": "e_u2_3",
              "name": "Sentadilla goblet",
              "description": "Sentadilla con mancuerna, controlada.",
              "sets": [
                { "index": 1, "weight": 16, "reps": 12 },
                { "index": 2, "weight": 18, "reps": 10 }
              ]
            },
            {
              "id": "e_u2_4",
              "name": "Hip thrust",
              "description": "Enfoque en glúteo.",
              "sets": [
                { "index": 1, "weight": 50, "reps": 12 },
                { "index": 2, "weight": 60, "reps": 10 }
              ]
            },
            {
              "id": "e_u2_5",
              "name": "Elevación de talones en máquina",
              "description": "Trabajo de pantorrilla.",
              "sets": [
                { "index": 1, "weight": 25, "reps": 15 },
                { "index": 2, "weight": 25, "reps": 12 }
              ]
            }
          ]
        }
      ]
    },
    {
      "id": "u3",
      "perfil": {
        "nombre": "Luis",
        "apellido": "Torres",
        "edad": 40,
        "genero": "Masculino",
        "peso_kg": 85,
        "altura_cm": 175,
        "frecuencia_entrenamiento": "2 veces por semana",
        "historial_lesiones": true,
        "zona_lesion": "Espalda baja"
      },
      "workouts": [
        {
          "id": "w_u3_0",
          "name": "Full body suave (espalda baja)",
          "exercises": [
            {
              "id": "e_u3_0",
              "name": "Prensa horizontal",
              "description": "Trabajo de piernas con soporte lumbar.",
              "sets": [
                { "index": 1, "weight": 80, "reps": 12 },
                { "index": 2, "weight": 90, "reps": 10 }
              ]
            },
            {
              "id": "e_u3_1",
              "name": "Jalón al pecho agarre neutro",
              "description": "Menos estrés en hombro y espalda baja.",
              "sets": [
                { "index": 1, "weight": 35, "reps": 12 },
                { "index": 2, "weight": 40, "reps": 10 }
              ]
            },
            {
              "id": "e_u3_2",
              "name": "Plancha isométrica",
              "description": "Trabajo de core sin carga axial.",
              "sets": [
                { "index": 1, "weight": 0, "reps": 30 },
                { "index": 2, "weight": 0, "reps": 30 }
              ]
            }
          ]
        }
      ]
    }
  ]
}
];
