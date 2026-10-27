# Guía del lenguaje Instinct

## Índice

1. [Visión general](#1-visión-general)
2. [Estructura de un archivo `.ins`](#2-estructura-de-un-archivo-ins)
3. [La cabecera](#3-la-cabecera)
4. [El cuerpo: tipos de línea](#4-el-cuerpo-tipos-de-línea)
5. [Léxico: nombres, palabras reservadas y comentarios](#5-léxico-nombres-palabras-reservadas-y-comentarios)
6. [Tipos y expresiones](#6-tipos-y-expresiones)
7. [Variables](#7-variables)
8. [Las siete acciones básicas](#8-las-siete-acciones-básicas)
9. [Percepciones, constantes y funciones `see` / `name`](#9-percepciones-constantes-y-funciones-see--name)
10.[Resumen](#10-resumen)

---

## 1. Visión general

- Cada **especie** de criatura se define en un archivo de texto con extensión **`.ins`**.
- Una criatura es, en esencia, un **ciclo infinito de condicionales** que decide qué hacer según lo que percibe de sí misma, del mapa y de su entorno.
- Los tipos de dato son solo dos: **enteros** y **texto**.
- Las criaturas interactúan con el mundo mediante **acciones** (con forma de llamada a función), y lo observan mediante **percepciones** (variables de solo lectura) y **funciones** (`see`, `name`).
- Los errores de compilación se reportan **con número de línea**.

---

## 2. Estructura de un archivo `.ins`

Un archivo tiene exactamente **dos partes**:

| Parte | Contenido | Dónde termina/empieza |
|---|---|---|
| **Cabecera** | Atributos de la especie (5 claves obligatorias) | Todo lo que aparece **antes** de la etiqueta `start:` |
| **Cuerpo** | Comportamiento de la criatura | Empieza en la etiqueta obligatoria `start:` |

```
# uruk.ins                  <- comentario
creature Uruk               <- cabecera
faction isengard
health 80
vision 6
lifespan 400

start:                      <- cuerpo
    if health < 20 goto flee
    ...
```

---

## 3. La cabecera

Cada línea de la cabecera tiene la forma:

```
id valor
```

- La **primera línea no vacía** debe ser `creature Name`.
- Los otros **cuatro** ids pueden ir en **cualquier orden**.
- **Las cinco claves son obligatorias**: si falta una, el archivo no compila.

| Clave | Significado | Restricción |
|---|---|---|
| `creature Name` | Nombre de la especie. Identifica el archivo en la aplicación. | Debe ir primero. |
| `faction Name` | Facción. Dos criaturas son **aliadas** si sus facciones son la misma cadena de texto; **enemigas** en otro caso. Varias especies pueden compartir facción. | — |
| `health N` | Vida inicial. **No hay vida máxima**: se puede acumular tanta como se consiga. Baja 1 por tick; al llegar a 0 la criatura muere. | `N > 0` |
| `vision N` | Radio (en casillas) en el que la criatura percibe su entorno. También limita hasta dónde puede mirar con `see` y `name`. | `N >= 1` |
| `lifespan N` | Esperanza de vida en ticks. Cuando la edad alcanza este valor, la criatura muere de vieja. | `N > 0` |

> Todas las criaturas ocupan **exactamente una casilla**.

---

## 4. El cuerpo: tipos de línea

El cuerpo es una secuencia de líneas. **Cada línea es una (y solo una)** de estas cosas:

| Línea | Qué hace |
|---|---|
| `# texto` | **Comentario.** Se ignora. También se puede poner al final de cualquier línea. |
| `nombre:` | **Etiqueta.** Marca un punto al que se puede saltar. **No consume turno.** |
| `goto nombre` | **Salto incondicional** a la etiqueta. |
| `if expr goto nombre` | **Salto condicional**: salta si la expresión es verdadera. |
| `nombre = expr` | **Asignación.** Crea la variable si no existía. No se puede asignar a una percepción ni a una constante. |
| `accion(arg, arg, ...)` | **Acción.** Una llamada sola en su línea, con o sin argumentos. |

Observaciones importantes:

- **No hay bloques** ni `else`: `if` siempre tiene la forma `if expr goto etiqueta`.
- La indentación es libre y **no significa nada**.
- Las etiquetas pueden "caer" una sobre otra: si la ejecución llega a una etiqueta sin saltar, simplemente continúa con la línea siguiente.
- La etiqueta `start:` es **obligatoria**.

---

## 5. Léxico: nombres, palabras reservadas y comentarios

### Palabras reservadas

Solo hay **cinco**:

```
if   goto   and   or   not
```

Todo lo demás (acciones, funciones, percepciones, constantes) son **nombres que el intérprete resuelve contra su catálogo**.

### Reglas de los nombres

- Empiezan por **letra o guion bajo** (`_`).
- Siguen con letras, dígitos o guiones bajos.
- Se **distingue entre mayúsculas y minúsculas** (`GROUND` ≠ `ground`).

### Comentarios e indentación

- `# ...` hasta el final de la línea (sola o al final de otra).
- Indentación libre.

---

## 6. Tipos y expresiones

### 6.1 Tipos

| Tipo | Ejemplos |
|---|---|
| **Entero** | `0`, `42`, `-7` |
| **Texto** | `"grass"`, `"AWOOO"`, `""` |

### 6.2 Qué puede formar una expresión

- Literales enteros y de texto (entre comillas **dobles**).
- Variables propias, percepciones y constantes.
- Llamadas a funciones reservadas, con argumentos entre paréntesis separados por comas. En la base hay dos: `see(x, y)` y `name(x, y)`.
- **Aritmética:** `+`, `-`, `*`, `/` (división **entera**, como `//` de Python), `%` (resto), menos unario, paréntesis.
- **Comparaciones:** `<`, `<=`, `>`, `>=`, `==`, `!=`. Valen **1** si son ciertas y **0** si no.
- **Lógica:** `and`, `or`, `not`. Devuelven **0 o 1**.

### 6.3 Precedencia (de mayor a menor)

| Nivel | Operadores |
|---|---|
| 1 (más alta) | paréntesis y llamadas |
| 2 | menos unario, `not` |
| 3 | `*`, `/`, `%` |
| 4 | `+`, `-` |
| 5 | comparaciones (`<`, `<=`, `>`, `>=`, `==`, `!=`) |
| 6 | `and` |
| 7 (más baja) | `or` |

### 6.4 Reglas de tipos

| Operadores | Regla |
|---|---|
| Aritméticos (`+ - * / %`) y de orden (`< <= > >=`) | **Solo aceptan números.** |
| `==` y `!=` | Aceptan números o texto, pero **ambos lados deben tener el mismo tipo**. |
| Texto | **Solo** admite `==` y `!=` (no hay concatenación en la base). |
| Lógicos (`and`, `or`, `not`) | **Excepción**: aceptan cualquier combinación de tipos, porque no comparan nada. |

Mezclar un entero y un texto en un operador (salvo los lógicos) provoca un **error en tiempo de ejecución**.

### 6.5 Valor de verdad

| Valor | ¿Verdadero o falso? |
|---|---|
| El entero `0` | **Falso** |
| El texto vacío `""` | **Falso** |
| Cualquier otro entero o texto | **Verdadero** |

### 6.6 Argumentos de las acciones

- `move`, `attack`, `consume`, `reproduce` y `wait` esperan **números**: si reciben texto → error de ejecución.
- `roar` y `say` aceptan **cualquier valor** (un número se muestra como cifra).

---

## 7. Variables

- Se crean al **asignarlas por primera vez** (`pasos = 0`). No hay declaración.
- Pueden guardar un **entero o un texto**, y pueden **cambiar de tipo** al reasignarlas (como en Python).
- **Conservan su valor entre turnos** → permiten tener *memoria* (contar peleas, recordar hacia dónde iba, guardar la posición de su casa).
- Leer una variable **antes de asignarla** es un error de ejecución.
- **No se pueden asignar** las percepciones ni las constantes (error de compilación).
- **No se heredan:** una cría nace **sin ninguna variable**, aunque su madre las tuviera.
- Nombres como `dx`, `dy`, `home_x` o `steps` son variables normales: no son reservadas.

---

## 8. Las siete acciones básicas

**Direcciones:** se dan con dos números `dx` y `dy`, cada uno en `{-1, 0, 1}`.

- `dx = 1` → derecha; `dx = -1` → izquierda.
- `dy = 1` → **abajo**; `dy = -1` → arriba.
- Ambos distintos de 0 → **diagonal**.

Un `dx` o `dy` fuera de `{-1, 0, 1}` es un **error de ejecución**.

### Resumen

| Acción | Argumentos | Consume turno | Efecto resumido |
|---|---|:---:|---|
| `wait` | `n` | Sí | No hace nada durante `n` turnos seguidos. |
| `move` | `dx, dy, speed` | Sí | Avanza hasta `speed` casillas en la dirección dada. |
| `attack` | `dx, dy, damage` | Sí | Golpea lo que haya en la casilla adyacente. |
| `consume` | `dx, dy, damage, heal` | Sí | Como `attack`, y además gana `heal` de vida. |
| `reproduce` | `dx, dy, health` | Sí | Crea una cría de la misma especie en la casilla adyacente. |
| `roar` | `value` | Sí | Emite un rugido que otras criaturas pueden oír. |
| `say` | `value` | **No** | Muestra un texto sobre la criatura o en el registro. |

> **Toda acción salvo `say` consume el turno, tenga éxito o no.**

### Detalle de cada acción

#### `wait(n)`
- No hace nada durante `n` turnos seguidos.
- Si `n < 1`, cuenta como `1`.
- Mientras espera **no está protegida**: pierde vida, envejece y puede ser atacada.

#### `move(dx, dy, speed)`
- Avanza **hasta** `speed` casillas en la dirección `(dx, dy)`, **una a una**.
- Se detiene **antes de la primera casilla que no pueda pisar**: fuera del mapa, con objeto o con criatura.
- Consume **un solo turno** aunque avance varias casillas.

#### `attack(dx, dy, damage)`
Golpea lo que haya en la casilla **adyacente** en dirección `(dx, dy)`:

| Objetivo | Efecto |
|---|---|
| Criatura | Pierde `damage` de **vida**. |
| Objeto | Pierde `damage` de **reserva**. |
| Solo terreno | El terreno pierde `damage` de **reserva**. |
| `(0, 0)` | El objetivo es el **terreno bajo la propia criatura**. |

- Siempre **cuerpo a cuerpo** (distancia 1, diagonales incluidas).
- Si el objetivo está **fuera del mapa**, la acción no hace nada.
- Si deja a una criatura con vida ≤ 0, **muere ahí mismo** y su casilla pasa a ser solo terreno.

#### `consume(dx, dy, damage, heal)`
- Igual que `attack`, **y además** la criatura gana `heal` puntos de vida.
- **Sin tope:** el lenguaje no relaciona `heal` con `damage` ni con lo que tenía el objetivo. Poner límites sensatos es responsabilidad de quien programa la criatura.
- Interpretación temática libre: comer, hacer fotosíntesis, minar, etc.

#### `reproduce(dx, dy, health)`
- Crea una criatura de la **misma especie** (mismo archivo, misma facción) en la casilla adyacente `(dx, dy)`.
- **Requisitos:** la casilla debe tener **solo terreno** y la madre debe tener **más de `health`** puntos de vida.
- **Efectos:** la madre pierde `health` de vida; la cría nace con esa vida, **edad 0**, **sin variables** y con su programa en `start:`.
- Si algo falla → "aborto natural" (no pasa nada, pero el turno se consume).
- La cría recibe su primer turno **en el tick siguiente** al de su nacimiento.

#### `roar(value)`
- Emite un rugido.
- Las criaturas que lo oigan (dentro de su radio de visión) pueden leer su texto en el **tick siguiente** (`roars_near`, `last_roar`).
- La interfaz visual debe mostrarlo de alguna manera.

#### `say(value)`
- Muestra un texto sobre la criatura o en el registro de la aplicación.
- Es la **única acción que no consume turno** → se puede usar libremente antes de otra acción.

---

## 9. Percepciones, constantes y funciones `see` / `name`

Las criaturas ven el mundo de **dos maneras**:

1. **Percepciones:** variables de **solo lectura** que el **simulador** rellena al comienzo de cada turno.
2. **Funciones** (`see`, `name`): permiten preguntar por **cualquier casilla** dentro del radio de visión, con **coordenadas absolutas del canvas**.

### 9.1 Constantes devueltas por `see(x, y)`

| Constante | Valor | Significado |
|---|:---:|---|
| `NONE` | `-1` | Casilla **fuera del radio de visión** (distancia > `vision`). No se sabe qué hay. **Se comprueba antes que todo lo demás.** |
| `GROUND` | `0` | Solo hay terreno. Se puede pisar. |
| `OBJECT` | `1` | Hay un objeto (una roca, por ejemplo). No se puede pisar. Las coordenadas **fuera del mapa pero dentro del radio de visión** también devuelven `OBJECT` (el borde actúa como muro indestructible). |
| `ALLY` | `2` | Hay una criatura de la **misma facción** que quien pregunta (**la propia casilla devuelve `ALLY`**). |
| `ENEMY` | `3` | Hay una criatura de **otra facción**. |

### 9.2 `name(x, y)`

Devuelve un **texto** con el nombre de lo que hay en esa casilla:

| Si en la casilla hay... | Devuelve |
|---|---|
| Una criatura | El nombre de su **especie** |
| Un objeto | El nombre del **objeto** (p. ej. `"Rock"`) |
| Nada más | El nombre del **terreno** (p. ej. `"Grass"`) |
| Casilla fuera del radio de visión o fuera del mapa | `""` (texto vacío) |

Sirve para distinguir cosas (hierba/agua, roca/árbol) **sin que el lenguaje conozca de antemano** los nombres inventados por cada estudiante.

### 9.3 Percepciones sobre sí misma

| Percepción | Significado |
|---|---|
| `health` | Vida actual. |
| `age` | Edad en ticks (nunca menor que 0). |
| `lifespan` | Esperanza de vida (atributo de la cabecera). |
| `vision` | Radio de visión (atributo de la cabecera). |
| `species` | **Texto**: nombre de su especie. |
| `faction` | **Texto**: nombre de su facción. |
| `x`, `y` | Posición en el mapa. La casilla superior izquierda es `(0, 0)`; `x` crece hacia la derecha e `y` hacia abajo. |
| `terrain_here` | **Texto**: nombre del terreno bajo la criatura. |
| `reserve_here` | Reserva del terreno bajo la criatura. |

### 9.4 Percepciones sobre el mundo

| Percepción | Significado |
|---|---|
| `width`, `height` | Tamaño del mapa en casillas. |
| `tick` | Número del tick actual. |
| `total_creatures`, `total_allies`, `total_enemies` | Cuántas criaturas hay **vivas en todo el mapa** (sin contarse a sí misma). |
| `random` | Entero aleatorio entre **0 y 99**, **distinto cada vez que se lee**. Es la única fuente de aleatoriedad del lenguaje. |

> ⚠️ `random` se evalúa **de verdad cada vez que aparece**: `random - random` casi nunca da 0. Toda la aleatoriedad del simulador (esta percepción y el sorteo del orden de turnos) debería salir de **un mismo generador con semilla**, para poder repetir una simulación idéntica.

### 9.5 Percepciones sobre lo cercano

Se calculan **dentro del radio `vision`**. La distancia entre dos casillas es el **mayor** de los desplazamientos en `x` e `y` (distancia de Chebyshev), así que las **ocho casillas vecinas están a distancia 1**.

| Percepción | Significado |
|---|---|
| `allies_near`, `enemies_near`, `objects_near` | Cuántos hay dentro del radio de visión. |
| `enemy_dist`, `enemy_dx`, `enemy_dy` | Distancia al **enemigo más cercano** y dirección hacia él (`dx`, `dy` ∈ `{-1, 0, 1}`, listos para pasarlos a `move`, `attack` o `consume`). Si no hay ninguno visible: `enemy_dist = -1` y direcciones `0`. |
| `ally_dist`, `ally_dx`, `ally_dy` | Lo mismo para el **aliado** más cercano. |
| `object_dist`, `object_dx`, `object_dy` | Lo mismo para el **objeto** más cercano. |
| `roars_near` | Cuántas criaturas **rugieron en el tick anterior** dentro del radio de visión. |
| `last_roar` | **Texto**: lo que decía el último de esos rugidos, o `""` si no oyó ninguno. |

- Si hay **varios candidatos a la misma distancia**, se elige uno cualquiera, pero **se mantiene siempre el mismo** mientras la situación no cambie.
- Con `see` y `name` se puede ver lo que las percepciones no cuentan, recorriendo las casillas del radio de visión.

---

## 10. Resumen

### Estructura

```
creature N / faction N / health N / vision N / lifespan N     (5 obligatorias)
start:
  ...cuerpo...
```

### Líneas

```
# comentario            etiqueta:            goto etiqueta
if expr goto etiqueta   variable = expr      accion(args)
```

### Reservadas

```
if  goto  and  or  not
```

### Operadores (mayor → menor precedencia)

```
( ) llamadas  >  - unario, not  >  * / %  >  + -  >  < <= > >= == !=  >  and  >  or
```

### Acciones

```
wait(n)                         # espera n turnos (n<1 → 1)
move(dx, dy, speed)             # hasta speed casillas, 1 turno
attack(dx, dy, damage)          # cuerpo a cuerpo
consume(dx, dy, damage, heal)   # attack + ganar vida
reproduce(dx, dy, health)       # cría con 'health' de vida cedida por la madre
roar(value)                     # rugido, se oye en el tick siguiente
say(value)                      # NO consume turno
```

### Constantes de `see`

```
NONE = -1   GROUND = 0   OBJECT = 1   ALLY = 2   ENEMY = 3
```

### Percepciones

| Grupo | Nombres |
|---|---|
| Propias | `health`, `age`, `lifespan`, `vision`, `species`, `faction`, `x`, `y`, `terrain_here`, `reserve_here` |
| Mundo | `width`, `height`, `tick`, `total_creatures`, `total_allies`, `total_enemies`, `random` |
| Cercanas | `allies_near`, `enemies_near`, `objects_near`, `enemy_dist/dx/dy`, `ally_dist/dx/dy`, `object_dist/dx/dy`, `roars_near`, `last_roar` |

### Funciones

```
see(x, y)    → NONE | GROUND | OBJECT | ALLY | ENEMY
name(x, y)   → texto con el nombre de lo que hay ("" si fuera de visión o mapa)
```

### Límites y errores clave

| Concepto | Valor / regla |
|---|---|
| Líneas máximas por turno | **100** (luego, como `wait(1)`) |
| `random` | Entero en **[0, 99]** |
| `dx`, `dy` | Solo `-1`, `0`, `1` |
| División | Entera; dividir por 0 → error de ejecución |
| Tipos | Entero y texto; no se mezclan salvo en `and`/`or`/`not` |
| Falso | `0` y `""`; todo lo demás es verdadero |
| Cabecera | 5 claves obligatorias; `creature` primera; `health>0`, `vision>=1`, `lifespan>0` |
| Primer turno de una cría | En el **tick siguiente** a su nacimiento |
