import pygame
import os
import sys


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def explosion_large():
    # 外星人到达了屏幕底部或者撞到飞船的大爆炸声
    explosion_large = pygame.mixer.Sound(get_resource_path("music/Explo_Large.wav"))
    explosion_large.play()


def explosion_small():
    # 增加子弹和外星人碰撞的小爆炸声
    explosion_small = pygame.mixer.Sound(get_resource_path("music/Explo_Small.wav"))
    explosion_small.play()


def bullet_whiz():
    # 增加子弹射出的biu声
    bullet_whiz = pygame.mixer.Sound(get_resource_path("music/Bullet_Whiz.wav"))
    bullet_whiz.play()


def bg_music():
    # 游戏背景音乐（若游戏开始就一直播放）
    pygame.mixer.music.load(get_resource_path("music/order_music.mp3"))

