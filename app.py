import io
import urllib.request

import pygame
import pyperclip
from pytube import YouTube
from pytube.exceptions import RegexMatchError


class App:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.audio_title = None  # Initializing parameters
        self.video_title = None
        self.audio = None
        self.video = None
        self.url = None
        self.title_font = None
        self.text_surface = None
        self.font_size = 30
        self.base_font = pygame.font.SysFont('Arial', 30, bold=True)  # Pygame UI font, color, and screen
        self.sub_font = pygame.font.SysFont('Arial', 20, bold=True)
        self.screen = pygame.display.set_mode((800, 800))
        self.screen.fill(pygame.Color('lightsteelblue4'))
        self.Thumbnail_Size = (700, 400)
        self.link = ''  # https://www.youtube.com/watch?v=dQw4w9WgXcQ' Pytube parameters
        self.yt = ''  # YouTube(self.link)
        self.user_link = ' '  # self.link
        self.user_location = r""
        self.input_link = pygame.Rect(108, 20, 645, 35)  # Pygame Rectangles to type in
        self.input_location = pygame.Rect(290, 70, 462, 35)
        self.active_link = False
        self.active_location = False
        self.DL18 = pygame.Rect(170, 650, 100, 32)  # Rectangles for the buttons
        self.DL22 = pygame.Rect(170, 700, 100, 32)
        self.DL140 = pygame.Rect(620, 650, 100, 32)
        self.DL251 = pygame.Rect(620, 700, 100, 32)
        self.title_x_value = 250
        self.stream = 0
        self.enabled_DL18 = False
        self.enabled_DL22 = False
        self.enabled_DL140 = False
        self.enabled_DL251 = False
        self.text = ''

    def program(self):  # This is where all the pytube related code is, in order to get the video info
        self.link = self.user_link
        self.yt = YouTube(self.link)
        self.url = self.yt.thumbnail_url
        self.video = self.yt.streams.filter(progressive=True)  # This is where the video and audio is grabbed
        self.audio = self.yt.streams.filter(only_audio=True)
        self.video_title = self.base_font.render("Video & Audio", True, (0, 0, 0))
        self.audio_title = self.base_font.render("Audio Only", True, (0, 0, 0))
        r = urllib.request.urlopen(self.url).read()  # Opens the thumbnail url and gets the image
        # For video:
        if "18" in str(self.video):
            self.enabled_DL18 = True
        if "22" in str(self.video):
            self.enabled_DL22 = True

        # For Audio:
        if "140" in str(self.audio):
            self.enabled_DL140 = True
        if "251" in str(self.audio):
            self.enabled_DL251 = True

        img = io.BytesIO(r)  # converts the image from bytes
        image = pygame.image.load(img).convert()  # loads the image
        image = pygame.transform.scale(image, self.Thumbnail_Size)  # scales the image
        self.screen.blit(image, (50, 120))  # displays the image
        if len(self.yt.title) > 50:  # If the title gets too long, it gets shorten and ... added to the end
            title = '%.50s' % self.yt.title + "..."
        else:
            title = '%.50s' % self.yt.title
        if len(title) >= 25:  # moves the position of the title to left if the title is long
            for x in range(25, len(title), 5):
                self.title_x_value -= 29
        self.title_font = pygame.font.SysFont('Arial', self.font_size, bold=True)
        try:  # try catches error from titles with unsupported characters
            self.text_surface = self.title_font.render(title, True, (0, 0, 0))
        except UnicodeError:
            self.title_x_value = 250
            title = 'Error: A Unicode character not supported'
            self.text_surface = self.title_font.render(title, True, (0, 0, 0))
        self.screen.blit(self.text_surface, (self.title_x_value, 550))
        self.screen.blit(self.video_title, (100, 600))
        self.screen.blit(self.audio_title, (550, 600))
        pygame.display.flip()

    def menu(self):  # Contains the colors and text for the UI
        dl_text = self.base_font.render(f"Download Location:", True, (pygame.Color("black")))
        url_txt = self.base_font.render(f"URL:", True, (pygame.Color("black")))
        self.screen.blit(dl_text, (50, 70))
        self.screen.blit(url_txt, (48, 20))
        color = pygame.Color(
            'deepskyblue4')  # When you click the mouse over the inputs it should change to color_active
        color_active = pygame.Color('cadetblue1')
        color2 = pygame.Color('deepskyblue4')
        color_active2 = pygame.Color('cadetblue1')
        if self.active_link:
            color = color_active
        if self.active_location:
            color2 = color_active2
        pygame.draw.rect(self.screen, color, self.input_link)
        pygame.draw.rect(self.screen, color2, self.input_location)
        text_surface = self.base_font.render(self.user_link, True, (pygame.Color("black")))
        text_surface2 = self.base_font.render(self.user_location, True, (pygame.Color("black")))
        self.screen.blit(text_surface, self.input_link)
        self.screen.blit(text_surface2, self.input_location)
        pygame.display.flip()

    def paste(self):  # Paste whatever text is in the clipboard into a box with control + v
        self.text = pyperclip.paste()
        lines = self.text.split("\n")
        for line in range(len(lines)):
            lines[line] = '*' + lines[line]
        pyperclip.copy(self.text)

    def downloading_text(self):  # Made this to compress 4 lines into 1
        self.screen.fill(pygame.Color('lightsteelblue4'))
        self.title_x_value = 250
        self.program()
        self.menu()

    def run(self):  # Detects mouse and keyboard inputs
        confirm_dl_text = self.base_font.render(f"Downloading...", True, (pygame.Color("black")))
        warning_text = self.base_font.render(f"Please give valid Youtube URL and file path", True,
                                             (pygame.Color("black")))
        running = True

        while running:  # Keeps checking for button presses, mouse position, and screen updates
            pygame.display.update()
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:  # Confirms button has been pressed
                    if self.input_link.collidepoint(event.pos):
                        self.active_link = True
                    else:
                        self.active_link = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_location.collidepoint(event.pos):
                        self.active_location = True
                    else:
                        self.active_location = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.DL18.collidepoint(event.pos):  # Depending on the point of collision between mouse and box
                        self.stream = self.yt.streams.get_by_itag(18)
                        self.screen.blit(confirm_dl_text, (320, 750))
                        pygame.display.flip()  # Shows a text that the video is downloading then downloads
                        self.stream.download(output_path=self.user_location)
                        self.downloading_text()
                    elif self.DL22.collidepoint(event.pos):
                        self.stream = self.yt.streams.get_by_itag(22)
                        self.screen.blit(confirm_dl_text, (320, 750))
                        pygame.display.flip()
                        self.stream.download(output_path=self.user_location)
                        self.downloading_text()
                    elif self.DL140.collidepoint(event.pos):
                        self.stream = self.yt.streams.get_by_itag(140)
                        self.screen.blit(confirm_dl_text, (320, 750))
                        pygame.display.flip()
                        self.stream.download(output_path=self.user_location)
                        self.downloading_text()
                    elif self.DL251.collidepoint(event.pos):
                        self.stream = self.yt.streams.get_by_itag(251)
                        self.screen.blit(confirm_dl_text, (320, 750))
                        pygame.display.flip()
                        self.stream.download(output_path=self.user_location)
                        self.downloading_text()

                if event.type == pygame.KEYDOWN:
                    if self.active_link:  # This is for the link box, showing the user that it is active
                        if event.key == pygame.K_v:
                            mods = pygame.key.get_mods()
                            if mods & pygame.KMOD_CTRL:  # Allows users to paste links
                                self.paste()
                                self.user_link = self.text
                                self.text = ''
                        elif event.key == pygame.K_RETURN:  # Makes pytube collect the data for the program
                            self.screen.fill(pygame.Color('lightsteelblue4'))
                            self.enabled_DL18 = False
                            self.enabled_DL22 = False
                            self.enabled_DL140 = False
                            self.enabled_DL251 = False
                            self.title_x_value = 250  # Reset the x value for the title
                            try:  # Catches invalid inputs
                                self.program()
                            except RegexMatchError:
                                self.screen.blit(warning_text, (140, 750))
                                print('Please give valid Youtube URL and file path')
                        elif event.key == pygame.K_BACKSPACE:  # Allows the user to use backspace
                            self.user_link = self.user_link[:-1]
                        else:
                            self.user_link += event.unicode

                if event.type == pygame.KEYDOWN:
                    if self.active_location:
                        if event.key == pygame.K_v:
                            mods = pygame.key.get_mods()
                            if mods & pygame.KMOD_CTRL:
                                self.paste()
                                self.user_location = self.text
                                self.text = ''
                        elif event.key == pygame.K_RETURN:
                            self.screen.fill(pygame.Color('lightsteelblue4'))
                            self.enabled_DL18 = False
                            self.enabled_DL22 = False
                            self.enabled_DL140 = False
                            self.enabled_DL251 = False
                            self.title_x_value = 250
                            try:
                                self.program()
                            except RegexMatchError:
                                self.screen.blit(warning_text, (140, 750))
                                print('Please give valid Youtube URL and file path')
                        elif event.key == pygame.K_BACKSPACE:
                            self.user_location = self.user_location[:-1]
                        else:
                            self.user_location += event.unicode

                dl = self.sub_font.render(f"Download", True, (pygame.Color("black")))
                if self.enabled_DL18:  # Buttons are enabled to be clicked on and show that they have been clicked on
                    line_dl18 = self.sub_font.render(f"360p MP4", True, (pygame.Color("black")))
                    self.screen.blit(line_dl18, (80, 653))
                    if self.DL18.collidepoint(mouse):
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue3'), self.DL18)
                        self.screen.blit(dl, (180, 653))
                    else:
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue4'), self.DL18)
                        self.screen.blit(dl, (180, 653))
                if self.enabled_DL22:
                    line_dl22 = self.sub_font.render(f"720p MP4", True, (pygame.Color("black")))
                    self.screen.blit(line_dl22, (80, 700))
                    if self.DL22.collidepoint(mouse):
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue3'), self.DL22)
                        self.screen.blit(dl, (180, 703))
                    else:
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue4'), self.DL22)
                        self.screen.blit(dl, (180, 703))

                if self.enabled_DL140:
                    line_dl140 = self.sub_font.render(f"128kbps MP4A", True, (pygame.Color("black")))
                    self.screen.blit(line_dl140, (500, 653))
                    if self.DL140.collidepoint(mouse):
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue3'), self.DL140)
                        self.screen.blit(dl, (630, 653))
                    else:
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue4'), self.DL140)
                        self.screen.blit(dl, (630, 653))
                if self.enabled_DL251:
                    line_dl251 = self.sub_font.render(f"160kbps WEBM", True, (pygame.Color("black")))
                    self.screen.blit(line_dl251, (495, 703))
                    if self.DL251.collidepoint(mouse):
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue3'), self.DL251)
                        self.screen.blit(dl, (630, 703))
                    else:
                        pygame.draw.rect(self.screen, pygame.Color('deepskyblue4'), self.DL251)
                        self.screen.blit(dl, (630, 703))

                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                self.menu()


if __name__ == '__main__':
    app = App()
    app.run()
