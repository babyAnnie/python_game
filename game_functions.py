import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import json
import all_music as am
import os
import sys


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def play_bg_music():
    # 检查背景音乐流播放，有返回True，没有返回False    如果没有音乐流则选择播放
    """ 此方法同Sound方法一样！都是以流的方式呈现。一直播放需要使用while循环！"""
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(loops=0,start=0)


def pause_bg_music():
    # 暂停背景音乐
    """ 此方法同Sound方法一样！都是以流的方式呈现。一直播放需要使用while循环！"""
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()


def check_high_score(stats, sb):
    """ 检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ 检查是否有外星人到达了屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            """ 像飞船被撞到一样进行处理"""
            am.explosion_large()
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ 响应被外星人撞到的飞船"""

    if stats.ships_left > 0:
        am.explosion_large()
        # 将ships_left减一
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def change_fleet_direction(ai_settings, aliens):
    """ 将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """ 有外星人到达边缘时采取向右相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ 检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    """ 检测外星人和飞船之间的碰撞"""
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    """ 检查是否有外星人到达屏幕底部"""
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_rows(ai_settings, ship_height, alien_height):
    """ 计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(ai_settings, alien_width):
    """ 计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ 创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """ 创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            """创建一个外星人并将其加入当前行"""
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def fire_bullet(ai_settings, screen, ship, bullets):
    """ 如果还没有到达限制，就发射一颗子弹"""
    """ 创建一颗子弹，并将其加入到编组bullets中"""

    if len(bullets) < ai_settings.bullets_allowed:
        am.bullet_whiz()
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb, aliens):
    """ 响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        # 退出游戏
        with open(get_resource_path('high_score.json'), 'w') as f_obj:
            json.dump(stats.high_score, f_obj)
        pygame.quit()
        sys.exit()
    elif event.key == pygame.K_r:
        # 重新开始游戏
        start_play_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
        stats.game_active = True
        stats.continue_active = False
    elif event.key == pygame.K_w:
        # 暂停游戏
        # 显示光标
        pygame.mouse.set_visible(True)
        stats.continue_active = True
        stats.game_active = False
        # pause_bg_music()
    #     sleep(3600)
    elif event.key == pygame.K_c:
        # 继续游戏
        pygame.mouse.set_visible(False)
        stats.continue_active = False
        stats.game_active = True


def check_keyup_events(event, ship):
    """ 响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """ 在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        # start_play_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
        stats.game_active = True
        stats.continue_active = False


def start_play_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    if not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """ 响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open(get_resource_path('high_score.json'), 'w') as f_obj:
                json.dump(stats.high_score, f_obj)
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, continue_button):
    """ 更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都会重绘屏幕
    screen.fill(ai_settings.bg_color)
    """ 在飞船和外星人后面重绘所有子弹"""
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blit_me()
    aliens.draw(screen)
    # 显示得分
    sb.show_score()
    # 如果游戏处于非活动状态，就绘制Play按钮
    if (stats.game_active is False) & (stats.continue_active is False):
        play_button.draw_button()
    elif stats.continue_active is True:
        continue_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, bullets, aliens):
    """ 更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ 响应子弹和外星人的碰撞"""
    """ 检查是否有子弹击中了外星人，如果击中就删除相应的子弹和外星人"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        am.explosion_small()
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        """ 删除现有的子弹,加快游戏节奏，并新建一群外星人"""
        # 如果整群外星人都被消灭，就提高一个等级
        bullets.empty()
        ai_settings.increase_speed()

        start_new_level(stats, sb)

        create_fleet(ai_settings, screen, ship, aliens)


def start_new_level(stats, sb):
    # 提高等级
    stats.level += 1
    sb.prep_level()
