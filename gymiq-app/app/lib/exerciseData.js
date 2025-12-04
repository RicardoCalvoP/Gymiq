export const WORKOUT_DATA = [
  {
    "usuarios": [
      {
        "id": "u1",
        "perfil": {
          "nombre": "Carlos",
          "apellido": "Ramírez",
          "edad": 28,
          "imc": 24.1,
          "peso_usuario": 78,
          "sexo": "M",
          "historial_lesion_tipo": "leve",
          "historial_lesion_tiempo_semanas": 12,
          "dolor_actual": "no_dolor",
          "altura_cm": 180,
          "frecuencia_entrenamiento": "4 veces por semana"
        },
        "workouts": [
          {
            "id": "w_u1_0",
            "name": "Push personalizado Carlos",
            "sesion_num": 0,
            "exercises": [
              {
                "id": "e_u1_0",
                "name": "Press banca con barra",
                "description": "Movimiento principal de empuje horizontal.",
                "reps_objetivo": 8,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 90.0,
                    "reps": 10,
                    "peso_kg_actual": 90.0,
                    "reps_realizadas": 10,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 90.0,
                    "reps": 8,
                    "peso_kg_actual": 90.0,
                    "reps_realizadas": 8,
                    "rpe_real": 8.0
                  },
                  {
                    "index": 3,
                    "weight": 90.0,
                    "reps": 6,
                    "peso_kg_actual": 90.0,
                    "reps_realizadas": 6,
                    "rpe_real": 8.5
                  }
                ]
              },
              {
                "id": "e_u1_1",
                "name": "Press militar con barra",
                "description": "Empuje vertical para hombro.",
                "reps_objetivo": 8,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 40.0,
                    "reps": 10,
                    "peso_kg_actual": 40.0,
                    "reps_realizadas": 10,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 40.0,
                    "reps": 8,
                    "peso_kg_actual": 40.0,
                    "reps_realizadas": 8,
                    "rpe_real": 8.0
                  },
                  {
                    "index": 3,
                    "weight": 40.0,
                    "reps": 6,
                    "peso_kg_actual": 40.0,
                    "reps_realizadas": 6,
                    "rpe_real": 8.5
                  }
                ]
              },
              {
                "id": "e_u1_2",
                "name": "Fondos en paralelas asistidos",
                "description": "Trabajo de tríceps y pecho con asistencia.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 5.0,
                    "reps": 12,
                    "peso_kg_actual": 5.0,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 5.0,
                    "reps": 10,
                    "peso_kg_actual": 5.0,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  },
                  {
                    "index": 3,
                    "weight": 5.0,
                    "reps": 8,
                    "peso_kg_actual": 5.0,
                    "reps_realizadas": 8,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u1_3",
                "name": "Aperturas con mancuernas en banco plano",
                "description": "Aislamiento de pectoral con recorrido controlado.",
                "reps_objetivo": 12,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 14.0,
                    "reps": 12,
                    "peso_kg_actual": 14.0,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 14.0,
                    "reps": 10,
                    "peso_kg_actual": 14.0,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u1_4",
                "name": "Jalón en polea alta agarre cerrado",
                "description": "Enfoque en dorsales y bíceps, complementa el trabajo de empuje.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 50.0,
                    "reps": 12,
                    "peso_kg_actual": 50.0,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 50.0,
                    "reps": 10,
                    "peso_kg_actual": 50.0,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u1_5",
                "name": "Extensión de tríceps en polea",
                "description": "Trabajo de tríceps con agarre en barra recta.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 30.0,
                    "reps": 12,
                    "peso_kg_actual": 30.0,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 30.0,
                    "reps": 10,
                    "peso_kg_actual": 30.0,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  },
                  {
                    "index": 3,
                    "weight": 30.0,
                    "reps": 8,
                    "peso_kg_actual": 30.0,
                    "reps_realizadas": 8,
                    "rpe_real": 8.5
                  }
                ]
              }
            ]
          },
          {
            "id": "w_u1_1",
            "name": "Legs (adaptado rodilla)",
            "sesion_num": 1,
            "exercises": [
              {
                "id": "e_u1_6",
                "name": "Prensa de piernas",
                "description": "Menos carga en rodilla que la sentadilla libre.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 100,
                    "reps": 12,
                    "peso_kg_actual": 100,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 120,
                    "reps": 10,
                    "peso_kg_actual": 120,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  },
                  {
                    "index": 3,
                    "weight": 130,
                    "reps": 8,
                    "peso_kg_actual": 130,
                    "reps_realizadas": 8,
                    "rpe_real": 8.5
                  }
                ]
              },
              {
                "id": "e_u1_7",
                "name": "Peso muerto rumano",
                "description": "Trabajo de isquios y glúteo con énfasis en la bisagra de cadera.",
                "reps_objetivo": 8,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 50,
                    "reps": 10,
                    "peso_kg_actual": 50,
                    "reps_realizadas": 10,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 60,
                    "reps": 8,
                    "peso_kg_actual": 60,
                    "reps_realizadas": 8,
                    "rpe_real": 8.0
                  },
                  {
                    "index": 3,
                    "weight": 60,
                    "reps": 8,
                    "peso_kg_actual": 60,
                    "reps_realizadas": 8,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u1_8",
                "name": "Curl femoral sentado",
                "description": "Aislamiento de isquios.",
                "reps_objetivo": 12,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 30,
                    "reps": 12,
                    "peso_kg_actual": 30,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 35,
                    "reps": 10,
                    "peso_kg_actual": 35,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u1_9",
                "name": "Extensión de cuádriceps",
                "description": "Trabajo de cuádriceps con control para cuidar la rodilla.",
                "reps_objetivo": 12,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 25,
                    "reps": 15,
                    "peso_kg_actual": 25,
                    "reps_realizadas": 15,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 30,
                    "reps": 12,
                    "peso_kg_actual": 30,
                    "reps_realizadas": 12,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u1_10",
                "name": "Desplantes",
                "description": "Trabajo unilateral de pierna, rango moderado por rodilla.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 14,
                    "reps": 10,
                    "peso_kg_actual": 14,
                    "reps_realizadas": 10,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 16,
                    "reps": 8,
                    "peso_kg_actual": 16,
                    "reps_realizadas": 8,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u1_11",
                "name": "Abducción de cadera en máquina",
                "description": "Enfoque en glúteo medio, carga moderada.",
                "reps_objetivo": 15,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 35,
                    "reps": 15,
                    "peso_kg_actual": 35,
                    "reps_realizadas": 15,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 40,
                    "reps": 12,
                    "peso_kg_actual": 40,
                    "reps_realizadas": 12,
                    "rpe_real": 8.0
                  }
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
          "imc": 22.8,
          "peso_kg": 62,
          "sexo": "F",
          "historial_lesion_tipo": "ninguna",
          "historial_lesion_tiempo_semanas": 0,
          "dolor_actual": "no_dolor",
          "altura_cm": 165,
          "frecuencia_entrenamiento": "3 veces por semana"
        },
        "workouts": [
          {
            "id": "w_u2_0",
            "name": "Upper body Ana",
            "sesion_num": 0,
            "exercises": [
              {
                "id": "e_u2_0",
                "name": "Press banca inclinado con barra",
                "description": "Pecho superior con menor estrés en hombro.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 12,
                    "reps": 12,
                    "peso_kg_actual": 12,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 14,
                    "reps": 10,
                    "peso_kg_actual": 14,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  },
                  {
                    "index": 3,
                    "weight": 16,
                    "reps": 8,
                    "peso_kg_actual": 16,
                    "reps_realizadas": 8,
                    "rpe_real": 8.5
                  }
                ]
              },
              {
                "id": "e_u2_1",
                "name": "Remo sentado en polea baja",
                "description": "Trabajo de espalda media.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 35,
                    "reps": 12,
                    "peso_kg_actual": 35,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 40,
                    "reps": 10,
                    "peso_kg_actual": 40,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u2_2",
                "name": "Elevaciones laterales",
                "description": "Aislamiento del deltoide medio.",
                "reps_objetivo": 12,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 4,
                    "reps": 15,
                    "peso_kg_actual": 4,
                    "reps_realizadas": 15,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 6,
                    "reps": 12,
                    "peso_kg_actual": 6,
                    "reps_realizadas": 12,
                    "rpe_real": 8.0
                  },
                  {
                    "index": 3,
                    "weight": 6,
                    "reps": 10,
                    "peso_kg_actual": 6,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u2_3",
                "name": "Jalón en polea alta agarre cerrado",
                "description": "Trabajo de dorsales con menos estrés en los hombros.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 30,
                    "reps": 12,
                    "peso_kg_actual": 30,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 35,
                    "reps": 10,
                    "peso_kg_actual": 35,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u2_4",
                "name": "Curl con mancuernas",
                "description": "Trabajo de bíceps alterno de pie.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 7,
                    "reps": 12,
                    "peso_kg_actual": 7,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 8,
                    "reps": 10,
                    "peso_kg_actual": 8,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u2_5",
                "name": "Extensión de tríceps con cuerda",
                "description": "Enfoque en tríceps con mayor rango de movimiento.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 18,
                    "reps": 12,
                    "peso_kg_actual": 18,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 20,
                    "reps": 10,
                    "peso_kg_actual": 20,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  }
                ]
              }
            ]
          },
          {
            "id": "w_u2_1",
            "name": "Lower body Ana",
            "sesion_num": 1,
            "exercises": [
              {
                "id": "e_u2_6",
                "name": "Sentadilla con barra",
                "description": "Sentadilla con mancuerna, controlada.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 16,
                    "reps": 12,
                    "peso_kg_actual": 16,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 18,
                    "reps": 10,
                    "peso_kg_actual": 18,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  },
                  {
                    "index": 3,
                    "weight": 20,
                    "reps": 8,
                    "peso_kg_actual": 20,
                    "reps_realizadas": 8,
                    "rpe_real": 8.5
                  }
                ]
              },
              {
                "id": "e_u2_7",
                "name": "Hip thrust",
                "description": "Enfoque en glúteo.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 60,
                    "reps": 12,
                    "peso_kg_actual": 60,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 70,
                    "reps": 10,
                    "peso_kg_actual": 70,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  },
                  {
                    "index": 3,
                    "weight": 75,
                    "reps": 8,
                    "peso_kg_actual": 75,
                    "reps_realizadas": 8,
                    "rpe_real": 8.5
                  }
                ]
              },
              {
                "id": "e_u2_8",
                "name": "Elevación de talones de pie (pantorrilla)",
                "description": "Trabajo de pantorrilla.",
                "reps_objetivo": 15,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 30,
                    "reps": 15,
                    "peso_kg_actual": 30,
                    "reps_realizadas": 15,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 35,
                    "reps": 12,
                    "peso_kg_actual": 35,
                    "reps_realizadas": 12,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u2_9",
                "name": "Peso muerto rumano",
                "description": "Trabajo de isquios y glúteo con menor carga axial.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 18,
                    "reps": 12,
                    "peso_kg_actual": 18,
                    "reps_realizadas": 12,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 20,
                    "reps": 10,
                    "peso_kg_actual": 20,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u2_10",
                "name": "Patada de glúteo en polea",
                "description": "Trabajo de glúteo medio y estabilidad de cadera.",
                "reps_objetivo": 15,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 10,
                    "reps": 15,
                    "peso_kg_actual": 10,
                    "reps_realizadas": 15,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 12,
                    "reps": 12,
                    "peso_kg_actual": 12,
                    "reps_realizadas": 12,
                    "rpe_real": 8.0
                  }
                ]
              },
              {
                "id": "e_u2_11",
                "name": "Desplantes",
                "description": "Trabajo unilateral de pierna, enfoque en cuádriceps y glúteo.",
                "reps_objetivo": 10,
                "rpe_objetivo": 8.0,
                "sets": [
                  {
                    "index": 1,
                    "weight": 8,
                    "reps": 10,
                    "peso_kg_actual": 8,
                    "reps_realizadas": 10,
                    "rpe_real": 7.5
                  },
                  {
                    "index": 2,
                    "weight": 8,
                    "reps": 10,
                    "peso_kg_actual": 8,
                    "reps_realizadas": 10,
                    "rpe_real": 8.0
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
];//n