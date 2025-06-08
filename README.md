# 🛒 Simulación de Supermercado - Modelo de Cola Finita

## 📋 Descripción del Proyecto

Simulación interactiva de un sistema de supermercado que implementa el modelo de **cola finita** (M/M/S/K) para el análisis de rendimiento de sistemas de servicio. El proyecto permite estudiar el comportamiento de clientes y cajeros en tiempo real, calculando métricas importantes como tiempos de espera, utilización del sistema y probabilidades de rechazo.

## 🎯 Características Principales

### 🔧 Funcionalidades del Sistema
- **Modelo de Cola Finita**: Capacidad limitada del sistema (N clientes máximo)
- **Múltiples Servidores**: Hasta 8 cajeros simultáneos
- **Sistema de Prioridades**: Clientes normales (70%), premium (20%) y express (10%)
- **Parámetros Ajustables**: Tasa de llegada, tiempo de servicio, velocidad de cajeros
- **Visualización en Tiempo Real**: Animaciones fluidas y métricas actualizadas
- **Interface Redimensionable**: Ventana adaptable con resolución de 1400x1020
- **Efectos Visuales Avanzados**: Sombras, gradientes y efectos de "glow" para cajeros activos

### 📊 Métricas y Análisis
- **Utilización del Sistema**: Porcentaje de capacidad en uso
- **Throughput**: Clientes atendidos por minuto
- **Probabilidad de Rechazo**: Porcentaje de clientes perdidos
- **Tiempo Promedio de Espera**: Estadística clave de rendimiento
- **Eficiencia del Sistema**: Ratio de clientes atendidos vs. generados
- **Longitud Promedio de Cola**: Análisis de congestión

### 🎮 Controles Interactivos
- **Sliders**: Ajuste dinámico de parámetros (Tasa de llegada: 1-10, Tiempo por producto: 1-10)
- **Botones**: Control de simulación (Reset/Pausa/Start/Export)
- **Controles de Cajeros**: Botones para agregar/quitar cajeros con contador visual
- **Teclado**: Atajos rápidos para modificar el sistema
- **Ventana Redimensionable**: Interface adaptable con reposicionamiento automático

## 🔧 Mejoras Técnicas Implementadas

### 🎨 Mejoras Visuales
- **Paleta de Colores Profesional**: Esquema de colores moderno con verde esmeralda, azul brillante y gradientes
- **Fuentes Optimizadas**: Uso de Segoe UI como fuente principal con fallback a Arial
- **Efectos de Profundidad**: Sombras y efectos de "glow" para elementos activos
- **Animaciones Fluidas**: Movimiento suave de clientes con velocidad ajustable (2.0 píxeles/frame)
- **Interface Adaptable**: Reposicionamiento automático de elementos al redimensionar ventana

### ⚡ Optimizaciones de Rendimiento
- **Limitación de FPS**: Control de 60 FPS para mejor rendimiento
- **Gestión Eficiente de Sprites**: Carga optimizada de imágenes con escalado automático
- **Algoritmos de Cola Optimizados**: Uso de `deque` para operaciones O(1)
- **Redistribución Inteligente**: Algoritmo equitativo para reasignar clientes al eliminar cajeros

### 🛠️ Funcionalidades Avanzadas
- **Posicionamiento Dinámico**: Cálculo automático de posiciones de cajeros basado en altura de ventana
- **Alineación Inteligente**: Clientes alineados horizontalmente con el centro de cajeros
- **Sistema de Prioridades Avanzado**: Factores de tiempo dinámicos según tipo de cliente
- **Métricas en Tiempo Real**: Cálculo continuo de estadísticas del sistema

## 📖 Documentación Adicional

Para información detallada sobre controles y casos de uso educativos, consulta:
- **`CONTROLES.md`**: Guía completa de controles, atajos de teclado y casos de estudio educativos

## 🚀 Requisitos e Instalación

### Dependencias
```bash
pip install pygame
```

### Ejecución
```bash
python "colafinita.py"
```

## 🎯 Controles de la Simulación

### ⌨️ Controles de Teclado
| Tecla | Función |
|-------|---------|
| `ESPACIO` | Pausar/Reanudar simulación |
| `↑` | Agregar cajero (máximo 8) |
| `↓` | Quitar cajero (mínimo 1) |
| `←` | Reducir velocidad cajero |
| `→` | Aumentar velocidad cajero |

### 🖱️ Controles de Mouse
- **Sliders**: Ajustar tasa de llegada (1-10) y tiempo por producto (1-10)
- **Botón Reset**: Reiniciar simulación
- **Botón Pausa**: Pausar simulación
- **Botón Start**: Reanudar simulación
- **Botón Export**: Exportar resultados a JSON
- **Botones de Cajeros**: Agregar (+), quitar (-) cajeros y visualizar contador

## 📈 Interpretación de Métricas

### 🔢 Métricas de Rendimiento
- **Utilización (0-100%)**: Mayor utilización = sistema más eficiente
- **Throughput (clientes/min)**: Velocidad de procesamiento del sistema
- **Prob. Rechazo (0-100%)**: Menor rechazo = mejor capacidad del sistema
- **Tiempo Espera (segundos)**: Menor tiempo = mejor experiencia del cliente

### 🎨 Sistema de Prioridades
- **🟢 Normal (70%)**: Clientes regulares con tiempo de servicio estándar
- **🔵 Premium (20%)**: Servicio 20% más rápido (factor 0.8)
- **🔴 Express (10%)**: Servicio 40% más rápido (factor 0.6)

