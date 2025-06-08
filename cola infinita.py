#Librerías necesarias
import pygame
import random
import os
from collections import deque
import math
import csv
from datetime import datetime

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Simulación de Supermercado - Modelo de Cola Finita")

# Variables globales para tamaño de pantalla
current_width, current_height = WIDTH, HEIGHT

# Colores profesionales con paleta mejorada
WHITE = (255, 255, 255)
BLACK = (35, 35, 35)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (200, 200, 200)
GREEN = (46, 204, 113)  # Verde esmeralda
RED = (231, 76, 60)     # Rojo pomelo
BLUE = (52, 152, 219)   # Azul brillante
ORANGE = (230, 126, 34) # Naranja zanahoria
PURPLE = (155, 89, 182) # Amatista
YELLOW = (241, 196, 15) # Amarillo sol
TURQUOISE = (26, 188, 156) # Turquesa
BACKGROUND = (245, 248, 250) # Fondo más claro
PANEL_BG = (255, 255, 255)   # Fondo de paneles
SLIDER_BG = (180, 180, 180)
SLIDER_HANDLE = (100, 100, 100)
ACCENT_COLOR = (52, 73, 94)  # Color acento para elementos importantes
ACCENT_COLOR_LIGHT = (72, 93, 114)  # Versión más clara del color acento
GRADIENT_TOP = (41, 128, 185)  # Azul más profundo para gradientes
GRADIENT_BOTTOM = (52, 152, 219)  # Azul más claro para gradientes

# Fuentes con estilo moderno
# Intentamos usar fuentes más modernas si están disponibles
try:
    FONT_LARGE = pygame.font.SysFont("Segoe UI", 22, bold=True)
    FONT_MEDIUM = pygame.font.SysFont("Segoe UI", 18)
    FONT_SMALL = pygame.font.SysFont("Segoe UI", 14)
    FONT_TITLE = pygame.font.SysFont("Segoe UI", 24, bold=True)
except:
    # Fallback a Arial si no está disponible Segoe UI
    FONT_LARGE = pygame.font.SysFont("Arial", 22, bold=True)
    FONT_MEDIUM = pygame.font.SysFont("Arial", 18)
    FONT_SMALL = pygame.font.SysFont("Arial", 14)
    FONT_TITLE = pygame.font.SysFont("Arial", 24, bold=True)

# Parámetros de simulación
VELOCIDAD_CAJERO = 5
TIEMPO_POR_PRODUCTO = 0.5
NUM_CAJEROS_INICIAL = 3
TASA_LLEGADA_BASE = 0.02
FPS_LIMITE = 60  # Limitar FPS para mejor rendimiento

# Posicionamiento
MARGEN_DERECHO = 200
MARGEN_IZQUIERDO = 350
ESPACIO_ENTRE_CAJEROS = 200
POS_X_CAJEROS = WIDTH - MARGEN_DERECHO

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.dragging = False
        self.handle_radius = 8
    
    def interpolate_color(self, color1, color2, factor):
        """Interpola entre dos colores basado en un factor (0-1)"""
        return tuple(int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3))
    
    def get_value_color(self):
        """Obtiene el color basado en el valor del slider y su propósito"""
        # Normalizar el valor entre 0 y 1
        normalized = (self.val - self.min_val) / (self.max_val - self.min_val)
        
        if "Tasa" in self.label:
            # Para tasa de llegada: Verde (bajo) -> Amarillo (medio) -> Rojo (alto)
            if normalized < 0.5:
                # Verde a amarillo
                return self.interpolate_color(GREEN, YELLOW, normalized * 2)
            else:
                # Amarillo a rojo
                return self.interpolate_color(YELLOW, RED, (normalized - 0.5) * 2)
        else:
            # Para tiempo por producto: Verde (rápido) -> Amarillo (medio) -> Rojo (lento)
            if normalized < 0.5:
                # Verde a amarillo
                return self.interpolate_color(GREEN, YELLOW, normalized * 2)
            else:
                # Amarillo a rojo
                return self.interpolate_color(YELLOW, RED, (normalized - 0.5) * 2)
    
    def get_handle_color(self):
        """Color del handle basado en el valor"""
        value_color = self.get_value_color()
        # Hacer el handle un poco más oscuro que el track
        return tuple(max(0, c - 40) for c in value_color)
        
    def handle_pos(self):
        # Calcular posición del handle basado en el valor
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        return self.rect.x + ratio * self.rect.width
    
    def handle_event(self, event):
        handle_x = self.handle_pos()
        handle_rect = pygame.Rect(handle_x - self.handle_radius, 
                                 self.rect.centery - self.handle_radius,
                                 self.handle_radius * 2, 
                                 self.handle_radius * 2)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if handle_rect.collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                self.dragging = True
                # Actualizar valor inmediatamente
                mouse_x = event.pos[0]
                relative_x = mouse_x - self.rect.x
                ratio = max(0, min(1, relative_x / self.rect.width))
                self.val = self.min_val + ratio * (self.max_val - self.min_val)
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                return True
                
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            relative_x = mouse_x - self.rect.x
            ratio = max(0, min(1, relative_x / self.rect.width))
            self.val = self.min_val + ratio * (self.max_val - self.min_val)
            return True
            
        return False
    
    def draw(self, screen):
        # Obtener colores dinámicos
        track_color = self.get_value_color()
        handle_color = self.get_handle_color()
        
        # Fondo del slider (parte no llena)
        pygame.draw.rect(screen, SLIDER_BG, self.rect, border_radius=3)
        
        # Parte llena del slider con color dinámico
        fill_width = (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(screen, track_color, fill_rect, border_radius=3)
        
        # Borde del slider
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 1, border_radius=3)
        
        # Handle del slider con color dinámico
        handle_x = self.handle_pos()
        handle_y = self.rect.centery
        
        # Sombra del handle
        pygame.draw.circle(screen, (0, 0, 0, 50), (handle_x + 1, handle_y + 1), self.handle_radius)
        # Handle con color dinámico
        pygame.draw.circle(screen, WHITE, (handle_x, handle_y), self.handle_radius)
        pygame.draw.circle(screen, handle_color, (handle_x, handle_y), self.handle_radius, 3)
        
        # Etiqueta y valor con color dinámico para el valor
        label_text = FONT_SMALL.render(self.label, True, DARK_GRAY)
        value_text = FONT_SMALL.render(f"{self.val:.1f}", True, handle_color)
        
        screen.blit(label_text, (self.rect.x, self.rect.y - 20))
        screen.blit(value_text, (self.rect.right - value_text.get_width(), self.rect.y - 20))

