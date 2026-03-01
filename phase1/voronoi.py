from numpy import sqrt
import pygame
from pygame.math import Vector2

import json


WIDTH, HEIGHT = 800, 800
ZOOM = 20          
OFFSET_X = 150
OFFSET_Y = 150
COLORS = [(116, 0, 184), (105, 48, 195), (94, 96, 206), (83, 144, 217), (78, 168, 222), (72, 191, 227),(86, 207, 225),(100, 223, 223),(114, 239, 221),(128, 255, 219)]

class Germ:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.color = (0,0,0)
        self.x_screen = int(x * ZOOM + OFFSET_X)
        self.y_screen = int(HEIGHT - (y * ZOOM + OFFSET_Y))

    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x_screen, self.y_screen), 2)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

with open('pointplan.json', 'r') as f:        
    points = json.load(f)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

liste_germes = []
for p in points:
    nouveau_germe = Germ(p['x'] , p['y'])
    liste_germes.append(nouveau_germe)



def voronoi(liste_germes, x, y):
    min_distance = 800
    closest_germe = None
    px = (x- OFFSET_X)/ZOOM
    py = (HEIGHT - y - OFFSET_Y)/ZOOM
    for germe in liste_germes:
        distance = sqrt((px - germe.position.x) ** 2 + (py - germe.position.y) ** 2)
        if distance < min_distance: 
            min_distance = distance
            closest_germe = germe
    return closest_germe


for x in range(WIDTH):
    for y in range(HEIGHT):
        germe_proche = voronoi(liste_germes, x ,y)
        if germe_proche is not None:
            screen.set_at((x, y), COLORS[liste_germes.index(germe_proche) % len(COLORS)])
  

running = True
while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for germe in liste_germes:
            germe.draw(screen)
        pygame.display.flip()
        pygame.image.save(screen, "voronoi.png")
        
pygame.quit()

