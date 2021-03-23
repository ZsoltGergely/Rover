import pygame
import sys
import json
import socket
import time
from _thread import *
from cryptography.fernet import Fernet

color_white = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
color_green = (0, 255, 0)
color_red = (255, 0, 0)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
res = (1024,720)
commands = ""
command_output_height = 20

cfg = open("client_config.json", "r")
tmpconfig = cfg.read()
cfg.close()
config = json.loads(tmpconfig)

host = config["server"]
port = config["port"]
key = config["key"]


Client = socket.socket()
pygame.init()
screen = pygame.display.set_mode(res)
width = screen.get_width()
height = screen.get_height()
smallfont = pygame.font.SysFont('Corbel',32)
tinyfont = pygame.font.SysFont('Corbel',12)
crypto = Fernet(key)


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

    def __init__(self, x, y, w, h, function, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.function = function
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
                    eval(self.function + "(" + str(self.text) + ")")
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

Rover_move_commands =[
"Forward()",
"Back()"

]
Rover_turn_commands = [
"Left()",
"Right()"
]
Arm_commands = [
"Arm_up()",
"Arm_down()",
"Arm_Forward()",
"Arm_Back()",
"Arm_Left()",
"Arm_Right()"
]
Camera_commands = [
"Camera_Up()",
"Camera_Down()"
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
Button_class(150, 550, 70, 70, "Left", "Camera_Up"),
Button_class(310, 550, 70, 70, "Right", "Camera_Down"),
Button_class(850, 670, 120, 40, "Read File", "Read_from_file")
]



Input_boxes = [


InputBox(160, 360, 20, 32, "Rover_move_text_func"),
InputBox(160, 420, 20, 32, "Rover_turn_text_func"),
InputBox(590, 360, 20, 32, "Arm_move_text_func"),
InputBox(160, 630, 20, 32, "Cam_deg_text_func")


]

Rover_move = 1
Rover_move_text = Text_class(160, 390, 24, str(Rover_move), color_white)

Rover_turn = 1
Rover_turn_text = Text_class(160, 450, 24, str(Rover_move), color_white)

Arm_move = 10
Arm_move_text = Text_class(590, 400, 24, str(Arm_move), color_white)

Cam_deg = 15
Cam_deg_text = Text_class(160, 670, 24, str(Cam_deg), color_white)


Texts = [
Text_class(170, 50, 36, "Rover Controls", color_white),
Text_class(520, 50, 36, "Arm Controls", color_white),
Text_class(170, 480, 36, "Camera Controls", color_white),
Text_class(20, 370, 24, "Move amount", color_white),
Text_class(20, 430, 24, "Turn amount", color_white)

]


def Arm_move_text_func(value):
    global Arm_move
    global Arm_move_text
    Arm_move = int(value)
    Arm_move_text = Text_class(590, 400, 24, str(Arm_move), color_white)


def Rover_move_text_func(value):
    global Rover_move
    global Rover_move_text
    Rover_move = int(value)
    Rover_move_text = Text_class(160, 400, 24, str(Rover_move), color_white)

def Rover_turn_text_func(value):
    global Rover_turn
    global Rover_turn_text
    Rover_turn = int(value)
    Rover_turn_text = Text_class(160, 450, 24, str(Rover_turn), color_white)

def Cam_deg_text_func(value):
    global Cam_deg
    global Cam_deg_text
    Cam_deg = int(value)
    Cam_deg_text = Text_class(160, 620, 24, str(Cam_deg), color_white)


def Close_window():
    print("Closing Client")
    pygame.quit()

def line_valid(command):
    split = command.split("(")
    if split[0]+"()" in Rover_commands or split[0]+"()" in Arm_commands or split[0]+"()" in Camera_commands:
        try:
            int(split[1][:-1])
            return True
        except ValueError:
            return False

def Check_commands():
    global Commands_in_file
    global command_output_height
    Commands_in_file = []
    input_file = open("commands.txt", "r")
    check = True
    command_output_height = 20
    for line in input_file:

        if not line_valid(line.rstrip()):
            Commands_in_file.append(Text_class(820, command_output_height, 16, line.rstrip() + "  <----", color_white))
            check = False

        else:
            Commands_in_file.append(Text_class(820, command_output_height, 16, line.rstrip(), color_white))


        command_output_height += 18
    input_file.close()
    return check

def Read_from_file():

    if Check_commands() == True:
        input_file = open("commands.txt", "r")
        data = "FL;"
        for line in input_file:
            data += line.rstrip()+";"
        Client.send(str.encode(data))
        print("Sent from file: " + data + "\n" + "Waiting for response...")
        res = Client.recv(2048)
        decrypted_message = crypto.decrypt(res)
        if decrypted_message != data:
            print(decrypted_message)
            print(data)
            print("File transfer not successfull")
        time.sleep(0.1)
        Commands_in_file.append(Text_class(820, command_output_height, 18,"Data transfer successfull", color_white))
        input_file.close()
    else:
        Commands_in_file.append(Text_class(820, command_output_height, 18,"Error in file!",color_white))

def main_loop():
    while True:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            #checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for Button in Buttons:
                    if Button.loc_x <= mouse[0] <= Button.loc_x + Button.size_x and Button.loc_y <= mouse[1] <= Button.loc_y + Button.size_y:
                        if Button.function + "()" in Rover_move_commands:
                            data = Button.function + "(" + str(Rover_move) + ")"
                            Client.send(str.encode(data))
                            print("Sent from file: " + data + "\n" + "Waiting for response...")

                            res = Client.recv(2048)
                            decrypted_message = crypto.decrypt(res)
                            print(decrypted_message)
                        if Button.function + "()" in Rover_turn_commands:
                            data = Button.function + "(" + str(Rover_turn) + ")"
                            Client.send(str.encode(data))
                            print("Sent from file: " + data + "\n" + "Waiting for response...")

                            res = Client.recv(2048)
                            decrypted_message = crypto.decrypt(res)
                            print(decrypted_message)
                        elif Button.function + "()" in Arm_commands:
                            data = Button.function + "(" + str(Rover_move) + ")"
                            Client.send(str.encode(data))
                            print("Sent from file: " + data + "\n" + "Waiting for response...")
                            res = Client.recv(2048)
                            decrypted_message = crypto.decrypt(res)
                            print(decrypted_message)

                        elif Button.function + "()" in Camera_commands:
                            data = Button.function + "(" + str(Cam_deg) + ")"
                            Client.send(str.encode(data))
                            print("Sent from file: " + data + "\n" + "Waiting for response...")
                            res = Client.recv(2048)
                            decrypted_message = crypto.decrypt(res)
                            print(decrypted_message)
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

        Arm_move_text.draw(screen, color_white)
        Rover_move_text.draw(screen, color_white)
        Cam_deg_text.draw(screen, color_white)
        Rover_turn_text.draw(screen, color_white)
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
