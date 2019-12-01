import random
import json
import pickle
import os

from pico2d import *
import game_framework
import game_world

import main_state

from boy import Boy
from zombie import Zombie


boy = None


name = "WorldBuildState"

menu = None

def enter():
    global menu
    menu = load_image('menu.png')
    hide_cursor()
    hide_lattice()

def exit():
    global menu
    del menu

def pause():
    pass

def resume():
    pass

def get_boy():
    return boy



def create_new_world():
    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    # fill here




def load_saved_world():
    global boy

    # fill here



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_n:
            create_new_world()
            game_framework.change_state(main_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_l:
            load_saved_world()
            game_framework.change_state(main_state)

def update():
    pass

def draw():
    clear_canvas()
    menu.draw(get_canvas_width()//2, get_canvas_height()//2)
    update_canvas()






