# 🎵 TP0: Lanzamiento del Proyecto — SoundNode

## 1. Datos del Proyecto
* **Nombre del Proyecto:** SoundNode
* **Dominio Elegido:** Música (Canciones, Artistas, Géneros y Puntuaciones)
* **Integrantes:** Gustavo Ojeda, Natanael Contardo Ceriani, Julian Ttito

---

## 2. Definición del Dominio y Problema
* **¿Por qué elegimos este dominio?:** 
  La música es un dominio interconectado por naturaleza. Nos permite trabajar con datasets reales de canciones y aplicar de manera clara estructuras como listas, árboles de búsqueda, jerarquías de géneros, colas de prioridad (heaps) y grafos para recomendaciones.
* **Problema que resuelve:** 
  Ayuda a los usuarios a descubrir nueva música relacionada con sus gustos, explorar géneros específicos y encontrar rankings según puntuaciones sin perderse en catálogos extensos.
* **Usuario Objetivo:** 
  Ariel, un estudiante melómano de 22 años que escucha bandas de rock y pop, y busca un sistema rápido de consola para descubrir canciones similares y navegar por rankings.

---

## 3. Cinco Funcionalidades Iniciales
1. **Buscar elemento:** Búsqueda rápida por título de canción o nombre de artista.
2. **Explorar por géneros:** Filtrar el catálogo según el género o subgénero musical.
3. **Ver Top Rankings:** Mostrar las N canciones con mejor puntuación (uso de Heaps en etapas posteriores).
4. **Obtener recomendaciones:** Sugerir canciones afines en base a similitud o relaciones (uso de Grafos).
5. **Encontrar conexiones:** Descubrir el camino de colaboraciones o relación entre dos artistas.

---

## 4. Boceto de Interfaz de Consola (Mockup CLI) y Diagrama UML

```text
================================================
        🎵 SOUNDNODE — TERMINAL 🎵
================================================

1. Buscar canción o artista
2. Explorar categorías y géneros
3. Ver Top 5 más valoradas
4. Obtener recomendaciones de una canción
5. Encontrar conexión entre dos artistas
0. Salir

------------------------------------------------
Opción: _

> Opción seleccionada: 4
> Ingrese canción: In the End

╔═════════════════════════════════════════════════╗
║ 🎵 Si te gustó "In the End" (Linkin Park)       ║
║ te recomendamos:                                ║
║                                                 ║
║ 1. Numb - Linkin Park             ⭐ 9.4       ║
║ 2. Enter Sandman - Metallica      ⭐ 9.6       ║
║ 3. Seven Nation Army - White Stripes ⭐ 9.0     ║
╚═════════════════════════════════════════════════╝

+-------------------------------------------------------+
|                       Cancion                         |
+-------------------------------------------------------+
| - _id: int                                            |
| - _titulo: str                                        |
| - _artista: str                                       |
| - _genero: str                                        |
| - _duracion: str                                      |
| - _puntuacion: float                                  |
+-------------------------------------------------------+
| + id(): int                                           |
| + titulo(): str                                       |
| + artista(): str                                      |
| + genero(): str                                       |
| + duracion(): str                                     |
| + puntuacion(): float                                 |
+-------------------------------------------------------+
                            ^
                            | contiene (1..*)
+-------------------------------------------------------+
|                       Catalogo                        |
+-------------------------------------------------------+
| - _canciones: list[Cancion]                           |
+-------------------------------------------------------+
| + agregar_cancion(cancion: Cancion): void             |
| + obtener_todas(): list[Cancion]                      |
| + buscar(texto: str): list[Cancion]                   |
| + filtrar_por_genero(genero: str): list[Cancion]      |
| + obtener_top_puntuadas(limite: int): list[Cancion]   |
+-------------------------------------------------------+