class Button:
    def __init__(self, x, y, w, h, text, color=LIGHT_GRAY, text_color=BLACK):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover = False
        self.pressed = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed:
                self.pressed = False
                if self.rect.collidepoint(event.pos):
                    return True
        return False
    
    def draw(self, screen):
        # Color del botón según estado
        color = self.color
        if self.hover:
            color = tuple(min(255, c + 20) for c in self.color)
        if self.pressed:
            color = tuple(max(0, c - 20) for c in self.color)
            
        # Dibujar botón
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2, border_radius=5)
        
        # Texto centrado con fuente más pequeña para botones
        text_surface = FONT_SMALL.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

# --- Carga de imágenes ---
def load_image(name, scale=1.0):
    try:
        img = pygame.image.load(f"assets/{name}.png").convert_alpha()
        if scale != 1.0:
            new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
            img = pygame.transform.scale(img, new_size)
        return img
    except FileNotFoundError:
        print(f"Error: No se encontró assets/{name}.png")
        # Crear sprites más profesionales como fallback
        surf = pygame.Surface((40, 60), pygame.SRCALPHA)
        colors = [(BLUE), (GREEN), (ORANGE), (PURPLE), (RED)]
        color = random.choice(colors)
        pygame.draw.ellipse(surf, color, (5, 5, 30, 30))  # Cabeza
        pygame.draw.rect(surf, color, (10, 25, 20, 35))   # Cuerpo
        return surf

# Sprites para clientes con colores distintivos
client_sprites = []
client_colors = [BLUE, GREEN, ORANGE, PURPLE, RED, (255, 20, 147), (0, 191, 255), (50, 205, 50)]

for i in range(8):  # Crear 8 tipos diferentes de clientes
    try:
        sprite = load_image(["female", "male", "rob", "zom"][i % 4], 0.35)
        client_sprites.append(sprite)
    except:
        # Fallback con diferentes colores
        surf = pygame.Surface((40, 60), pygame.SRCALPHA)
        color = client_colors[i]
        pygame.draw.ellipse(surf, color, (5, 5, 30, 30))
        pygame.draw.rect(surf, color, (10, 25, 20, 35))
        client_sprites.append(surf)

# Sprite para cajeros mejorado
try:
    cashier_sprite = load_image("register", 1.2)
except:
    cashier_sprite = pygame.Surface((80, 60))
    cashier_sprite.fill(DARK_GRAY)
    pygame.draw.rect(cashier_sprite, LIGHT_GRAY, (10, 10, 60, 40))

