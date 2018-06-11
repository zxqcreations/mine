import pygame
from pygame.locals import *
import numpy as np
import sys
from mine_status import *

'''
    status: x, y, bomb_stat, user_stat
        bomb_stat:
            -1: with bomb
            other: bomb num
        user_stat:
            0: no flipped
            1: flipped
            2: flag
            3: puzzle
    f_status: x, y, bomb_stat, auto_stat
        bomb_stat:
            -1: with bomb
            other: bomb num
        
'''

diff = np.array(((9, 9, 10), (16, 16, 40), (30, 16, 99)))
level = 2
SIZE = diff[level, 0:2]*30
color_line = (117, 117, 117)
color_text = (33, 33, 33)
color_clicked = (187,222,251)
color_bg = (33,150,243)
color_btn = (3,169,244)
color_lose = (211,47,47)
color_bomb_ok = (76,175,80)
color_bomb_wrong = (255,152,0)

mouse_left_up = True
mouse_right_down = False
mouse_old_x = 0
mouse_old_y = 0

lose = False
stop = False
restart = True

status = np.zeros(np.append(diff[level, 0:2]+2, 2), np.int8)
status = mine_status(diff, level)
#f_status = np.zeros(np.append(diff[level, 0:2], 2), np.int8)
#mines = list()

def bomb_cnt(mat):
    cnt = 0
    for i in range(0,3):
        for j in range(0,3):
            if mat[i, j, 0]==-1:
                cnt += 1
    return cnt

def check_rec(m_i, m_j):
    global status
    cnt = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if status[m_i+i, m_j+j, 1]==0:
                cnt += 1
    return cnt

def recur_none(m_i, m_j):
    global status
    status[m_i-1:m_i+2, m_j-1:m_j+2, 1] = 1
    #print('neo item:', m_i, m_j)
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i ==0 and j == 0) and \
               status[m_i+i, m_j+j, 0] == 0 and \
               m_i+i>=1 and m_i+i<diff[level, 0]+1 and \
               m_j+j>=1 and m_j+j<diff[level, 1]+1 and \
               not check_rec(m_i+i, m_j+j) == 0:
                    recur_none(m_i+i, m_j+j)

def handle_event(screen, event):
    global status, mouse_old_x, mouse_old_y, mouse_left_up, \
           color_btn, lose, stop, restart, level
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    if event.type == KEYDOWN:
        keyboard_key = pygame.key.get_pressed()
        if keyboard_key[K_r]:
            restart = True
        if keyboard_key[K_1]:
            level = 0
            restart = True
        if keyboard_key[K_2]:
            level = 1
            restart = True
        if keyboard_key[K_3]:
            level = 2
            restart = True
    if event.type == MOUSEBUTTONDOWN:
        if stop:
            return
        mouse_key = pygame.mouse.get_pressed()
        if mouse_key[0]:
            if mouse_left_up:
                mouse_old_x, mouse_old_y = pygame.mouse.get_pos()
                mouse_left_up = False
                
        if mouse_key[2]:
            x, y = pygame.mouse.get_pos()
            m_i, m_j = int(x/30), int(y/30)
            t = status[m_i+1, m_j+1, 1]
            if not t == 1:
                if t == 0:
                    t = 2
                elif t == 2:
                    t = 3
                elif t == 3:
                    t = 0
            status[m_i+1, m_j+1, 1] = t
            mouse_left_up = True
            
    if event.type == MOUSEBUTTONUP:
        if stop:
            return
        if not mouse_left_up:
            x, y = pygame.mouse.get_pos()
            if (x - mouse_old_x < 30) and (y - mouse_old_y < 30):
                m_i, m_j = int(x/30), int(y/30)
                if status[m_i+1, m_j+1, 1] == 0:
                    status[m_i+1, m_j+1, 1] = 1
                    if status[m_i+1, m_j+1, 0] == 0:
                        recur_none(m_i+1, m_j+1)
                    if status[m_i+1, m_j+1, 0] == -1:
                        lose = True
                    mouse_left_up = True
                else:
                    mouse_left_up = True
            else:
              mouse_left_up = True
