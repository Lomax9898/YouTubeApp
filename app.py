import pygame
import pyperclip
import urllib.request, io
from pytube import YouTube


# Issue with jpg files loading in pygame versions above 1.9.6 reference > https://github.com/pygame/pygame/issues/1516
class App:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.fontsize = 30
        self.basefont = pygame.font.SysFont('Arial', 30, bold=True)
        self.subfont = pygame.font.SysFont('Arial', 20, bold=True)
        self.screen = pygame.display.set_mode((800, 800))
        self.screen.fill(pygame.Color('lightsteelblue4'))
        self.Thumbnail_Size = (700, 400)
        self.link = ''  # https://www.youtube.com/watch?v=vFrvFKOVU6A'
        self.yt = ''  # YouTube(self.link)
        self.user_link = ' '  # self.link
        self.user_location = "C:\\Users\\Kevin\\Desktop"
        self.input_link = pygame.Rect(108, 20, 600, 35)
        self.input_location = pygame.Rect(290, 70, 418, 35)
        self.active_link = False
        self.active_location = False
        self.DL18 = pygame.Rect(170, 650, 100, 32)
        self.DL22 = pygame.Rect(170, 700, 100, 32)
        self.DL140 = pygame.Rect(620, 650, 100, 32)
        self.DL251 = pygame.Rect(620, 700, 100, 32)
        self.titlex = 250
        self.clicked_DL18 = False
        self.clicked_DL22 = False
        self.clicked_DL140 = False
        self.clicked_DL251 = False
        self.enabled_DL18 = False
        self.enabled_DL22 = False
        self.enabled_DL140 = False
        self.enabled_DL251 = False
        self.text = ''
        self.vecounter = 0
        self.aucounter = 0


    def Program(self):
        self.link= self.user_link
        self.yt = YouTube(self.link)
        self.url = self.yt.thumbnail_url
        print(self.yt.streams.filter(progressive=True))
        print(self.yt.streams.filter(only_audio=True))
        print(len(self.yt.streams.filter(progressive=True)))
        print(len(self.yt.streams.filter(only_audio=True)))
        self.video = self.yt.streams.filter(progressive=True)
        self.audio = self.yt.streams.filter(only_audio=True)
        self.videotitle = self.basefont.render("Video & Audio", True, (0, 0, 0))
        self.audiotitle = self.basefont.render("Audio Only", True, (0, 0, 0))
        r = urllib.request.urlopen(self.url).read()
        print("For video:")
        if "18" in str(self.video):
            print("18 is here")
            self.vecounter += 1
            self.enabled_DL18 = True
        else:
            print("18 is not here")
        if "22" in str(self.video):
            print("22 is here")
            self.vecounter += 1
            self.enabled_DL22 = True
        else:
            print("22 is not here")
        print("For Audio")
        if "140" in str(self.audio):
            print("140 is here")
            self.aucounter += 1
            self.enabled_DL140 = True
        else:
            print("140 is not here")
        if "249" in str(self.audio):
            print("249 is here")
            self.aucounter += 1
        else:
            print("249 is not here")
        if "250" in str(self.audio):
            print("250 is here")
            self.aucounter += 1
        else:
            print("250 is not here")
        if "251" in str(self.audio):
            print("251 is here")
            self.enabled_DL251 = True
            self.aucounter += 1
        else:
            print("251 is not here")

        if self.vecounter == len(self.yt.streams.filter(progressive=True)):
            print("All possible videos are counted for")
        else:
            print("Missing possible videos")
        if self.aucounter == len(self.yt.streams.filter(only_audio=True)):
            print("All possible audios are counted for")
        else:
            print("Missing possible audios")

        img = io.BytesIO(r)
        image = pygame.image.load(img).convert()
        image = pygame.transform.scale(image, self.Thumbnail_Size)
        self.screen.blit(image, (50, 120))
        if len(self.yt.title) > 50:
            title = '%.50s' % self.yt.title + "..."
        else:
            title = '%.50s' % self.yt.title
        if len(title) >= 25:
            for x in range(25, len(title), 5):
                self.titlex -= 29
        self.titlefont = pygame.font.SysFont('Arial', self.fontsize, bold=True)
        self.textsurface = self.titlefont.render(title, True, (0, 0, 0))
        print(self.titlex)
        print(self.fontsize)

        self.screen.blit(self.textsurface, (self.titlex, 550))
        self.screen.blit(self.videotitle, (100, 600))
        self.screen.blit(self.audiotitle, (550, 600))
        pygame.display.flip()

    def menu(self):
        DLtext = self.basefont.render(f"Download Location:", True, (pygame.Color("black")))
        URLtxt = self.basefont.render(f"URL:", True, (pygame.Color("black")))
        self.screen.blit(DLtext, (50, 70))
        self.screen.blit(URLtxt, (48, 20))
        color = pygame.Color('deepskyblue4')
        color_active = pygame.Color('cadetblue1')
        color2 = pygame.Color('deepskyblue4')
        color_active2 = pygame.Color('cadetblue1')
        if self.active_link:
            color = color_active
        if self.active_location:
            color2 = color_active2
        pygame.draw.rect(self.screen, color, self.input_link)
        pygame.draw.rect(self.screen, color2, self.input_location)
        text_surface = self.basefont.render(self.user_link, True, (pygame.Color("black")))
        text_surface2 = self.basefont.render(self.user_location, True, (pygame.Color("black")))
        self.screen.blit(text_surface, self.input_link)
        self.screen.blit(text_surface2, self.input_location)
        pygame.display.flip()


    def Paste(self):
        self.text = pyperclip.paste()
        lines = self.text.split("\n")
        for line in range(len(lines)):
            lines[line] = '*' + lines[line]
        pyperclip.copy(self.text)

    def redraw(self):
        self.screen.fill((255, 255, 255))

    def run(self):
        running = True
        while running:
            pygame.display.update()
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_link.collidepoint(event.pos):
                        self.active_link = True
                    else:
                        self.active_link = False

                if event.type == pygame.KEYDOWN:
                    if self.active_link:
                        if event.key == pygame.K_v:
                            mods = pygame.key.get_mods()
                            if mods & pygame.KMOD_CTRL:
                                self.Paste()
                                self.user_link = self.text
                                self.text = ''
                        elif event.key == pygame.K_RETURN:
                            self.screen.fill(pygame.Color('lightsteelblue4'))
                            self.enabled_DL18 = False
                            self.enabled_DL22 = False
                            self.enabled_DL140 = False
                            self.enabled_DL251 = False
                            self.titlex = 250
                            self.Program()
                        elif event.key == pygame.K_BACKSPACE:
                            self.user_link = self.user_link[:-1]
                        else:
                            self.user_link += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_location.collidepoint(event.pos):
                        self.active_location = True
                    else:
                        self.active_location = False

                if event.type == pygame.KEYDOWN:
                    if self.active_location:
                        if event.key == pygame.K_v:
                            mods = pygame.key.get_mods()
                            if mods & pygame.KMOD_CTRL:
                                self.Paste()
                                self.user_location = self.text
                                self.text = ''
                        if event.key == pygame.K_BACKSPACE:
                            self.user_location = self.user_location[:-1]
                        else:
                            self.user_location += event.unicode
                DL = self.subfont.render(f"Download", True, (pygame.Color("black")))
                if self.enabled_DL18:
                    lineDL18 = self.subfont.render(f"360p MP4", True, (pygame.Color("black")))
                    self.screen.blit(lineDL18, (80, 653))
                    if self.DL18.collidepoint(mouse):
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue3'), self.DL18)
                        self.screen.blit(DL, (180, 653))
                    else:
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue4'), self.DL18)
                        self.screen.blit(DL, (180, 653))
                if self.enabled_DL22:
                    lineDL22 = self.subfont.render(f"720p MP4", True, (pygame.Color("black")))
                    self.screen.blit(lineDL22, (80, 700))
                    if self.DL22.collidepoint(mouse):
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue3'), self.DL22)
                        self.screen.blit(DL, (180, 703))
                    else:
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue4'), self.DL22)
                        self.screen.blit(DL, (180, 703))

                if self.enabled_DL140:
                    lineDL140 = self.subfont.render(f"128kbps MP4A", True, (pygame.Color("black")))
                    self.screen.blit(lineDL140, (500, 653))
                    if self.DL140.collidepoint(mouse):
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue3'), self.DL140)
                        self.screen.blit(DL, (630, 653))
                    else:
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue4'), self.DL140)
                        self.screen.blit(DL, (630, 653))
                if self.enabled_DL251:
                    lineDL251 = self.subfont.render(f"160kbps WEBM", True, (pygame.Color("black")))
                    self.screen.blit(lineDL251, (495, 703))
                    if self.DL251.collidepoint(mouse):
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue3'), self.DL251)
                        self.screen.blit(DL, (630, 703))
                    else:
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue4'), self.DL251)
                        self.screen.blit(DL, (630, 703))

                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                self.menu()


if __name__ == '__main__':
    app = App()
    app.run()