class Cliente:
    def __init__(self, id, tiempo_llegada, prioridad=1):
        self.id = id
        self.productos = random.randint(1, 30)
        self.prioridad = prioridad  # 1=normal, 2=premium, 3=express
        self.sprite = random.choice(client_sprites)
        self.tiempo_atencion = self.productos * TIEMPO_POR_PRODUCTO * (10 / VELOCIDAD_CAJERO)
        self.x = -100
        self.y = 0
        self.objetivo_x = None
        self.objetivo_y = None
        self.velocidad = 2.0
        self.tiempo_llegada = tiempo_llegada
        self.color = self._get_priority_color()
    def _get_priority_color(self):
        colors = {1: BLACK, 2: BLUE, 3: RED}
        return colors.get(self.prioridad, BLACK)
        
    def calcular_tiempo_espera(self, tiempo_actual):
        return tiempo_actual - self.tiempo_llegada
    
    def dibujar(self, screen):
        # Sombra para dar efecto de profundidad
        shadow_offset = 2
        shadow_surface = pygame.Surface(self.sprite.get_size(), pygame.SRCALPHA)
        shadow_surface.fill((0, 0, 0, 60))
        screen.blit(shadow_surface, (self.x + shadow_offset, self.y + shadow_offset))
        
        # Dibujar sprite del cliente
        screen.blit(self.sprite, (self.x, self.y))
        
        # Número de productos con fondo y estilo moderno
        text = f"{self.productos}"
        text_surface = FONT_SMALL.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        
        # Fondo del texto según prioridad con bordes redondeados
        bg_color = {
            1: DARK_GRAY,  # Normal
            2: BLUE,       # Premium
            3: RED         # Express
        }.get(self.prioridad, DARK_GRAY)
        
        # Dibuja un círculo como fondo para el contador de productos
        circle_pos = (self.x + 24 + text_rect.width // 2, self.y - 20)
        circle_radius = max(text_rect.width // 2 + 6, 12)
        pygame.draw.circle(screen, bg_color, circle_pos, circle_radius)
        pygame.draw.circle(screen, BLACK, circle_pos, circle_radius, 1)  # Borde
        
        # Centra el texto en el círculo
        text_pos = (circle_pos[0] - text_rect.width // 2, circle_pos[1] - text_rect.height // 2)
        screen.blit(text_surface, text_pos)
        
        # Indicador de prioridad mejorado
        if self.prioridad > 1:
            # Símbolos más llamativos y coloridos
            if self.prioridad == 2:  # Premium
                symbol = "★"
                sym_color = YELLOW
            else:  # Express
                symbol = "⚡"
                sym_color = ORANGE
                
            # Fondo circular para el símbolo de prioridad
            priority_surface = FONT_MEDIUM.render(symbol, True, sym_color)
            pri_rect = priority_surface.get_rect()
            badge_radius = pri_rect.width // 2 + 4
            badge_pos = (self.x - 5 + pri_rect.width // 2, self.y - 15)
            
            # Dibuja círculo de fondo blanco con borde            
            pygame.draw.circle(screen, WHITE, badge_pos, badge_radius)
            pygame.draw.circle(screen, bg_color, badge_pos, badge_radius, 2)  # Borde del color del cliente
            # Posiciona el símbolo en el centro del círculo
            screen.blit(priority_surface, (badge_pos[0] - pri_rect.width // 2, badge_pos[1] - pri_rect.height // 2))
    
    def mover(self):
        if self.objetivo_x is not None and self.objetivo_y is not None:
            dx = self.objetivo_x - self.x
            dy = self.objetivo_y - self.y
            distancia = (dx**2 + dy**2)**0.5
            
            if distancia > 2:
                # Movimiento más suave con velocidad ajustada
                self.x += dx / distancia * self.velocidad
                self.y += dy / distancia * self.velocidad
            else:
                # Si estamos muy cerca del objetivo, simplemente nos posicionamos allí
                self.x = self.objetivo_x
                self.y = self.objetivo_y

class Cajero:
    def __init__(self, id, y):
        self.id = id
        self.x = POS_X_CAJEROS
        self.y = y
        self.sprite = cashier_sprite
        self.cola = deque()
        self.cliente_actual = None
        self.tiempo_inicio = 0
        self.clientes_atendidos_cajero = 0
        self.tiempo_inactivo = 0
        
    def dibujar(self, screen):
        # Área del cajero con borde y sombra
        shadow_offset = 4
        
        # Efecto de luz si el cajero está activo
        if self.cliente_actual:
            # Crear un efecto de "glow" alrededor del cajero activo
            glow_rect = pygame.Rect(self.x - 15, self.y - 45, 130, 110)
            glow_color = (52, 152, 219, 50)  # Azul con transparencia
            glow_surface = pygame.Surface((130, 110), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, glow_color, (0, 0, 130, 110), border_radius=12)
            screen.blit(glow_surface, (self.x - 15, self.y - 45))
            
            # Segunda capa de glow más intensa en el centro
            glow_inner = pygame.Rect(self.x - 12, self.y - 42, 124, 104)
            glow_inner_color = (52, 152, 219, 30)
            glow_inner_surface = pygame.Surface((124, 104), pygame.SRCALPHA)
            pygame.draw.rect(glow_inner_surface, glow_inner_color, (0, 0, 124, 104), border_radius=10)
            screen.blit(glow_inner_surface, (self.x - 12, self.y - 42))
        
        # Sombra del cajero
        shadow_rect = pygame.Rect(self.x - 10 + shadow_offset, self.y - 40 + shadow_offset, 120, 100)
        pygame.draw.rect(screen, (220, 220, 220), shadow_rect, border_radius=8)
        
        # Área del cajero con borde redondeado
        cajero_rect = pygame.Rect(self.x - 10, self.y - 40, 120, 100)
        pygame.draw.rect(screen, PANEL_BG, cajero_rect, border_radius=8)
        pygame.draw.rect(screen, ACCENT_COLOR, cajero_rect, 2, border_radius=8)
        
        # Título con gradiente suave (dos rectángulos para simular gradiente)
        header_rect = pygame.Rect(self.x - 10, self.y - 40, 120, 25)
        pygame.draw.rect(screen, GRADIENT_TOP, header_rect, border_top_left_radius=8, border_top_right_radius=8)
        header_bottom = pygame.Rect(self.x - 10, self.y - 40 + 12, 120, 13)
        pygame.draw.rect(screen, GRADIENT_BOTTOM, header_bottom)
        
        # Número del cajero (texto blanco sobre fondo azul)
        num_text = FONT_MEDIUM.render(f"Caja {self.id + 1}", True, WHITE)
        screen.blit(num_text, (self.x, self.y - 35))
        
        # Contador de clientes en cola con estilo mejorado
        cola_text = f"Cola: {len(self.cola)}"
        cola_surface = FONT_SMALL.render(cola_text, True, WHITE)
        screen.blit(cola_surface, (self.x + 60, self.y - 35))
        
        # Barra de progreso con estilo moderno y animación
        if self.cliente_actual:
            progreso = (pygame.time.get_ticks() - self.tiempo_inicio) / (self.cliente_actual.tiempo_atencion * 1000)
            barra_width = 100
            barra_height = 8
            barra_x = self.x - 5
            barra_y = self.y - 10
            
            # Fondo de la barra con borde redondeado
            pygame.draw.rect(screen, LIGHT_GRAY, (barra_x, barra_y, barra_width, barra_height), border_radius=4)
            
            # Calcular color dinámico para la barra de progreso
            if progreso < 0.6:
                bar_color = GREEN
            elif progreso < 0.8:
                bar_color = YELLOW
            else:
                bar_color = RED
                
            # Progreso de la barra con borde redondeado
            progress_width = barra_width * min(progreso, 1.0)
            if progress_width > 0:
                pygame.draw.rect(screen, bar_color, (barra_x, barra_y, progress_width, barra_height), border_radius=4)
            
            # Borde de la barra
            pygame.draw.rect(screen, DARK_GRAY, (barra_x, barra_y, barra_width, barra_height), 1, border_radius=4)
          # Cajero (sprite)
        screen.blit(self.sprite, (self.x, self.y))
        
        # Clientes en cola con alineación horizontal mejorada
        offset_x = 60  # Espacio horizontal entre clientes aumentado
        inicio_cola_x = self.x - 80  # Punto de inicio de la cola ajustado
        
        # Calcular la posición Y para alinear el centro del cliente con el centro del cajero
        cajero_center_y = self.y + (cashier_sprite.get_height() // 2)
        cliente_center_offset = 30  # Aproximadamente la mitad de la altura del sprite del cliente
        cliente_y = cajero_center_y - cliente_center_offset
        
        for i, cliente in enumerate(self.cola):
            # Calcular posición objetivo para cada cliente - alineados horizontalmente con el cajero
            cliente.objetivo_x = inicio_cola_x - (i * offset_x)
            cliente.objetivo_y = cliente_y  # Alineados con el centro del cajero
            
            # Mover y dibujar el cliente
            cliente.mover()
            cliente.dibujar(screen)
            
        # Cliente siendo atendido - mejor alineación
        if self.cliente_actual:
            self.cliente_actual.objetivo_x = self.x + cashier_sprite.get_width() + 15
            self.cliente_actual.objetivo_y = cliente_y  # Mismo nivel que la cola
            self.cliente_actual.mover()
            self.cliente_actual.dibujar(screen)
    
    def mover_clientes_cola(self, nuevo_x):
        # Posicionar cada cliente en una ubicación específica en la fila
        offset_x = 60  # Espacio horizontal entre clientes
        inicio_cola_x = nuevo_x - 80  # Punto de inicio de la cola
        
        # Calcular la posición Y para alinear con el centro del cajero
        cajero_center_y = self.y + (cashier_sprite.get_height() // 2)
        cliente_center_offset = 30
        cliente_y = cajero_center_y - cliente_center_offset
        
        for i, cliente in enumerate(self.cola):
            # Cada cliente debería estar alineado horizontalmente en fila
            cliente.objetivo_x = inicio_cola_x - (i * offset_x)
            # Todos a la misma altura (alineados con el cajero)
            cliente.objetivo_y = cliente_y

class Simulacion:
    def __init__(self):
        self.cajeros = []
        self.clientes_atendidos = 0
        self.clientes_perdidos = 0
        self.tiempo_espera_acumulado = 0
        self.reloj = 0
        self.pausada = False
        self.clientes_totales_generados = 0
        self.tiempo_respuesta_acumulado = 0
        self.historial_tiempos_espera = []
        
    def agregar_cajero(self, y_pos):
        nuevo_id = len(self.cajeros)
        self.cajeros.append(Cajero(nuevo_id, y_pos))
    
    def redistribuir_clientes(self, cajero_eliminado):
        # Redistribuir clientes de manera equitativa
        clientes_a_redistribuir = list(cajero_eliminado.cola)
        if cajero_eliminado.cliente_actual:
            clientes_a_redistribuir.insert(0, cajero_eliminado.cliente_actual)
        
        for i, cliente in enumerate(clientes_a_redistribuir):
            cajero_destino = self.cajeros[i % len(self.cajeros)]
            if i == 0 and not cajero_destino.cliente_actual:
                cajero_destino.cliente_actual = cliente
                cajero_destino.tiempo_inicio = pygame.time.get_ticks()
            else:
                cajero_destino.cola.append(cliente)
    
    def balancear_colas_nuevo_cajero(self, nuevo_cajero):
        """Redistribuye clientes de colas largas al nuevo cajero"""
        if len(self.cajeros) <= 1:
            return
        
        # Encontrar las colas más largas (excluyendo el nuevo cajero)
        otros_cajeros = [c for c in self.cajeros if c.id != nuevo_cajero.id]
        
        # Ordenar cajeros por longitud de cola (más largos primero)
        otros_cajeros.sort(key=lambda c: len(c.cola), reverse=True)
        
        # Calcular cuántos clientes mover para balancear
        total_clientes_en_cola = sum(len(c.cola) for c in otros_cajeros)
        promedio_deseado = total_clientes_en_cola // len(self.cajeros)
        
        clientes_a_mover = []
        
        # Tomar clientes de las colas más largas
        for cajero in otros_cajeros:
            if len(cajero.cola) > promedio_deseado:
                # Mover desde el final de la cola (los que llegaron más tarde)
                clientes_para_mover = min(len(cajero.cola) - promedio_deseado, 
                                        promedio_deseado - len(clientes_a_mover))
                
                for _ in range(clientes_para_mover):
                    if cajero.cola:
                        cliente = cajero.cola.pop()  # Quitar del final
                        clientes_a_mover.append(cliente)
                        
                        # Actualizar posiciones de los clientes restantes
                        cajero.mover_clientes_cola(cajero.x)
                
                if len(clientes_a_mover) >= promedio_deseado:
                    break
        
        # Asignar los clientes movidos al nuevo cajero
        for cliente in clientes_a_mover:
            nuevo_cajero.cola.append(cliente)
        
        # Actualizar posiciones del nuevo cajero
        nuevo_cajero.mover_clientes_cola(nuevo_cajero.x)

    def contar_clientes_activos(self):
        total = 0
        for cajero in self.cajeros:
            total += len(cajero.cola)
            if cajero.cliente_actual:
                total += 1
        return total
    
    def get_estadisticas(self):
        max_clientes = len(self.cajeros) * 10
        clientes_activos = self.contar_clientes_activos()
        
        # Utilización del sistema
        utilizacion = (clientes_activos / max_clientes * 100) if max_clientes > 0 else 0
        
        # Probabilidad de rechazo
        total_intentos = self.clientes_atendidos + self.clientes_perdidos
        prob_rechazo = (self.clientes_perdidos / max(1, total_intentos)) * 100
        
        # Tiempo promedio de espera
        tiempo_prom_espera = self.tiempo_espera_acumulado / max(1, self.clientes_atendidos)
        
        # Throughput (clientes por minuto)
        throughput = (self.clientes_atendidos / max(1, self.reloj)) * 60 if self.reloj > 0 else 0
        
        # Eficiencia del sistema
        eficiencia = (self.clientes_atendidos / max(1, self.clientes_totales_generados)) * 100
        
        # Longitud promedio de cola
        longitud_prom_cola = sum(len(cajero.cola) for cajero in self.cajeros) / max(1, len(self.cajeros))
        
        return {
            'utilizacion': utilizacion,
            'prob_rechazo': prob_rechazo,
            'tiempo_prom_espera': tiempo_prom_espera,
            'throughput': throughput,
            'clientes_activos': clientes_activos,
            'max_clientes': max_clientes,
            'eficiencia': eficiencia,
            'longitud_prom_cola': longitud_prom_cola
        }
    
    def reset(self):
        self.clientes_atendidos = 0
        self.clientes_perdidos = 0
        self.tiempo_espera_acumulado = 0
        self.reloj = 0
        self.clientes_totales_generados = 0
        self.tiempo_respuesta_acumulado = 0
        self.historial_tiempos_espera = []
        
        # Limpiar cajeros
        for cajero in self.cajeros:
            cajero.cola.clear()
            cajero.cliente_actual = None
            cajero.clientes_atendidos_cajero = 0

    def exportar_resultados(self):
        """Exporta los resultados de la simulación a un archivo CSV"""
        stats = self.get_estadisticas()
        # Generar nombre de archivo con fecha y hora
        filename = f"simulacion_supermercado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                # Encabezado general y fecha
                writer.writerow(["Parámetro", "Valor"])
                writer.writerow(["Fecha y hora", datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow(["Duración simulación (s)", f"{self.reloj:.2f}"])
                writer.writerow([])

                # Parámetros de simulación
                writer.writerow(["Parámetros de simulación", ""])
                writer.writerow(["Número de cajeros", len(self.cajeros)])
                writer.writerow(["Velocidad cajero", VELOCIDAD_CAJERO])
                writer.writerow(["Tiempo por producto", TIEMPO_POR_PRODUCTO])
                writer.writerow(["Tasa de llegada", TASA_LLEGADA_BASE])
                writer.writerow([])

                # Estadísticas
                writer.writerow(["Estadísticas de simulación", ""])
                writer.writerow(["Clientes atendidos", self.clientes_atendidos])
                writer.writerow(["Clientes perdidos", self.clientes_perdidos])
                writer.writerow(["Clientes totales generados", self.clientes_totales_generados])
                writer.writerow(["Utilización (%)", f"{stats['utilizacion']:.2f}"])
                writer.writerow(["Probabilidad de rechazo (%)", f"{stats['prob_rechazo']:.2f}"])
                writer.writerow(["Tiempo promedio de espera (s)", f"{stats['tiempo_prom_espera']:.2f}"])
                writer.writerow(["Throughput (clientes/min)", f"{stats['throughput']:.2f}"])
                writer.writerow(["Eficiencia (%)", f"{stats['eficiencia']:.2f}"])
                writer.writerow(["Longitud promedio de cola", f"{stats['longitud_prom_cola']:.2f}"])
                writer.writerow([])

                # Historial de tiempos de espera
                writer.writerow(["Historial de tiempos de espera (últimos 100 clientes)"])
                writer.writerow(["Tiempo de espera (s)"])
                for tiempo in self.historial_tiempos_espera[-100:]:
                    writer.writerow([f"{tiempo:.2f}"])

            print(f"Resultados exportados exitosamente a: {filename}")
            return True

        except Exception as e:
            print(f"Error al exportar resultados: {e}")
            return False

def calcular_posiciones_cajeros(num_cajeros, height):
    margen_superior = 120
    espacio_disponible = height - margen_superior - 150
    espacio_entre = min(ESPACIO_ENTRE_CAJEROS, espacio_disponible / max(1, num_cajeros - 1)) if num_cajeros > 1 else 0
    return [int(margen_superior + i * espacio_entre) for i in range(num_cajeros)]

def dibujar_panel_metricas(screen, simulacion):
    # Panel de fondo con sombra - ajustar altura para dar espacio al panel de controles
    shadow_offset = 4
    shadow_rect = pygame.Rect(14, 14, MARGEN_IZQUIERDO - 30, current_height - 270)
    pygame.draw.rect(screen, (220, 220, 220), shadow_rect, border_radius=10)
    
    # Panel principal con borde redondeado
    panel_rect = pygame.Rect(10, 10, MARGEN_IZQUIERDO - 30, current_height - 270)
    pygame.draw.rect(screen, PANEL_BG, panel_rect, border_radius=10)
    pygame.draw.rect(screen, ACCENT_COLOR, panel_rect, 2, border_radius=10)
    
    # Barra de título con degradado
    title_rect = pygame.Rect(10, 10, MARGEN_IZQUIERDO - 30, 40)
    pygame.draw.rect(screen, ACCENT_COLOR, title_rect, border_top_left_radius=10, border_top_right_radius=10)
    
    # Título con estilo moderno
    titulo = FONT_TITLE.render("MÉTRICAS DEL SISTEMA", True, WHITE)
    titulo_rect = titulo.get_rect(center=(panel_rect.centerx, 30))
    screen.blit(titulo, titulo_rect)
    
    stats = simulacion.get_estadisticas()
    
    # Métricas principales
    metricas = [
        ("Estado", "PAUSADO" if simulacion.pausada else "EJECUTANDO", RED if simulacion.pausada else GREEN),
        ("Tiempo simulación", f"{simulacion.reloj:.1f}s", BLACK),
        ("", "", BLACK),  # Separador
        ("RENDIMIENTO", "", DARK_GRAY),
        ("Clientes atendidos", f"{simulacion.clientes_atendidos}", GREEN),
        ("Clientes perdidos", f"{simulacion.clientes_perdidos}", RED),
        ("Throughput", f"{stats['throughput']:.1f} cli/min", BLUE),
        ("Eficiencia", f"{stats['eficiencia']:.1f}%", PURPLE),
        ("", "", BLACK),  # Separador
        ("SISTEMA", "", DARK_GRAY),
        ("En sistema", f"{stats['clientes_activos']}/{stats['max_clientes']}", ORANGE),
        ("Utilización", f"{stats['utilizacion']:.1f}%", PURPLE),
        ("Prob. rechazo", f"{stats['prob_rechazo']:.1f}%", RED),
        ("Cola promedio", f"{stats['longitud_prom_cola']:.1f}", BLUE),
        ("", "", BLACK),  # Separador
        ("TIEMPOS", "", DARK_GRAY),
        ("Espera promedio", f"{stats['tiempo_prom_espera']:.1f}s", BLUE),    ]
    
    y_offset = 65
    for label, value, color in metricas:
        if label == "":  # Separador
            y_offset += 15
            # Línea divisoria sutil
            pygame.draw.line(screen, (220, 220, 220), (25, y_offset - 7), (MARGEN_IZQUIERDO - 55, y_offset - 7), 1)
            continue
            
        elif label.isupper() and value == "":  # Títulos de sección
            # Fondo de sección
            section_bg = pygame.Rect(15, y_offset - 5, MARGEN_IZQUIERDO - 40, 30)
            pygame.draw.rect(screen, (240, 240, 240), section_bg, border_radius=5)
            
            # Título de sección con icono visual
            text = FONT_MEDIUM.render(label, True, ACCENT_COLOR)
            screen.blit(text, (30, y_offset))
            
            # Pequeño indicador colorido
            indicator_color = {
                "RENDIMIENTO": GREEN,
                "SISTEMA": BLUE,
                "TIEMPOS": ORANGE
            }.get(label, ACCENT_COLOR)
            pygame.draw.rect(screen, indicator_color, (20, y_offset, 5, 20), border_radius=2)
            
            y_offset += 30
            continue
        
        # Métricas normales con diseño mejorado
        # Área de métrica con hover visual
        metric_bg = pygame.Rect(20, y_offset - 2, MARGEN_IZQUIERDO - 50, 24)
        
        # Diferenciar filas para mejor lectura
        if (y_offset // 20) % 2 == 0:
            pygame.draw.rect(screen, (248, 248, 252), metric_bg, border_radius=4)
            
        # Etiqueta
        label_surface = FONT_SMALL.render(f"{label}:", True, DARK_GRAY)
        screen.blit(label_surface, (30, y_offset))
        
        # Valor con fondo redondeado del color correspondiente
        value_bg = pygame.Rect(195, y_offset - 2, 80, 20)
        value_alpha_color = (*color[:3], 40)  # Color con transparencia
        
        # Superficie con transparencia para el fondo del valor
        value_bg_surface = pygame.Surface((80, 20), pygame.SRCALPHA)
        value_bg_surface.fill(value_alpha_color)
        rounded_surface = pygame.Surface((80, 20), pygame.SRCALPHA)
        pygame.draw.rect(rounded_surface, value_alpha_color, (0, 0, 80, 20), border_radius=10)
        screen.blit(rounded_surface, (195, y_offset - 2))
        
        # Texto del valor
        value_surface = FONT_SMALL.render(str(value), True, color)
        value_rect = value_surface.get_rect(center=(value_bg.centerx, value_bg.centery))
        screen.blit(value_surface, value_rect)
        
        y_offset += 24

def dibujar_panel_controles(screen, sliders, buttons, cajero_buttons):
    # Panel de controles en la parte inferior izquierda - posición fija desde abajo
    panel_y = current_height - 250  # Espacio fijo desde abajo
    
    # Sombra
    shadow_rect = pygame.Rect(14, panel_y + 4, MARGEN_IZQUIERDO - 30, 250)
    pygame.draw.rect(screen, (220, 220, 220), shadow_rect, border_radius=10)
    
    # Panel principal - altura fija para todos los controles
    panel_rect = pygame.Rect(10, panel_y, MARGEN_IZQUIERDO - 30, 250)
    pygame.draw.rect(screen, PANEL_BG, panel_rect, border_radius=10)
    pygame.draw.rect(screen, ACCENT_COLOR, panel_rect, 2, border_radius=10)
    
    # Barra de título con color accent
    title_rect = pygame.Rect(10, panel_y, MARGEN_IZQUIERDO - 30, 30)
    pygame.draw.rect(screen, TURQUOISE, title_rect, border_top_left_radius=10, border_top_right_radius=10)
    
    # Título del panel centrado
    titulo = FONT_MEDIUM.render("CONTROLES", True, WHITE)
    titulo_rect = titulo.get_rect(center=(panel_rect.centerx, panel_y + 15))
    screen.blit(titulo, titulo_rect)
      # Separador sutil después del título
    pygame.draw.line(screen, (230, 230, 230), 
                    (15, panel_y + 35), 
                    (MARGEN_IZQUIERDO - 35, panel_y + 35), 1)
    
    # Dibujar sliders con espaciado más compacto - más espacio para evitar overlap con título
    slider_start_y = panel_y + 50
    for i, slider in enumerate(sliders):
        slider.rect.y = slider_start_y + (i * 25)  # Reducir espaciado de 30 a 25
        slider.draw(screen)
    
    # Etiqueta para control de cajeros - posición más compacta
    cajeros_label_y = slider_start_y + (len(sliders) * 25) + 10
    cajeros_bg = pygame.Rect(20, cajeros_label_y - 5, 90, 20)
    pygame.draw.rect(screen, (240, 240, 250), cajeros_bg, border_radius=5)
    
    cajeros_label = FONT_SMALL.render("Cajeros:", True, DARK_GRAY)
    screen.blit(cajeros_label, (25, cajeros_label_y))
    
    # Botones de cajeros con espaciado más compacto
    buttons_cajero_y = cajeros_label_y + 25
    for i, button in enumerate(cajero_buttons):
        if i < 2:  # Botones - y +
            button.rect.x = 25 + (i * 40)
            button.rect.y = buttons_cajero_y
            button.rect.height = 25
        else:  # Botón contador
            button.rect.x = 110
            button.rect.y = buttons_cajero_y
            button.rect.height = 25
        button.draw(screen)
    
    # Etiqueta para botones principales - espaciado más compacto
    controles_label_y = buttons_cajero_y + 30
    controles_bg = pygame.Rect(20, controles_label_y - 5, 120, 20)
    pygame.draw.rect(screen, (240, 240, 250), controles_bg, border_radius=5)
    
    controles_label = FONT_SMALL.render("Simulación:", True, DARK_GRAY)
    screen.blit(controles_label, (25, controles_label_y))
    
    # Botones principales en dos filas - espaciado más compacto
    buttons_main_y = controles_label_y + 25
    button_width = 68
    button_spacing = 8
    start_x = 20
    
    # Primera fila: PAUSAR y START
    for i in range(2):
        buttons[i + 1].rect.x = start_x + (i * (button_width + button_spacing))
        buttons[i + 1].rect.y = buttons_main_y
        buttons[i + 1].rect.width = button_width
        buttons[i + 1].rect.height = 25
        buttons[i + 1].draw(screen)
    
    # Segunda fila: REINICIAR y EXPORT
    buttons_second_row_y = buttons_main_y + 30
    for i in range(2):
        button_index = i if i == 0 else 3  # índices 0 (Reset) y 3 (Export)
        buttons[button_index].rect.x = start_x + (i * (button_width + button_spacing))
        buttons[button_index].rect.y = buttons_second_row_y
        buttons[button_index].rect.width = button_width
        buttons[button_index].rect.height = 25
        buttons[button_index].draw(screen)

def generar_cliente_con_prioridad():
    # 70% normales, 20% premium, 10% express
    rand = random.random()
    if rand < 0.7:
        return 1  # Normal
    elif rand < 0.9:
        return 2  # Premium
    else:
        return 3  # Express

def mostrar_instrucciones():
    """
    CONTROLES DE LA SIMULACIÓN:
    
    TECLADO:
    - ESPACIO: Pausar/Reanudar simulación
    - ↑: Agregar cajero (máximo 8)
    - ↓: Quitar cajero (mínimo 1)
    - ←: Reducir velocidad cajero
    - →: Aumentar velocidad cajero
    
    MOUSE:
    - Sliders: Ajustar tasa de llegada y tiempo por producto
    - Botones: Reset, Pausa, Start, Export
    
    MÉTRICAS CLAVE:
    - Utilización: % de capacidad del sistema en uso
    - Throughput: Clientes atendidos por minuto
    - Prob. rechazo: % de clientes que no pueden ser atendidos
    - Eficiencia: % de clientes atendidos vs generados
    """
    pass

def dibujar_patron_fondo(screen, rect):
    """Dibuja un patrón de fondo sutil para el área de simulación"""
    color1 = (242, 245, 250)  # Tono muy claro casi blanco
    color2 = (235, 240, 248)  # Un poco más oscuro
    
    tam_celda = 15
    for i in range(rect.left, rect.right, tam_celda):
        for j in range(rect.top + 40, rect.bottom, tam_celda):  # Empezamos después de la barra de título
            if (i // tam_celda + j // tam_celda) % 2 == 0:
                pygame.draw.rect(screen, color1, (i, j, tam_celda, tam_celda))
            else:
                pygame.draw.rect(screen, color2, (i, j, tam_celda, tam_celda))

def main():
    global VELOCIDAD_CAJERO, current_width, current_height, screen, POS_X_CAJEROS, TASA_LLEGADA_BASE
    
    print("Iniciando simulación de supermercado...")
    
    clock = pygame.time.Clock()
    simulacion = Simulacion()
    posiciones_y = calcular_posiciones_cajeros(NUM_CAJEROS_INICIAL, current_height)
    for y in posiciones_y:
        simulacion.agregar_cajero(y)
    
    # Crear controles deslizantes con posiciones iniciales
    sliders = [
        Slider(30, current_height - 150, 180, 6, 1, 10, TASA_LLEGADA_BASE * 100, "Tasa de Llegada"),
        Slider(30, current_height - 120, 180, 6, 1, 10, 5, "Tiempo por Producto")
    ]
    
    # Crear botones principales con dimensiones ajustadas y nombres correctos
    buttons = [
        Button(240, current_height - 50, 68, 25, "REINICIAR", RED, WHITE),
        Button(240, current_height - 50, 68, 25, "PAUSAR", ORANGE, WHITE),
        Button(240, current_height - 50, 68, 25, "START", GREEN, WHITE),
        Button(240, current_height - 50, 68, 25, "EXPORT", BLUE, WHITE)
    ]
    
    # Crear botones para control de cajeros
    cajero_buttons = [
        Button(30, current_height - 60, 35, 25, "-", RED, WHITE),
        Button(70, current_height - 60, 35, 25, "+", GREEN, WHITE),
        Button(110, current_height - 60, 80, 25, f"{len(simulacion.cajeros)} Cajeros", PURPLE, WHITE)
    ]
    
    print("Simulación iniciada correctamente. Presiona ESC para salir.")
    
    running = True
    while running:
        dt = clock.tick(FPS_LIMITE) / 1000
        
        if not simulacion.pausada:
            simulacion.reloj += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Agregar ESC para salir
                    running = False
                # Manejar eventos de sliders
            for slider in sliders:
                if slider.handle_event(event):
                    if slider.label.startswith("Tasa"):
                        TASA_LLEGADA_BASE = slider.val / 100
                    elif slider.label.startswith("Tiempo"):
                        TIEMPO_POR_PRODUCTO = slider.val / 10
            
            # Manejar eventos de botones principales
            for i, button in enumerate(buttons):
                if button.handle_event(event):
                    if i == 0:  # REINICIAR
                        simulacion.reset()
                    elif i == 1:  # PAUSAR
                        simulacion.pausada = True
                        buttons[1].text = "PAUSAR"
                        buttons[2].text = "START"
                    elif i == 2:  # START
                        simulacion.pausada = False
                        buttons[1].text = "PAUSAR"
                        buttons[2].text = "START"
                    elif i == 3:  # EXPORT
                        simulacion.exportar_resultados()
            
            # Manejar eventos de botones de cajeros
            for i, button in enumerate(cajero_buttons):
                if button.handle_event(event):
                    if i == 0 and len(simulacion.cajeros) > 1:  # Quitar cajero
                        cajero_eliminado = simulacion.cajeros.pop()
                        simulacion.redistribuir_clientes(cajero_eliminado)
                        posiciones_y = calcular_posiciones_cajeros(len(simulacion.cajeros), current_height)
                        for j, cajero in enumerate(simulacion.cajeros):
                            cajero.y = posiciones_y[j]
                            # Calcular posición Y alineada para clientes
                            cajero_center_y = cajero.y + (cashier_sprite.get_height() // 2)
                            cliente_y = cajero_center_y - 30
                            # Si hay un cliente siendo atendido, actualizar su posición
                            if cajero.cliente_actual:
                                cajero.cliente_actual.objetivo_x = cajero.x + cashier_sprite.get_width() + 15
                                cajero.cliente_actual.objetivo_y = cliente_y
                            # Actualizar posiciones de los clientes en cola
                            cajero.mover_clientes_cola(cajero.x)
                        # Actualizar texto del botón contador
                        cajero_buttons[2].text = f"{len(simulacion.cajeros)} Cajeros"
                    elif i == 1 and len(simulacion.cajeros) < 8:  # Agregar cajero
                        # Crear nuevo cajero
                        nuevo_indice = len(simulacion.cajeros)
                        posiciones_y = calcular_posiciones_cajeros(len(simulacion.cajeros) + 1, current_height)
                        nuevo_cajero = Cajero(nuevo_indice, posiciones_y[nuevo_indice])
                        simulacion.cajeros.append(nuevo_cajero)
                        
                        # Balancear las colas moviendo clientes al nuevo cajero
                        simulacion.balancear_colas_nuevo_cajero(nuevo_cajero)
                        
                        # Reposicionar todos los cajeros existentes
                        for i, cajero in enumerate(simulacion.cajeros):
                            cajero.y = posiciones_y[i]
                            # Calcular posición Y alineada para clientes
                            cajero_center_y = cajero.y + (cashier_sprite.get_height() // 2)
                            cliente_y = cajero_center_y - 30
                            # Si hay un cliente siendo atendido, actualizar su posición
                            if cajero.cliente_actual:
                                cajero.cliente_actual.objetivo_x = cajero.x + cashier_sprite.get_width() + 15
                                cajero.cliente_actual.objetivo_y = cliente_y
                            # Actualizar posiciones de los clientes en cola
                            cajero.mover_clientes_cola(cajero.x)
                        # Actualizar texto del botón contador
                        cajero_buttons[2].text = f"{len(simulacion.cajeros)} Cajeros"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and VELOCIDAD_CAJERO > 1:
                    VELOCIDAD_CAJERO -= 1
                elif event.key == pygame.K_RIGHT and VELOCIDAD_CAJERO < 10:
                    VELOCIDAD_CAJERO += 1
                elif event.key == pygame.K_UP and len(simulacion.cajeros) < 8:
                    # Crear nuevo cajero
                    nuevo_indice = len(simulacion.cajeros)
                    posiciones_y = calcular_posiciones_cajeros(len(simulacion.cajeros) + 1, current_height)
                    nuevo_cajero = Cajero(nuevo_indice, posiciones_y[nuevo_indice])
                    simulacion.cajeros.append(nuevo_cajero)
                    
                    # Balancear las colas moviendo clientes al nuevo cajero
                    simulacion.balancear_colas_nuevo_cajero(nuevo_cajero)
                    
                    # Reposicionar todos los cajeros existentes y sus clientes
                    for i, cajero in enumerate(simulacion.cajeros):
                        cajero.y = posiciones_y[i]
                        # Calcular posición Y alineada para clientes
                        cajero_center_y = cajero.y + (cashier_sprite.get_height() // 2)
                        cliente_y = cajero_center_y - 30
                        # Si hay un cliente siendo atendido, actualizar su posición
                        if cajero.cliente_actual:
                            cajero.cliente_actual.objetivo_x = cajero.x + cashier_sprite.get_width() + 15
                            cajero.cliente_actual.objetivo_y = cliente_y
                        # Actualizar posiciones de los clientes en cola
                        cajero.mover_clientes_cola(cajero.x)
                elif event.key == pygame.K_DOWN and len(simulacion.cajeros) > 1:
                    cajero_eliminado = simulacion.cajeros.pop()
                    simulacion.redistribuir_clientes(cajero_eliminado)
                    posiciones_y = calcular_posiciones_cajeros(len(simulacion.cajeros), current_height)
                    for i, cajero in enumerate(simulacion.cajeros):
                        cajero.y = posiciones_y[i]
                        # Calcular posición Y alineada para clientes
                        cajero_center_y = cajero.y + (cashier_sprite.get_height() // 2)
                        cliente_y = cajero_center_y - 30
                        # Si hay un cliente siendo atendido, actualizar su posición
                        if cajero.cliente_actual:
                            cajero.cliente_actual.objetivo_x = cajero.x + cashier_sprite.get_width() + 15
                            cajero.cliente_actual.objetivo_y = cliente_y
                        # Actualizar posiciones de los clientes en cola
                        cajero.mover_clientes_cola(cajero.x)
        
                elif event.key == pygame.K_SPACE:
                    simulacion.pausada = not simulacion.pausada
            
            elif event.type == pygame.VIDEORESIZE:
                new_width, new_height = event.w, event.h
                screen = pygame.display.set_mode((max(new_width, 1000), max(new_height, 700)), pygame.RESIZABLE)
                current_width, current_height = screen.get_size()
                POS_X_CAJEROS = current_width - MARGEN_DERECHO
                
                # Actualizar posiciones iniciales de sliders (se ajustarán en dibujar_panel_controles)
                sliders[0].rect.x = 30
                sliders[1].rect.x = 30
                
                # Actualizar posiciones de sliders y botones
                sliders[0].rect.y = current_height - 140
                sliders[1].rect.y = current_height - 100
                buttons[0].rect.y = current_height - 140
                buttons[1].rect.y = current_height - 110
                buttons[2].rect.y = current_height - 80
                buttons[3].rect.y = current_height - 50
                
                # Actualizar posiciones de botones de cajeros
                cajero_buttons[0].rect.y = current_height - 60
                cajero_buttons[1].rect.y = current_height - 60
                cajero_buttons[2].rect.y = current_height - 60
                  # Recalcular posiciones de los cajeros y mover todos sus clientes
                posiciones_y = calcular_posiciones_cajeros(len(simulacion.cajeros), current_height)
                for i, cajero in enumerate(simulacion.cajeros):
                    cajero.x = POS_X_CAJEROS
                    cajero.y = posiciones_y[i]
                    
                    # Si hay un cliente siendo atendido, actualizar su posición objetivo primero
                    if cajero.cliente_actual:
                        cajero.cliente_actual.objetivo_x = cajero.x + cashier_sprite.get_width() + 15
                        cajero.cliente_actual.objetivo_y = cajero.y + 10
                    
                    # Asegurarse de que todos los clientes en cola se muevan con su cajero
                    cajero.mover_clientes_cola(cajero.x)
        
        # Lógica de simulación
        if not simulacion.pausada:
            # Generar nuevos clientes con límite
            clientes_activos = simulacion.contar_clientes_activos()
            max_clientes = len(simulacion.cajeros) * 10
            
            # Tasa de llegada dinámica basada en utilización
            if random.random() < TASA_LLEGADA_BASE:
                simulacion.clientes_totales_generados += 1
                if clientes_activos < max_clientes:
                    prioridad = generar_cliente_con_prioridad()
                    nuevo_cliente = Cliente(simulacion.clientes_totales_generados, simulacion.reloj, prioridad)
                    
                    # Asignar a la cola más corta (o por prioridad)
                    if prioridad == 3:  # Express va a la cola más corta
                        cajero_elegido = min(simulacion.cajeros, key=lambda c: len(c.cola))
                    else:
                        cajero_elegido = min(simulacion.cajeros, key=lambda c: len(c.cola))
                    
                    cajero_elegido.cola.append(nuevo_cliente)
                else:
                    simulacion.clientes_perdidos += 1
            
            # Atender clientes
            for cajero in simulacion.cajeros:
                if not cajero.cliente_actual and cajero.cola:
                    cajero.cliente_actual = cajero.cola.popleft()
                    cajero.tiempo_inicio = pygame.time.get_ticks()
                    # Establecer posición inmediata del cliente siendo atendido
                    cajero.cliente_actual.objetivo_x = cajero.x + cashier_sprite.get_width() + 15
                    cajero.cliente_actual.objetivo_y = cajero.y + 10
                    tiempo_espera = cajero.cliente_actual.calcular_tiempo_espera(simulacion.reloj)
                    simulacion.tiempo_espera_acumulado += tiempo_espera
                    simulacion.historial_tiempos_espera.append(tiempo_espera)
                    cajero.clientes_atendidos_cajero += 1
                
                elif cajero.cliente_actual:
                    # Ajustar tiempo de atención por prioridad
                    factor_tiempo = {1: 1.0, 2: 0.8, 3: 0.6}.get(cajero.cliente_actual.prioridad, 1.0)
                    tiempo_atencion_ajustado = cajero.cliente_actual.tiempo_atencion * factor_tiempo
                    
                    if pygame.time.get_ticks() - cajero.tiempo_inicio > tiempo_atencion_ajustado * 1000:
                        simulacion.clientes_atendidos += 1
                        cajero.cliente_actual = None
        
        # Dibujar
        screen.fill(BACKGROUND)
        dibujar_panel_metricas(screen, simulacion)
        dibujar_panel_controles(screen, sliders, buttons, cajero_buttons)        # Dibujar área de simulación con diseño mejorado
        # Sombra sutil
        shadow_area = pygame.Rect(MARGEN_IZQUIERDO + 4, 14, current_width - MARGEN_IZQUIERDO - MARGEN_DERECHO + 180, current_height - 20)
        pygame.draw.rect(screen, (220, 220, 220), shadow_area, border_radius=12)
        
        # Área principal de simulación
        sim_area = pygame.Rect(MARGEN_IZQUIERDO, 10, current_width - MARGEN_IZQUIERDO - MARGEN_DERECHO + 180, current_height - 20)
        pygame.draw.rect(screen, PANEL_BG, sim_area, border_radius=12)
        
        # Patrón de fondo sutil para el área de simulación
        dibujar_patron_fondo(screen, sim_area)
        
        # Borde del área de simulación
        pygame.draw.rect(screen, ACCENT_COLOR, sim_area, 2, border_radius=12)
        
        # Barra de título en la parte superior con gradiente
        title_bar = pygame.Rect(MARGEN_IZQUIERDO, 10, current_width - MARGEN_IZQUIERDO - MARGEN_DERECHO + 180, 40)
        # Gradiente simple con dos rectángulos (uno encima del otro)
        pygame.draw.rect(screen, GRADIENT_TOP, title_bar, border_top_left_radius=12, border_top_right_radius=12)
        gradient_bottom = pygame.Rect(MARGEN_IZQUIERDO, 30, current_width - MARGEN_IZQUIERDO - MARGEN_DERECHO + 180, 20)
        pygame.draw.rect(screen, GRADIENT_BOTTOM, gradient_bottom)
          # Título del área de simulación con efecto de sombra sutil
        titulo_sim = FONT_TITLE.render("SIMULACIÓN DE SUPERMERCADO", True, WHITE)
        # Sombra del texto (offset ligero)
        titulo_shadow = FONT_TITLE.render("SIMULACIÓN DE SUPERMERCADO", True, (30, 30, 30, 128))
        titulo_rect = titulo_sim.get_rect(center=(title_bar.centerx, title_bar.centery))
        shadow_rect = titulo_shadow.get_rect(center=(title_bar.centerx + 1, title_bar.centery + 1))
        screen.blit(titulo_shadow, shadow_rect)
        screen.blit(titulo_sim, titulo_rect)
          # Asegurar que los clientes estén correctamente alineados antes de dibujarlos
        for cajero in simulacion.cajeros:
            # Actualizar posiciones de los clientes en cola para asegurar el alineamiento
            offset_x = 60
            inicio_cola_x = cajero.x - 80
            
            for i, cliente in enumerate(cajero.cola):
                cliente.objetivo_x = inicio_cola_x - (i * offset_x)
                cliente.objetivo_y = cajero.y + 10
            
            # Actualizar posición del cliente siendo atendido si existe
            if cajero.cliente_actual:
                cajero.cliente_actual.objetivo_x = cajero.x + cashier_sprite.get_width() + 15
                cajero.cliente_actual.objetivo_y = cajero.y + 10

            # Dibujar el cajero y sus clientes
            cajero.dibujar(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    print("Simulación terminada.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error al ejecutar la simulación: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
