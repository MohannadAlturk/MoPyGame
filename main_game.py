import pygame as py
import tkinter as tk
from tkinter import messagebox
import time
import json


class Game1:
    def __init__(self, speed):
        py.init()

        self.speed = speed
        self.MAX_WIDTH = 800
        self.MAX_HEIGHT = 800
        self.frame_count = 0
        self.counter = 0
        self.time_end = 0
        self.time_start = 0

        self.record = 0

        self.run = True

        self.screen = py.display.set_mode((self.MAX_WIDTH, self.MAX_HEIGHT))

        py.display.set_caption("Collision Detection")
        self.background_image = py.image.load("hintergrundbild1.jpg")
        self.background_image = py.transform.scale(self.background_image, (self.MAX_WIDTH, self.MAX_HEIGHT))

        self.dreieck = py.Rect((55, 60, 20, 20))

        self.wall_top = py.Rect((0, 0, 800, 50))
        self.wall_left = py.Rect((0, 0, 50, 800))
        self.wall_right = py.Rect((750, 0, 50, 800))
        self.wall_bottom = py.Rect((0, 750, 800, 50))
        self.wall1 = py.Rect((0, 120, 680, 50))
        self.wall2 = py.Rect((130, 250, 630, 50))
        self.wall3 = py.Rect((0, 380, 680, 50))
        self.wall4 = py.Rect((130, 510, 630, 50))
        self.wall5 = py.Rect((0, 640, 680, 50))
        self.play_again_button = False
        #self.button_rect = py.Rect(400, 385, 150, 40) ##

        self.win_point = py.Rect((55, 695, 50, 50))

        py.display.set_caption("Text-Label mit Pygame")
        self.font = py.font.Font(None, 36)

    def run_game(self):
        self.read_data()
        while self.run:
            self.build_window()
            self.pop_up_collison()
            self.handel_events()
        py.quit()

    def build_window(self):
        self.time_start = time.time()
        self.screen.fill((250, 250, 250))
        self.screen.blit(self.background_image, (0, 0))

        py.draw.rect(self.screen, (250, 0, 0), self.dreieck)

        py.draw.rect(self.screen, (60, 60, 60), self.wall_top)
        py.draw.rect(self.screen, (60, 60, 60), self.wall_left)
        py.draw.rect(self.screen, (60, 60, 60), self.wall_right)
        py.draw.rect(self.screen, (60, 60, 60), self.wall_bottom)
        py.draw.rect(self.screen, (60, 60, 60), self.wall1)
        py.draw.rect(self.screen, (60, 60, 60), self.wall2)
        py.draw.rect(self.screen, (60, 60, 60), self.wall3)
        py.draw.rect(self.screen, (60, 60, 60), self.wall4)
        py.draw.rect(self.screen, (60, 60, 60), self.wall5)

        #if self.play_again_button:
        #    py.draw.rect(self.screen, (60, 120, 60), self.button_rect) #####

        py.draw.rect(self.screen, (0, 150, 50), self.win_point)

        self.time_label()
        self.record_label()

        if self.frame_count % self.speed == 0:
            key = py.key.get_pressed()
            if key[py.K_d] and self.dreieck.right < self.MAX_WIDTH:
                self.dreieck.move_ip(1, 0)
            elif key[py.K_a] and self.dreieck.left > 0:
                self.dreieck.move_ip(-1, 0)
            elif key[py.K_w] and self.dreieck.top > 0:
                self.dreieck.move_ip(0, -1)
            elif key[py.K_s] and self.dreieck.bottom < self.MAX_HEIGHT:
                self.dreieck.move_ip(0, 1)

        py.display.update()
        self.frame_count += 1

    def time_label(self):
        self.text = self.font.render("Time in seconds: "+str(round(self.counter, 1))+" s", True, (255, 255, 255))
        text_rect = self.text.get_rect()
        text_rect.center = (165, 25)
        self.screen.blit(self.text, text_rect)

    def record_label(self):
        self.text = self.font.render("Record: " + str(self.record) + "s", True, (255, 255, 255))
        text_rect = self.text.get_rect()
        text_rect.center = (600, 25)
        self.screen.blit(self.text, text_rect)

    #def text_label(self):
        #self.text = self.font.render(f"Your time:{round(self.counter,2)}", True, (255, 255, 255))
        #text_rect = self.text.get_rect()
        #text_rect.center = (200, 405)
        #self.screen.blit(self.text, text_rect)

    #def restart_button_label(self):
        #self.text = self.font.render("Play again!", True, (255, 255, 255))
        #text_rect = self.text.get_rect()
        #text_rect.center = (475, 405)
        #self.screen.blit(self.text, text_rect)

    def check_collision(self):
        if self.dreieck.colliderect(self.wall_top) or \
                self.dreieck.colliderect(self.wall_bottom) or \
                self.dreieck.colliderect(self.wall_left) or \
                self.dreieck.colliderect(self.wall_right) or \
                self.dreieck.colliderect(self.wall1) or \
                self.dreieck.colliderect(self.wall2) or \
                self.dreieck.colliderect(self.wall3) or \
                self.dreieck.colliderect(self.wall4) or \
                self.dreieck.colliderect(self.wall5):
            return True

    def check_win(self):
        if self.dreieck.colliderect(self.win_point):
            self.overwrite_data()
            #self.play_again_button = True
            return True

    def pop_up_collison(self):
        if self.check_collision():
            tk.Tk().withdraw()
            messagebox.showinfo("Kollision", "Kollision mit der Wand!")
            self.run = False
        elif self.check_win():
            message1 = f"New record is {self.record}"
            #self.read_data()
            message2 = f"Your time: {round(self.counter, 2)}\nRecord is {round(self.record, 2)}"
            if self.counter <= self.record:
                self.read_data()
                tk.Tk().withdraw()
                messagebox.showinfo("win", message1)
            else:
                tk.Tk().withdraw()
                messagebox.showinfo("win", message2)
            self.run = False

    def handel_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.run = False
            elif event.type == py.MOUSEBUTTONDOWN: ##
                # Mausklick-Ereignis überprüfen ##
                if self.button_rect.collidepoint(event.pos): ##
                    print("Button wurde geklickt!") ##

        self.time_end = time.time()
        self.counter += round(self.time_end, 2) - round(self.time_start, 2)

    def read_data(self):
        with open("data.json", "r") as file:
            data = json.load(file)
        self.record = data["counter"]

    def overwrite_data(self):
        with open("data.json", "r") as file:
            data = json.load(file)
        data_new = {"counter": round(self.counter, 2)}

        if data["counter"] > data_new["counter"]:
            with open("data.json", "w") as file:
                json.dump(data_new, file, indent=4, sort_keys=True)
            self.record = data_new["counter"]


for i in range(10):
    start = Game1(1)
    start.run_game()
