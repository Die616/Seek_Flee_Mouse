import pygame
import math
import random

# Inicializar pygame
pygame.init()

# Dimensiones de la ventana
w_screen = 800
h_screen = 512

def create_window():
    # Crear la ventana y establecer el titulo
    screen = pygame.display.set_mode((w_screen, h_screen))
    pygame.display.set_caption("Seek and Flee Mouse")
    return screen

class Boid:
    def __init__(self, x, y, radius, color):
        # Constructor de la clase Boid
        self.x = x  # Posicion en el eje x
        self.y = y  # Posicion en el eje y
        self.radius = radius    # Radio del circulo
        self.color = color    # Color del circulo
        self.velocity = [0, 0]  # Velocidad inicial en [x, y]
        self.speed = 0.05   # Velocidad de actualizacion

    def update(self):
        # Actualizar la posicion de Boid
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        #Comprobar si Boid sale de la pantalla y ajustar su posicion si es necesario
        if self.x < -self.radius:
            self.x = w_screen + self.radius
        elif self.x > w_screen + self.radius:
            self.x = -self.radius

        if self.y < -self.radius:
            self.y = h_screen + self.radius
        elif self.y > h_screen + self.radius:
            self.y = -self.radius

    def avoid_colition(self, boids):
        # Definir una distancia de seguridad para evitar colisiones
        safety_distance = 20

        for other_boid in boids:
            if other_boid != self:
                # Calcular la distancia entre este Boid y el otro Boid
                distance = math.sqrt((self.x - other_boid.x) ** 2 + (self.y - other_boid.y) ** 2)

                # Si estan demasiado cerca, calcular una direccion de evasion
                if distance < safety_distance:
                    direction = calculate_vec_direction(self, other_boid.x, other_boid.y)

                    # Actualizar la velocidad para evitar la colision
                    self.x -= direction[0] * (safety_distance - distance)
                    self.y -= direction[1] * (safety_distance - distance)

    def draw(self, screen):
        # Dibujar a Boid en la pantalla
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, 1)
        pygame.draw.line(screen, (255, 255, 0), (self.x, self.y), (self.x + self.velocity[0] * 500, self.y + self.velocity[1] * 500), 2)

def calculate_vec_direction(boid, target_x, target_y):
    """
    Calcular la direccion del vector desde Boid hasta el objetivo.

    :param boid: Objeto Boid
    :param target_x: Coordenada X del objetivo
    :param target_y: Coordenada Y del objetivo
    :return: Lista [dx, dy] que representa la direccion normalizada del vector
    """
    vec_direction = [target_x - boid.x, target_y - boid.y]
    length = math.sqrt(vec_direction[0] ** 2 + vec_direction[1] ** 2)

    # Noramalziar el vector direccion (asegurarse de que tiene una longitud de 1)
    if length > 0:
        vec_direction[0] /= length
        vec_direction[1] /= length
    
    return vec_direction  # Devolver la direccion normalizada del vector

def limit_posicion(boid):
    # Limitar la posicion del Boid dentro de los limites de la ventana
    if boid.x < 0:
        boid.x = random.randint(0, w_screen)
    elif boid.x > w_screen:
        boid.x = random.randint(0, w_screen)
    if boid.y < 0:
        boid.y = random.randint(0, h_screen)
    elif boid.y > h_screen:
        boid.y = random.randint(0, h_screen)

def seek_mouse(boids):
    """
    Mover a los Boids hacia la posicion del mouse.

    :param boids: Lista de objetos Boid
    """
    for boid in boids:
        # Obtener la posicion actual del mouse 
        mouse_x, mouse_y = pygame.mouse.get_pos()
                
        # Imprimir la posicion del mouse (Opcional, solo para depuracion)
        print("({}, {})".format(mouse_x, mouse_y))

        # Calcular la direccion desde el Boid hasta la posicion del mouse
        direction = calculate_vec_direction(boid, mouse_x, mouse_y)

        # Actualizar la velocidad del Boid para moverlo hacia la posicion del mouse
        boid.velocity = [direction[0] * boid.speed, direction[1] * boid.speed]

        # Actualizar la posicion del Boid
        boid.update()

        # Limitar la posicion del Boid
        limit_posicion(boid)

def flee_mouse(boids, flee_distance):
    """
    Mover a los Boids lejos de la posicion del mouse si esta cerca.

    :param boids: Lista de objetos Boid
    :param flee_distance: Distancia de huida, si el mouse esta mas cerca que esto, los Boids huiran
    """
    for boid in boids:
        # Obetener la posicion actual del mouse 
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Imprimir la posicion del mouse (Opcional, solo para depuracion)
        print("({}, {})".format(mouse_x, mouse_y))

        # Calcular la distancia entre el Boid y la posicion del mouse
        distance = math.sqrt((boid.x - mouse_x) ** 2 + (boid.y - mouse_y) ** 2)

        # Verificar si la distancia es menor que la distancia de huida
        if distance < flee_distance:
            # Calcular la direccion para huir del mouse
            direction = calculate_vec_direction(boid, mouse_x, mouse_y)

            # Actualizar la velocidad del Boid para moverlo lejos de la posicion del mouse
            boid.velocity = [-direction[0] * boid.speed, -direction[1] * boid.speed]
        else:
            # Si la distancia es mayor que el rango, reducir gradualmente la velocidad
            slowdown_factor = 0.05
            boid.velocity[0] *= (1 - slowdown_factor)
            boid.velocity[1] *= (1 - slowdown_factor)

            # Detener el Boi si la velocidad es lo suficientemente baja
            if abs(boid.velocity[0]) < 0.1 and abs(boid.velocity[1]) < 0.1:
                boid.velocity = [0, 0]

        # Actualizar la posicion del Boid
        boid.update()
        
        # Limitar la posicion del Boid
        limit_posicion(boid)

def main():
    screen = create_window()
    num_red_boids = 5
    num_blue_boids = 5
    red_start_boids = [(random.randint(0, w_screen), random.randint(0, h_screen)) for _ in range(num_red_boids)]
    blue_start_boids = [(random.randint(0, w_screen), random.randint(0, h_screen)) for _ in range(num_blue_boids)]
    red_boids = [Boid(x, y, 10, (255, 0, 0)) for x, y in red_start_boids]
    blue_boids = [Boid(x, y, 10, (0, 0, 255)) for x, y in blue_start_boids]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        
        for red_boid in red_boids:
            seek_mouse([red_boid])
            red_boid.avoid_colition(red_boids + blue_boids)
    
        for blue_boid in blue_boids:
            flee_mouse([blue_boid], 100)
            blue_boid.avoid_colition(blue_boids + red_boids)
        
        for boid in red_boids + blue_boids:
            boid.update()
            boid.draw(screen)
        
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()