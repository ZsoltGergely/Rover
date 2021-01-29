import pygame
import sys
import matplotlib

color_white = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
res = (1024,720)
commands = ""

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




def Close_window():
    print("Yes")
    pygame.quit()

def Forward():
    print("Going forward")

def Back():
    print("Going back")

def Left():
    print("Going left")

def Right():
    print("Going right")

def Arm_up():
    print("Moving arm up")

def Arm_down():
    print("Moving arm down")

def Arm_Forward():
    print("Moving arm forward")

def Arm_Back():
    print("Moving arm back")

def Arm_Left():
    print("Moving arm left")

def Arm_Right():
    print("Moving arm right")





Buttons = [
Button_class(650, 670, 65, 40, "Quit", "Close_window"),
Button_class(230, 120, 70, 70, "Forward", "Forward"),
Button_class(230, 280, 70, 70, "Back", "Back"),
Button_class(150, 200, 70, 70, "Left", "Left"),
Button_class(310, 200, 70, 70, "Right", "Right"),
Button_class(460, 120, 70, 70, "Up", "Arm_up"),
Button_class(460, 280, 70, 70, "Down", "Arm_down"),
Button_class(620, 120, 70, 70, "Forward", "Arm_Forward"),
Button_class(620, 280, 70, 70, "Back", "Arm_Back"),
Button_class(540, 200, 70, 70, "Left", "Arm_Left"),
Button_class(700, 200, 70, 70, "Right", "Arm_Right")
]

Input_boxes = [

# InputBox(400, 100, 140, 32)
]

Text = 


def main_loop():
    while True:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            #checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for Button in Buttons:
                    if Button.loc_x <= mouse[0] <= Button.loc_x + Button.size_x and Button.loc_y <= mouse[1] <= Button.loc_y + Button.size_y:
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

        pygame.display.update()

if __name__ == '__main__':
    main_loop()
    pygame.quit()
