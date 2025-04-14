import pygame
import random
import time
import math
from collections import deque

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Simulación de Supermercado")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.SysFont("Arial", 24)
COLORS = [(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)) for _ in range(20)]

# Parámetros de simulación
NUM_CAJEROS = 4  # Puede variar de 1 a 8
VELOCIDAD_CAJERO = 5  # Escala de 1 a 10
TIEMPO_POR_PRODUCTO = 1.0  # Segundos por producto (base)

class Cliente:
    def __init__(self, id):
        self.id = id
        self.productos = random.randint(1, 30)  # Rango de productos
        self.color = random.choice(COLORS)
        self.tiempo_atencion = self.productos * TIEMPO_POR_PRODUCTO * (10 / VELOCIDAD_CAJERO)
        self.x = -50
        self.y = HEIGHT - 100
        self.ancho = 30
        self.alto = 50
        self.objetivo_x = None
        self.objetivo_y = None
        self.velocidad = 2
        self.en_cola = False
        self.siendo_atendido = False
    
    def dibujar(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.ancho, self.alto))
        font = pygame.font.SysFont(None, 20)
        texto = font.render(f"{self.productos}", True, BLACK)
        screen.blit(texto, (self.x + 5, self.y + 5))
    
    def mover(self):
        if self.objetivo_x is not None and self.objetivo_y is not None:
            dx = self.objetivo_x - self.x
            dy = self.objetivo_y - self.y
            distancia = math.sqrt(dx**2 + dy**2)
            
            if distancia > 2:
                self.x += dx / distancia * self.velocidad
                self.y += dy / distancia * self.velocidad
            else:
                self.x = self.objetivo_x
                self.y = self.objetivo_y

class Cajero:
    def __init__(self, id, x):
        self.id = id
        self.x = x
        self.y = HEIGHT - 150
        self.ancho = 50
        self.alto = 80
        self.cola = deque()
        self.cliente_actual = None
        self.tiempo_inicio_atencion = 0
        self.ocupado = False
    
    def dibujar(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.ancho, self.alto))
        font = pygame.font.SysFont(None, 24)
        texto = font.render(f"Cajero {self.id+1}", True, WHITE)
        screen.blit(texto, (self.x + 5, self.y + 30))
        
        # Dibujar cola
        for i, cliente in enumerate(self.cola):
            cliente.objetivo_x = self.x - (i + 1) * 40
            cliente.objetivo_y = HEIGHT - 100
            cliente.dibujar()
        
        if self.cliente_actual:
            self.cliente_actual.objetivo_x = self.x + 60
            self.cliente_actual.objetivo_y = HEIGHT - 100
            self.cliente_actual.dibujar()
            
            # Barra de progreso
            tiempo_transcurrido = time.time() - self.tiempo_inicio_atencion
            progreso = min(tiempo_transcurrido / self.cliente_actual.tiempo_atencion, 1.0)
            pygame.draw.rect(screen, BLACK, (self.x + 60, HEIGHT - 120, 100, 10))
            pygame.draw.rect(screen, GREEN, (self.x + 60, HEIGHT - 120, 100 * progreso, 10))
    
    def agregar_cliente(self, cliente):
        self.cola.append(cliente)
        cliente.en_cola = True
    
    def atender(self):
        if not self.ocupado and self.cola:
            self.cliente_actual = self.cola.popleft()
            self.tiempo_inicio_atencion = time.time()
            self.ocupado = True
            self.cliente_actual.en_cola = False
            self.cliente_actual.siendo_atendido = True
        
        if self.ocupado and self.cliente_actual:
            tiempo_transcurrido = time.time() - self.tiempo_inicio_atencion
            if tiempo_transcurrido >= self.cliente_actual.tiempo_atencion:
                self.ocupado = False
                self.cliente_actual = None

def main():
    global NUM_CAJEROS, VELOCIDAD_CAJERO, TIEMPO_POR_PRODUCTO
    
    clock = pygame.time.Clock()
    running = True
    
    cajeros = [Cajero(i, 150 + i * 200) for i in range(NUM_CAJEROS)]
    clientes = []
    tiempo_ultimo_cliente = time.time()
intervalo_clientes = random.uniform(1, 3)  # Genera un número aleatorio entre 1 y 3 segundos
    
    while running:
        current_time = time.time()
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and NUM_CAJEROS < 8:
                    NUM_CAJEROS += 1
                    cajeros.append(Cajero(NUM_CAJEROS-1, 150 + (NUM_CAJEROS-1) * 200))
                elif event.key == pygame.K_DOWN and NUM_CAJEROS > 1:
                    cajeros.pop()
                    NUM_CAJEROS -= 1
                elif event.key == pygame.K_RIGHT and VELOCIDAD_CAJERO < 10:
                    VELOCIDAD_CAJERO += 1
                elif event.key == pygame.K_LEFT and VELOCIDAD_CAJERO > 1:
                    VELOCIDAD_CAJERO -= 1
        
        # Generar nuevo cliente
        if current_time - tiempo_ultimo_cliente > intervalo_clientes:
            nuevo_cliente = Cliente(len(clientes))
            clientes.append(nuevo_cliente)
            
            # Asignar a la cola más corta
            colas = [len(c.cola) for c in cajeros]
            cajero_elegido = colas.index(min(colas))
            cajeros[cajero_elegido].agregar_cliente(nuevo_cliente)
            
            tiempo_ultimo_cliente = current_time
            intervalo_clientes = random.uniform(1, 5)  # Variabilidad en llegada
        
        # Actualizar cajeros
        for cajero in cajeros:
            cajero.atender()
        
        # Actualizar clientes
        for cliente in clientes:
            cliente.mover()
            
        # Dibujar información
        def mostrar_metricas():
            metricas = [
                f"Cajeros activos: {NUM_CAJEROS} (↑/↓ para cambiar)",
                f"Velocidad: {VELOCIDAD_CAJERO}/10 (←/→ para cambiar)"
            ]
            
            for i, texto in enumerate(metricas):
                texto_surface = FONT.render(texto, True, BLACK)
                screen.blit(texto_surface, (10, 10 + i * 30))
        
        # Dibujar
        screen.fill(WHITE)
        mostrar_metricas()        
        
        # Dibujar cajeros y clientes
        for cajero in cajeros:
            cajero.dibujar()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
