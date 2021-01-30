import pygame
import sys
import json
import socket
import time
from _thread import *

color_white = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
color_green = (0, 255, 0)
color_red = (255, 0, 0)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
res = (1024,720)
commands = ""

cfg = open("client_config.json", "r")
tmpconfig = cfg.read()
cfg.close()
config = json.loads(tmpconfig)

host = config["server"]
port = config["port"]

Client = socket.socket()
pygame.init()
screen = pygame.display.set_mode(res)
width = screen.get_width()
height = screen.get_height()
smallfont = pygame.font.SysFont('Corbel',32)
tinyfont = pygame.font.SysFont('Corbel',12)


class Button_class:
    def __init__(self, loc_x, loc_y, size_x, size_y, text, function):
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.size_x = size_x
        self.size_y = size_y
        self.text = text
        self.function = function
    def draw(self, screen, color):
        pygame.draw.rect(screen,color,[self.loc_x, self.loc_y, self.size_x, self.size_y])
        text = smallfont.render(self.text , True , color_white)
        screen.blit(text , (self.loc_x, self.loc_y))

class Text_class:
    def __init__(self, loc_x, loc_y, size, text, color):
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.text = text
        self.size = size
        self.color = color
    def draw(self, screen, color):
        font = pygame.font.SysFont('Corbel',self.size)
        text = font.render(self.text , True , color_white)
        screen.blit(text , (self.loc_x, self.loc_y))

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = smallfont.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    global commands
                    commands +=  self.text + ";"
                    self.text = ""

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = smallfont.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):

        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


Commands_in_file = []

Valid_commands =[
"Forward()",
"Back()",
"Left()",
"Right()",
"Arm_up()",
"Arm_down()",
"Arm_Forward()",
"Arm_Back()",
"Arm_Left()",
"Arm_Right()",
"Camera_Left()",
"Camera_Right()"
]


Buttons = [
Button_class(650, 670, 65, 40, "Quit", "Close_window"),
Button_class(230, 120, 70, 70, "Forward", "Forward"),
Button_class(230, 280, 70, 70, "Back", "Back"),
Button_class(150, 200, 70, 70, "Left", "Left"),
Button_class(310, 200, 70, 70, "Right", "Right"),
Button_class(460, 120, 70, 70, "Up", "Arm_up"),
Button_class(460, 280, 70, 70, "Down", "Arm_down"),
Button_class(660, 120, 70, 70, "Forward", "Arm_Forward"),
Button_class(660, 280, 70, 70, "Back", "Arm_Back"),
Button_class(580, 200, 70, 70, "Left", "Arm_Left"),
Button_class(740, 200, 70, 70, "Right", "Arm_Right"),
Button_class(150, 500, 70, 70, "Left", "Camera_Left"),
Button_class(310, 500, 70, 70, "Right", "Camera_Right"),
Button_class(850, 670, 120, 40, "Read File", "Read_from_file")
]


Input_boxes = [

# InputBox(400, 100, 140, 32)
]


Texts = [
Text_class(170, 50, 36, "Rover Controls", color_white),
Text_class(520, 50, 36, "Arm Controls", color_white),
Text_class(170, 430, 36, "Camera Controls", color_white)
]

def Close_window():
    print("Closing Client")
    pygame.quit()

def Check_commands():
    global Commands_in_file
    Commands_in_file = []
    input_file = open("commands.txt", "r")
    check = True
    y = 20
    for line in input_file:

        if line.rstrip() not in Valid_commands:
            print("not okay")
            Commands_in_file.append(Text_class(820, y, 16, line.rstrip() + "  <----", color_white))
            check = False
        else:
            Commands_in_file.append(Text_class(820, y, 16, line.rstrip(), color_white))
            print("okay")
        y += 18
    input_file.close()
    return check

def Read_from_file():

    if Check_commands() == True:
        input_file = open("commands.txt", "r")
        for line in input_file:
            print("yay")
            data = line.rstrip()
            Client.send(str.encode(data))
            print("Sent from file: " + data)
            time.sleep(0.1)
        input_file.close()

def main_loop():
    while True:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            #checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for Button in Buttons:
                    if Button.loc_x <= mouse[0] <= Button.loc_x + Button.size_x and Button.loc_y <= mouse[1] <= Button.loc_y + Button.size_y:
                        if Button.function + "()" in Valid_commands:
                            Client.send(str.encode(Button.function + "()"))
                        else:
                            eval(Button.function + "()")
            for Box in Input_boxes:
                Box.handle_event(ev)

        screen.fill((60,25,60))

        mouse = pygame.mouse.get_pos()

        for Button in Buttons:
            if Button.loc_x <= mouse[0] <= Button.loc_x + Button.size_x and Button.loc_y <= mouse[1] <= Button.loc_y + Button.size_y:
                Button.draw(screen, color_light)
            else:
                Button.draw(screen, color_dark)

        for Box in Input_boxes:
            Box.update()
        for Box in Input_boxes:
            Box.draw(screen)
        for Text in Texts:
            Text.draw(screen, color_white)
        for Command_in_file in Commands_in_file:
            Command_in_file.draw(screen, color_white)

        pygame.display.update()

if __name__ == '__main__':
    print('Waiting for connection response')
    try:
        Client.connect((host, port))
    except socket.error as e:
        print(str(e))
    res = Client.recv(2048)
    # start_new_thread(listen_for_down, (Client, ))
    main_loop()
    pygame.quit()
