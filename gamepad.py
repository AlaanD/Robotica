import pygame

# Inicializar pygame
pygame.init()

# Verificar cuántos joysticks están conectados
num_joysticks = pygame.joystick.get_count()
if num_joysticks == 0:
    print("No se encontraron mandos conectados.")
    quit()

# Seleccionar el primer joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Bucle principal para leer las teclas del mando
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"Botón {event.button} presionado.")
        elif event.type == pygame.JOYBUTTONUP:
            print(f"Botón {event.button} liberado.")
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                print(f"Eje X: {event.value}")
            elif event.axis == 1:
                print(f"Eje Y: {event.value}")

    # Pausa para evitar el uso excesivo de la CPU
    pygame.time.delay(10)
