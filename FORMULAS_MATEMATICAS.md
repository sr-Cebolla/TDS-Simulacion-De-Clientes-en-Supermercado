# 📐 Fórmulas Matemáticas - Simulación de Supermercado

## 📖 Descripción General

Este documento contiene todas las fórmulas matemáticas utilizadas en la simulación del supermercado, basadas en el modelo de **cola finita M/M/s/c/K** (sistema con llegadas Poisson, tiempos de servicio exponenciales, c servidores y capacidad máxima K).

---

## 🎯 Parámetros del Sistema

### 📊 Variables Principales
- **λ (lambda)**: Tasa de llegada de clientes (clientes/segundo)
- **μ (mu)**: Tasa de servicio por cajero (clientes/segundo)
- **c**: Número de cajeros (servidores) disponibles
- **s**: Número de cajeros (servidores) disponibles
- **K**: Capacidad máxima del sistema (clientes totales permitidos)
- **ρ (rho)**: Factor de utilización del sistema

### 🔢 Constantes del Sistema
- **Capacidad por cajero**: K = 10 clientes por cajero
- **Capacidad total**: K_total = c × 10
- **Distribución de prioridades**:
  - Normal: 70% (factor tiempo = 1.0)
  - Premium: 20% (factor tiempo = 0.8)
  - Express: 10% (factor tiempo = 0.6)

---

## 📐 Fórmulas Implementadas

### 1. 📈 **Utilización del Sistema**
Mide el porcentaje de capacidad del sistema que está siendo utilizada.

```
Utilización (%) = (Clientes_Activos / Capacidad_Máxima) × 100

Donde:
- Clientes_Activos = Σ(clientes en cola + clientes siendo atendidos)
- Capacidad_Máxima = c × 10
```

**Código implementado:**
```python
utilizacion = (clientes_activos / max_clientes * 100) if max_clientes > 0 else 0
```

### 2. 🚪 **Probabilidad de Rechazo**
Porcentaje de clientes que no pueden entrar al sistema por estar lleno.

```
P_rechazo (%) = (Clientes_Perdidos / Total_Intentos) × 100

Donde:
- Total_Intentos = Clientes_Atendidos + Clientes_Perdidos
```

**Código implementado:**
```python
total_intentos = self.clientes_atendidos + self.clientes_perdidos
prob_rechazo = (self.clientes_perdidos / max(1, total_intentos)) * 100
```

### 3. ⏰ **Tiempo Promedio de Espera**
Tiempo promedio que un cliente espera en cola antes de ser atendido.

```
W_espera = Tiempo_Espera_Acumulado / Clientes_Atendidos

Donde:
- Tiempo_Espera_Acumulado = Σ(tiempo_actual - tiempo_llegada) para cada cliente
```

**Código implementado:**
```python
tiempo_prom_espera = self.tiempo_espera_acumulado / max(1, self.clientes_atendidos)
```

### 4. 🔄 **Throughput (Rendimiento)**
Número de clientes procesados por unidad de tiempo.

```
Throughput = (Clientes_Atendidos / Tiempo_Simulación) × 60

Unidades: clientes por minuto
```

**Código implementado:**
```python
throughput = (self.clientes_atendidos / max(1, self.reloj)) * 60 if self.reloj > 0 else 0
```

### 5. ⚡ **Eficiencia del Sistema**
Porcentaje de clientes que logran ser atendidos respecto al total generado.

```
Eficiencia (%) = (Clientes_Atendidos / Clientes_Totales_Generados) × 100
```

**Código implementado:**
```python
eficiencia = (self.clientes_atendidos / max(1, self.clientes_totales_generados)) * 100
```

### 6. 📏 **Longitud Promedio de Cola**
Número promedio de clientes esperando en todas las colas.

```
L_cola = Σ(longitud_cola_i) / c

Donde:
- longitud_cola_i = número de clientes en la cola del cajero i
- c = número total de cajeros
```

**Código implementado:**
```python
longitud_prom_cola = sum(len(cajero.cola) for cajero in self.cajeros) / max(1, len(self.cajeros))
```

---

## ⏱️ Fórmulas de Tiempo de Servicio

### 7. 🛒 **Tiempo de Atención Base**
Tiempo base que toma atender a un cliente sin considerar prioridades.

```
T_base = productos × TIEMPO_POR_PRODUCTO × (10 / VELOCIDAD_CAJERO)

Donde:
- productos = número aleatorio entre 1 y 30
- TIEMPO_POR_PRODUCTO = 0.5 segundos (configurable)
- VELOCIDAD_CAJERO = 1-10 (configurable)
```

### 8. 🎨 **Tiempo de Atención Ajustado por Prioridad**
Tiempo real considerando el tipo de cliente.

```
T_ajustado = T_base × Factor_Prioridad

Factores de Prioridad:
- Normal (70%): Factor = 1.0
- Premium (20%): Factor = 0.8 (20% más rápido)
- Express (10%): Factor = 0.6 (40% más rápido)
```

