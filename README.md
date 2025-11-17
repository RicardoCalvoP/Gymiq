<div align="center">

<img src="https://wiki.labnuevoleon.mx/images/4/4b/Tec-de-monterrey-logo.png" alt="Gymiq logo" width="400"/>

## INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY

**Campus Santa Fe**

## Proyecto Final

_Oct 27_

## Alumnos:

Ricardo Alfredo Calvo Pérez - A01028889

Melissa Mireles Rendón - Matrícula: A01379736

### Analítica de datos y herramientas de inteligencia artificial II

**Grupo 502**

</div>

## Índice

1. [Descripción general](#descripción-general)
2. [Fundamento teórico](#fundamento-teórico)
   - [Fundamentos fisiológicos del entrenamiento de fuerza](#fundamentos-fisiológicos-del-entrenamiento-de-fuerza)
   - [La fórmula de Epley](#la-fórmula-de-epley)
   - [Escala RPE y percepción del esfuerzo](#escala-rpe-y-percepción-del-esfuerzo)
3. [Justificación](#justificación)
4. [Objetivos](#objetivos)
   - [Objetivo general](#objetivo-general)
   - [Objetivos específicos](#objetivos-específicos)
5. [Metodología](#metodología)
   - [Fase 1. Registro de datos](#fase-1-registro-de-datos)
   - [Fase 2. Cálculo del 1RM estimado (fórmula de Epley)](#fase-2-cálculo-del-1rm-estimado-fórmula-de-epley)
   - [Fase 3. Cálculo del % de intensidad y RPE automático](#fase-3-cálculo-del--de-intensidad-y-rpe-automático)
   - [Fase 4. Recomendación adaptativa](#fase-4-recomendación-adaptativa)
   - [Fase 5. Aprendizaje del modelo](#fase-5-aprendizaje-del-modelo)
6. [Herramientas tecnológicas](#herramientas-tecnológicas)
7. [Conclusión](#conclusión)
8. [Referencias](#referencias)

# Proyecto: Modelo Predictivo para la Optimización del Entrenamiento de Fuerza en el Gimnasio

## Descripción general

El entrenamiento de fuerza es un proceso complejo que involucra adaptaciones fisiológicas, neuromusculares y metabólicas. La capacidad máxima de fuerza de un atleta (1RM o “una repetición máxima”) es un indicador clave de rendimiento, pero su medición directa puede representar **riesgos de lesión y fatiga excesiva**, especialmente en deportistas principiantes o en periodos de alta carga.

Por ello, la fisiología del ejercicio ha desarrollado métodos indirectos, como la **[fórmula de Epley (1985)](https://www.maxcalculator.com/guides/epley-formula/)**, que permite **estimar el 1RM** a partir del peso levantado y el número de repeticiones submáximas. Este cálculo se ha validado empíricamente en numerosos estudios de ciencias del deporte y ofrece un método seguro, confiable y práctico para controlar el progreso de fuerza.

El presente proyecto propone el desarrollo de un modelo predictivo inteligente, fundamentado en principios fisiológicos, metodologías deportivas y técnicas de analítica de datos, capaz de:

- Estimar el 1RM de forma automatizada.
- Calcular el %1RM (intensidad relativa).
- Estimar el RPE automático (Rate of Perceived Exertion o esfuerzo percibido).
- Generar recomendaciones inteligentes sobre si mantener, reducir o aumentar la carga.

Todo ello con el objetivo de optimizar la progresión muscular y prevenir el sobreentrenamiento.

## Fundamento teórico

### Fundamentos fisiológicos del entrenamiento de fuerza

El rendimiento en ejercicios de fuerza depende de tres factores fisiológicos principales:

1. Capacidad neuromuscular: eficiencia en la activación de unidades motoras.

1. Adaptaciones musculares: aumento del área transversal de las fibras musculares.

1. Factores metabólicos y hormonales: disponibilidad de ATP-CP y hormonas anabólicas.

La intensidad y el volumen del entrenamiento determinan la magnitud de estas adaptaciones. En fisiología del ejercicio, se recomienda trabajar dentro de rangos de intensidad expresados como porcentaje del 1RM (%1RM).

<div align="center">
<br>

| Objetivo fisiológico | %1RM recomendado | Repeticiones | RPE típico |
| -------------------- | ---------------- | ------------ | ---------- |
| Fuerza máxima        | 85–100%          | 1–6          | 8.5–10     |
| Hipertrofia          | 70–85%           | 6–12         | 7–8        |
| Resistencia muscular | 60–70%           | 12–20        | 6–7        |

<br>
</div>

La relación entre repeticiones y %1RM es la base fisiológica que el sistema utiliza para **estimar el RPE automático**.

### La fórmula de Epley

La ecuación desarrollada por Boyd Epley (1985) se expresa como:

$$
1RM = PesoLevantado \times (1 + 0.0333 \times Repeticiones)
$$

Esta fórmula ha sido validada por la National Strength and Conditioning Association (NSCA) como una herramienta precisa para estimar el 1RM sin necesidad de exponer al atleta a una carga máxima.

_Ejemplo: calculo de 1RM_

    Si un atleta levanta 100 kg × 6 repeticiones:

    100 kg x (1 + 0.0333 x 6) ≈ 119.98 kg
    1RM ≈ 118

### Escala RPE y percepción del esfuerzo

El **RPE (Rate of Perceived Exertion)** fue introducido por Gunnar Borg (1982) y adaptado al entrenamiento de fuerza por Mike Tuchscherer (2010). Esta escala permite medir el **esfuerzo percibido**, correlacionando el número de repeticiones restantes antes del fallo.

Sin embargo, la percepción subjetiva puede variar entre individuos. Por ello, el modelo calcula un **RPE automático**, derivado del %1RM y el número de repeticiones realizadas, utilizando una tabla empírica de correlaciones:

<div align="center">

<img src="https://ktarsisendurance.com/wp-content/uploads/2022/03/A-tener-en-cuenta.png" alt="RPE Table" width="400"/>

</div>

## Justificación

El entrenamiento moderno busca la individualización de las cargas. Sin embargo, la mayoría de los deportistas ajusta sus pesos según sensaciones subjetivas o intuición. Esto genera:

- Riesgo de sobreentrenamiento o fatiga acumulada.
- Estancamiento en la progresión de fuerza.
- Falta de control sobre la intensidad real del estímulo.

El modelo propuesto sustituye esta subjetividad por un enfoque **cuantitativo, adaptativo y basado en datos**, que combina fisiología del ejercicio y analítica predictiva.
El sistema aprende del historial del atleta y propone ajustes automáticos para mantener una progresión óptima sin comprometer la recuperación.

## Objetivos

### Objetivo General

Desarrollar un modelo predictivo que utilice la fórmula de Epley y variables de entrenamiento para estimar el esfuerzo real (RPE automático) y generar recomendaciones inteligentes sobre la carga ideal, promoviendo una progresión segura, individualizada y eficaz.

### Objetivos específicos

1. Registrar de forma estructurada los datos de entrenamiento.
1. Calcular el 1RM estimado por ejercicio.
1. Obtener el %1RM y el RPE automático.
1. Implementar reglas adaptativas de recomendación (mantener/aumentar/reducir carga).
1. Visualizar la evolución de la fuerza y validar la precisión del modelo.

## Metodología

El desarrollo del modelo se divide en cinco fases principales:

### Fase 1. Registro de datos

    El usuario solo debe registrar los valores básicos de cada sesión:

- Ejercicio:
  - Peso levantado
    - Repeticiones realizadas
- Fecha

_Ejemplo: Input del usuario_

    Sentadilla: 100 kg × 6 repeticiones (día 2025-11-01)

**Estos datos se almacenan en un archivo CSV o base de datos SQL, permitiendo el seguimiento histórico.**

### Fase 2. Cálculo del 1RM estimado (fórmula de Epley)

$$
1RM = PesoLevantado \times (1 + 0.0333 \times Repeticiones)
$$

_Ejemplo: calculo de 1RM_

    100 kg x (1 + 0.0333 x 6) ≈ 119.98 kg
    1RM ≈ 118

$$
1RM \approx 118 kg
$$

**Sacar promédio de 1RM**

$$
1RM_{mean} = \frac{\sum 1RM_n}{n}
$$

En donde $n$ representa el número de series completadas en ese ejercicio.

_Ejemplo: calculo de Promedio de 1RM_

    Si el atleta hace 3 series:
    Promedio 1RM = (119.98+119.98+113.32)/3 = 117.76kg

**Representa la fuerza máxima teórica del atleta sin necesidad de prueba directa.**

### Fase 3. Cálculo del % de intensidad y RPE automático

$$
 \% 1RM = \frac{Peso \space usado}{1RM \space estimado} \times  100
$$

_Ejemplo: calculo de %1RM y RPE_

    Usando el RM estimado calculado anteriormente (117.76%):
    %1RM = (100 / 118) x 100 ≈ 84.7%

**RPE estimado = 8 (esfuerzo óptimo)**

<div align="center">
<br>
<b>Tabla de referencia (Tuchscherer, 2010):</b>
<br><br>

| %1RM    | Reps posibles | RPE estimado |
| ------- | ------------- | ------------ |
| 95–100% | 1–2           | 9.5–10       |
| 90–94%  | 3–4           | 9            |
| 85–89%  | 5–6           | 8            |
| 80–84%  | 7–8           | 7.5          |
| 75–79%  | 9–10          | 7            |
| 70–74%  | 11–12         | 6.5          |

<br>

</div>

**Si %1RM = 84.7% y reps = 6 → RPE = 8.**

### Fase 4. Recomendación adaptativa

El sistema aplica una lógica condicional

<div align="center">
<br>

<table>
  <thead>
    <tr style="background-color:#cccccc; color:black;">
      <th>Rango de %1RM y RPE</th>
      <th>Interpretación fisiológica</th>
      <th>Recomendación</th>
      <th>Acción sugerida</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color:#a8e6a3; color:black;">
      <td>80–85% del 1RM RPE ≤ 8</td>
      <td>Esfuerzo óptimo, carga adecuada para estímulo de fuerza e hipertrofia</td>
      <td>Mantener carga actual</td>
      <td>Mantén el peso y repeticiones; estás en el rango ideal de trabajo.</td>
    </tr>
    <tr style="background-color:#fff3b0; color:black;">
      <td>&lt; 80% del 1RM RPE ≤ 7</td>
      <td>Carga ligera, estímulo insuficiente para progreso de fuerza</td>
      <td>Aumentar 2.5–5 kg</td>
      <td>Incrementa ligeramente la carga para alcanzar una intensidad más efectiva.</td>
    </tr>
    <tr style="background-color:#f8a8a8; color:black;">
      <td>&gt; 90% del 1RM RPE ≥ 9</td>
      <td>Fatiga alta, riesgo de sobrecarga o sobreentrenamiento</td>
      <td>Reducir 2.5–5 kg</td>
      <td>Disminuye la carga para favorecer la recuperación y evitar lesiones.</td>
    </tr>
  </tbody>
</table>

</div>

- **Zona verde (80–85%, RPE ≤ 8):** ideal para progreso sostenido.
- **Zona amarilla (<80%, RPE ≤ 7):** entrenamiento muy liviano, ajustar al alza.
- **Zona roja (>90%, RPE ≥ 9):** esfuerzo excesivo, posible fatiga, ajustar a la baja.

_Ejemplo: determinar peso a partir de condición_

    %1RM = 84.7%, RPE = 8 → Mantener 100 kg.

Si en la siguiente sesión hace 8 reps con el mismo peso $\rightarrow$ Aumentar a 102.5 kg.

### Fase 5: Aprendizaje del modelo

Cada sesión alimenta el sistema.

El modelo:

- Recalcula el 1RM estimado.
- Detecta tendencias de mejora o fatiga.
- Ajusta las recomendaciones futuras.

<p style="color:red;">
A mediano plazo puede evolucionar a un modelo de regresión lineal o red neuronal que prediga la carga óptima a partir de múltiples variables (historial, tipo de ejercicio, frecuencia, recuperación).
</p>

**Esquema general del sistema**:

<div align="center">
[Entrada de datos]

↓

[Procesamiento fisiológico: Epley + %1RM + RPE]

↓

[Motor de decisión adaptativa]

↓

[Aprendizaje automático]

↓

[Salida: recomendación de carga + visualización de progreso]

</div>

Este modelo conceptual combina la lógica de la fisiología del ejercicio con un enfoque de inteligencia adaptativa, permitiendo un control preciso y automatizado del entrenamiento.

## Herramientas tecnológicas

<div align="center">

| Área                               | Herramientas        |
| ---------------------------------- | ------------------- |
| Lenguaje de programación           | Python              |
| Librerías de análisis              | Pandas, NumPy       |
| Visualización                      | Matplotlib, Seaborn |
| Interfaz interactiva               | React               |
| Almacenamiento de datos (opcional) | CSV o Mongo         |
| Modelado predictivo                | Scikit-learn        |

</div>

## Conclusión

El proyecto integra ciencia fisiológica, inteligencia artificial y metodologías deportivas, logrando un sistema que aprende del rendimiento del atleta y genera recomendaciones seguras, precisas y personalizadas.
Este modelo representa un avance hacia el entrenamiento inteligente, donde los datos reemplazan la intuición y permiten una progresión óptima, segura y sostenible.

## Referencias

- Epley, B. (1985). Determination of one repetition maximum (1RM) without performing a maximum test. NSCA Journal, 6(4), 60–61.
- Tuchscherer, M. (2010). The reactive training manual: Developing your own custom training program. Reactive Training Systems.
- Zatsiorsky, V. M., & Kraemer, W. J. (2006). Science and practice of strength training (2nd ed.). Human Kinetics.
- Schoenfeld, B. J. (2010). The mechanisms of muscle hypertrophy and their application to resistance training. Journal of Strength and Conditioning Research, 24(10), 2857–2872. https://doi.org/10.1519/JSC.0b013e3181e840f3
