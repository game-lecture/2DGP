import game_framework
from pico2d import *

import game_world

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



# Boy Event
RIGHTKEY_DOWN, LEFTKEY_DOWN, UPKEY_DOWN, DOWNKEY_DOWN, RIGHTKEY_UP, LEFTKEY_UP, UPKEY_UP, DOWNKEY_UP, SPACE = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHTKEY_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFTKEY_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UPKEY_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWNKEY_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHTKEY_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFTKEY_UP,
    (SDL_KEYUP, SDLK_UP): UPKEY_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWNKEY_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


# Boy States

class WalkingState:

    @staticmethod
    def enter(boy, event):
        if event == RIGHTKEY_DOWN:
            boy.x_velocity += RUN_SPEED_PPS
        elif event == RIGHTKEY_UP:
            boy.x_velocity -= RUN_SPEED_PPS
        if event == LEFTKEY_DOWN:
            boy.x_velocity -= RUN_SPEED_PPS
        elif event == LEFTKEY_UP:
            boy.x_velocity += RUN_SPEED_PPS

        if event == UPKEY_DOWN:
            boy.y_velocity += RUN_SPEED_PPS
        elif event == UPKEY_UP:
            boy.y_velocity -= RUN_SPEED_PPS
        if event == DOWNKEY_DOWN:
            boy.y_velocity -= RUN_SPEED_PPS
        elif event == DOWNKEY_UP:
            boy.y_velocity += RUN_SPEED_PPS



    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        boy.x += boy.x_velocity * game_framework.frame_time
        boy.y += boy.y_velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1280 - 25)
        boy.y = clamp(25, boy.y, 1024 - 25)

    @staticmethod
    def draw(boy):
        if boy.x_velocity > 0:
            boy.image.clip_draw(int(boy.frame) * 100, 100, 100, 100, boy.x, boy.y)
            boy.dir = 1
        elif boy.x_velocity < 0:
            boy.image.clip_draw(int(boy.frame) * 100, 0, 100, 100, boy.x, boy.y)
            boy.dir = -1
        else:
            # if boy x_velocity == 0
            if boy.y_velocity > 0 or boy.y_velocity < 0:
                if boy.dir == 1:
                    boy.image.clip_draw(int(boy.frame) * 100, 100, 100, 100, boy.x, boy.y)
                else:
                    boy.image.clip_draw(int(boy.frame) * 100, 0, 100, 100, boy.x, boy.y)
            else:
                # boy is idle
                if boy.dir == 1:
                    boy.image.clip_draw(int(boy.frame) * 100, 300, 100, 100, boy.x, boy.y)
                else:
                    boy.image.clip_draw(int(boy.frame) * 100, 200, 100, 100, boy.x, boy.y)


next_state_table = {
    WalkingState: {RIGHTKEY_UP: WalkingState, LEFTKEY_UP: WalkingState, RIGHTKEY_DOWN: WalkingState, LEFTKEY_DOWN: WalkingState,
                UPKEY_UP: WalkingState, UPKEY_DOWN: WalkingState, DOWNKEY_UP: WalkingState, DOWNKEY_DOWN: WalkingState,
                SPACE: WalkingState}
}


class Boy:

    def __init__(self):
        self.x, self.y = 1280 // 2, 1024 // 2
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('animation_sheet.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.x_velocity, self.y_velocity = 0, 0
        self.frame = 0
        self.event_que = []
        self.cur_state = WalkingState
        self.cur_state.enter(self, None)

    def get_bb(self):
        # fill here
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))
        #fill here
        draw_rectangle(*self.get_bb())
        #debug_print('Velocity :' + str(self.velocity) + '  Dir:' + str(self.dir) + ' Frame Time:' + str(game_framework.frame_time))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