def generate_bomb():
    global status, mines 
    mine_cnt = 0
    while True:
        x = np.random.randint(diff[level, 0])
        y = np.random.randint(diff[level, 1])
        
        #if (x not in mines[:, 0]) or (y not in mines[:, 1]):
        if (x, y) not in mines:
            #print(x, y)
            mines.append((x, y))
            status[x+1, y+1, 0] = -1
            mine_cnt += 1
        if mine_cnt == diff[level, 2]:
            break
def cal_mine():
    global status
    for i in range(0, diff[level, 0]):
        for j in range(0, diff[level, 1]):
            if not status[i+1, j+1, 0] == -1:
                mat = status[i:i+3, j:j+3, 0:1]
                cnt = bomb_cnt(mat)
                status[i+1, j+1, 0] = cnt

def get_unflipped():
    global status

def auto_cal():
    global status
    

    

pygame.init()
screen = pygame.display.set_mode(SIZE, 0, 32)
pygame.display.set_caption('Mine')
font = pygame.font.SysFont('arial', 16)

status.generate_bomb()
status.cal_mine()


while True:
    screen.fill(color_bg) 
    for event in pygame.event.get():
        handle_event(screen, event)
        
    if restart:
        SIZE = diff[level, 0:2]*30
        screen = pygame.display.set_mode(SIZE, 0, 32)
        status.fill(0)
        mines.clear()
        mouse_left_up = True
        mouse_right_down = False
        mouse_old_x = 0
        mouse_old_y = 0
        lose = False
        stop = False
        generate_bomb()
        cal_mine()
        restart = False
        
    for i in range(0, diff[level, 0]):
        pygame.draw.line(screen, color_line,
                         (i*30, 0), (i*30, diff[level, 1]*30))
    for i in range(0, diff[level, 1]):
        pygame.draw.line(screen, color_line,
                         (0, i*30), (diff[level, 0]*30, i*30))
    
    x, y = pygame.mouse.get_pos()
    m_i, m_j = int(x/30), int(y/30)
    if not status[m_i+1, m_j+1, 1] == 1:
        btn = screen.subsurface(m_i*30+1, m_j*30+1, 29, 29)
        btn.fill(color_btn)
    
    for i in range(0, diff[level, 0]):
        for j in range(0, diff[level, 1]):
            label = screen.subsurface(i*30+1, j*30+1, 29, 29)
            if status[i+1, j+1, 1] == 1:
                label.fill(color_clicked)
                twh = font.size(str(status[i+1, j+1, 0]))
                label.blit(font.render(str(status[i+1, j+1, 0]),
                                       True, color_text),
                            (15-twh[0]/2,15-twh[1]/2))
            if status[i+1, j+1, 1] == 2:
                if lose and status[i+1, j+1, 0] == -1:
                    label.fill(color_bomb_ok)
                if lose and not status[i+1, j+1, 0] == -1:
                    label.fill(color_bomb_wrong)
                twh = font.size(str('▲'))
                label.blit(font.render(str('▲'),
                                       True, color_text),
                            (15-twh[0]/2,15-twh[1]/2))
            if status[i+1, j+1, 1] == 3:
                twh = font.size(str('?'))
                label.blit(font.render(str('?'),
                                       True, color_text),
                            (15-twh[0]/2,15-twh[1]/2))
            if lose and status[i+1, j+1, 0] == -1 and \
               not status[i+1, j+1, 1] == 2:
                label.fill(color_lose)
                twh = font.size(str('▲'))
                label.blit(font.render(str('▲'),
                                       True, color_text),
                            (15-twh[0]/2,15-twh[1]/2))
                stop = True
    
    pygame.display.update()