**Código implementado:**
```python
factor_tiempo = {1: 1.0, 2: 0.8, 3: 0.6}.get(prioridad, 1.0)
tiempo_atencion_ajustado = tiempo_atencion * factor_tiempo
```

### 9. ⏳ **Cálculo de Tiempo de Espera Individual**
Tiempo que un cliente específico esperó desde su llegada.

```
T_espera_cliente = Tiempo_Actual - Tiempo_Llegada
```

**Código implementado:**
```python
def calcular_tiempo_espera(self, tiempo_actual):
    return tiempo_actual - self.tiempo_llegada
```

---

## 🎲 Fórmulas de Generación Estocástica

### 10. 👥 **Generación de Clientes con Prioridad**
Distribución probabilística para asignar tipos de clientes.

```
P(tipo) = rand() donde rand() ∈ [0,1]

Si rand < 0.7  → Normal   (70%)
Si 0.7 ≤ rand < 0.9 → Premium  (20%)
Si rand ≥ 0.9  → Express (10%)
```

### 11. 📦 **Generación de Productos por Cliente**
Número aleatorio de productos que lleva cada cliente.

```
productos = random.randint(1, 30)
```

### 12. 🎯 **Tasa de Llegada Dinámica**
Probabilidad de que llegue un nuevo cliente en cada frame.

```
P(llegada) = random.random() < TASA_LLEGADA_BASE

Donde TASA_LLEGADA_BASE es configurable (0.01 - 0.10)
```

---

## 🏗️ Fórmulas de Posicionamiento Gráfico

### 13. 📐 **Posicionamiento Dinámico de Cajeros**
Cálculo automático de posiciones Y para cajeros basado en altura de ventana.

```
margen_superior = 120
espacio_disponible = altura_ventana - margen_superior - 150
espacio_entre = min(ESPACIO_ENTRE_CAJEROS, espacio_disponible / max(1, num_cajeros - 1))
posicion_y[i] = margen_superior + i × espacio_entre
```

### 14. 🎯 **Alineación de Clientes con Cajeros**
Posicionamiento de clientes para alinearse con el centro de los cajeros.

```
cajero_center_y = cajero.y + (altura_sprite_cajero / 2)
cliente_y = cajero_center_y - 30
cliente_x[i] = inicio_cola_x - (i × offset_x)

Donde:
- offset_x = 60 píxeles (espacio entre clientes)
- inicio_cola_x = cajero.x - 80
```

### 15. 🚶 **Movimiento Suave de Clientes**
Algoritmo de interpolación para movimiento fluido.

```
dx = objetivo_x - x_actual
dy = objetivo_y - y_actual
distancia = √(dx² + dy²)

Si distancia > 2:
    x_nuevo = x_actual + (dx / distancia) × velocidad
    y_nuevo = y_actual + (dy / distancia) × velocidad
Sino:
    x_nuevo = objetivo_x
    y_nuevo = objetivo_y
```

---

## 📊 Fórmulas de Métricas Derivadas

### 16. 🎯 **Factor de Utilización Teórico**
Basado en teoría de colas M/M/c/K.

```
ρ = λ / (c × μ)

Donde:
- λ = tasa de llegada efectiva
- μ = tasa de servicio por cajero
- c = número de cajeros
```

### 17. 📈 **Throughput Efectivo**
Considerando rechazos por capacidad limitada.

```
λ_efectiva = λ × (1 - P_rechazo)
Throughput_efectivo = λ_efectiva × 60  (clientes/minuto)
```

### 18. 🔄 **Tiempo Promedio en el Sistema (Ley de Little)**
Relación entre clientes en sistema y tiempo de permanencia.

```
W_sistema = L_sistema / λ_efectiva

Donde:
- L_sistema = número promedio de clientes en el sistema
- λ_efectiva = tasa de llegada efectiva
```

---

## 🧮 Parámetros de Configuración

### Rangos de Valores
- **Tasa de Llegada**: 0.01 - 0.10 (slider: 1-10)
- **Tiempo por Producto**: 0.1 - 1.0 segundos (slider: 1-10)
- **Velocidad de Cajero**: 1 - 10
- **Número de Cajeros**: 1 - 8
- **Capacidad por Cajero**: 10 clientes (fijo)

### Conversiones de Sliders
```
TASA_LLEGADA_BASE = slider_value / 100
TIEMPO_POR_PRODUCTO = slider_value / 10
```

---

## 📝 Notas Importantes

1. **Prevención de División por Cero**: Todas las fórmulas usan `max(1, denominador)` para evitar errores.

2. **Precisión Decimal**: Los resultados se muestran con 1 decimal usando `.1f` en el formateo.

3. **Unidades de Tiempo**: 
   - Simulación interna: segundos
   - Throughput: clientes por minuto
   - Tiempos de espera: segundos

4. **Límites del Sistema**:
   - Capacidad máxima: 8 cajeros × 10 clientes = 80 clientes
   - Productos por cliente: 1-30 (aleatorio)
   - Prioridades: 3 tipos con factores fijos

---

*Fórmulas extraídas del código fuente de `colafinita.py` - Simulación de Supermercado M/M/c/K*
