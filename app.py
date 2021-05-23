import pygame
import urllib.request, io
from pytube import YouTube
# Issue with jpg files loading in pygame versions above 1.9.6 reference > https://github.com/pygame/pygame/issues/1516
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30, bold=True)
screen = pygame.display.set_mode((800, 800))
screen.fill((255, 255, 255))
DEFAULT_IMAGE_SIZE = (700, 400)

yt = YouTube('https://www.youtube.com/watch?v=gKKGdxbjnt8')
url = yt.thumbnail_url
textsurface = myfont.render(yt.title, False, (0, 0, 0))
r = urllib.request.urlopen(url).read()
img = io.BytesIO(r)
image = pygame.image.load(img).convert()
image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)
screen.blit(image, (50, 20))
screen.blit(textsurface,(250, 450))
pygame.display.flip()
def redraw():
    screen.fill((255, 255, 255))


run = True
while run:
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