### 🎨 Elementos Visuales
- **Sprites Dinámicos**: 8 tipos diferentes de clientes con colores distintivos
- **Indicadores de Prioridad**: Símbolos ★ (Premium) y ⚡ (Express) con badges circulares
- **Barras de Progreso**: Visualización colorida del tiempo de atención con colores dinámicos
- **Efectos de Sombra**: Profundidad visual para clientes y elementos UI
- **Gradientes**: Fondos modernos con transiciones suaves

## 📁 Estructura del Proyecto

```
Simulacion de Supermercado/
├── colafinita.py    # Archivo principal de la simulación (versión actualizada)
├── CONTROLES.md             # Guía detallada de controles y casos de uso
├── README.md                # Documentación del proyecto
└── assets/                  # Recursos gráficos
    ├── female.png           # Sprite cliente femenino
    ├── male.png             # Sprite cliente masculino
    ├── rob.png              # Sprite robot
    ├── zom.png              # Sprite zombie
    ├── register.png         # Sprite caja registradora
    ├── cart.png             # Sprite carrito de compras
    └── kenney_*/            # Paquetes de assets adicionales
        ├── kenney_mini-market/
        ├── kenney_rpg-urban-pack/
        ├── kenney_toon-characters-1/
        └── kenney_voxel-pack/
```

## 🧮 Modelo Matemático

### Parámetros del Sistema M/M/c/N
- **λ (lambda)**: Tasa de llegada de clientes
- **μ (mu)**: Tasa de servicio por cajero
- **c**: Número de cajeros (servidores)
- **N**: Capacidad máxima del sistema

### Fórmulas Implementadas
- **Utilización**: ρ = λ/(c×μ)
- **Probabilidad de Rechazo**: P(N)
- **Tiempo Promedio en Sistema**: W = L/λ_efectiva
- **Throughput**: λ_efectiva = λ × (1 - P(rechazo))

## 📊 Exportación de Datos

El sistema genera archivos JSON con:
- Timestamp de la simulación
- Parámetros utilizados
- Estadísticas completas
- Historial de tiempos de espera

Formato: `simulacion_supermercado_YYYYMMDD_HHMMSS.json`

## 🎓 Aplicaciones Educativas

### Conceptos de Teoría de Colas
- **Sistemas M/M/S/C/K**: Modelo de cola finita con múltiples servidores
- **Análisis de Rendimiento**: Métricas de sistemas de servicio
- **Optimización de Recursos**: Balance entre costo y calidad de servicio
- **Simulación Discreta**: Modelado de eventos discretos

### Casos de Estudio
1. **Análisis de Capacidad**: ¿Cuántos cajeros necesita el supermercado?
   - Observar utilización del sistema con diferentes números de cajeros
   - Encontrar el punto de equilibrio entre costo y eficiencia
2. **Impacto de Prioridades**: Efecto de clientes VIP en el sistema
   - Analizar cómo los clientes Premium y Express afectan tiempos de espera
   - Estudiar la distribución de 70% normales, 20% premium, 10% express
3. **Optimización de Parámetros**: Encontrar el equilibrio óptimo
   - Ajustar tasa de llegada (1-10 clientes/segundo) y tiempo por producto
   - Modificar velocidad de cajeros (1-10) para diferentes escenarios
4. **Análisis de Sensibilidad**: Cómo afectan los cambios en parámetros
   - Usar controles en tiempo real para ver impacto inmediato
   - Exportar datos para análisis posterior

### 📊 Métricas Educativas Clave
- **Capacidad Máxima**: 10 clientes por cajero (sistema M/M/c/K)
- **Algoritmo de Asignación**: Cola más corta para distribución equitativa
- **Factores de Tiempo**: Normal (1.0), Premium (0.8), Express (0.6)
- **Redistribución**: Algoritmo inteligente al eliminar cajeros

## 🔮 Posibles Extensiones

### 🎯 Extensiones Funcionales
- **Diferentes Distribuciones**: Implementar distribuciones no exponenciales (Normal, Poisson)
- **Horarios Pico**: Variación temporal de la tasa de llegada según horas del día
- **Múltiples Tipos de Servicio**: Diferentes cajeros especializados (autoservicio, caja rápida)
- **Análisis Estadístico**: Gráficos de tendencias y distribuciones en tiempo real
- **Modo Batch**: Simulación automática de múltiples escenarios con parámetros variables

### 🎨 Extensiones Visuales
- **Mapas de Calor**: Visualización de zonas de congestión
- **Gráficos Dinámicos**: Histogramas y líneas de tendencia en tiempo real
- **Modo 3D**: Visualización tridimensional del supermercado
- **Temas Personalizables**: Diferentes esquemas de colores y estilos visuales
- **Animaciones Avanzadas**: Transiciones más complejas y efectos de partículas

### 📊 Extensiones Analíticas
- **Machine Learning**: Predicción de patrones de llegada de clientes
- **Optimización Automática**: Algoritmos genéticos para encontrar configuraciones óptimas
- **Comparación de Escenarios**: Análisis A/B de diferentes configuraciones
- **Reportes Avanzados**: Generación automática de informes PDF con gráficos
- **Base de Datos**: Almacenamiento persistente de simulaciones históricas

## 👨‍🎓 Información Académica

**Curso**: Técnicas de Simulación  
**Universidad**: UES 2025 Ciclo 1  
**Tema**: Simulación de Sistemas de Colas Finitas  
**Tecnología**: Python + Pygame  

---

*Desarrollado como herramienta educativa para el estudio de sistemas de colas y simulación de eventos discretos.*
