import json
import os
import sys


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class GameStats():
    """ 跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        """ 初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # 游戏刚启动时处于非活动状态~
        self.game_active = False
        self.continue_active = False

        # 在如何情况下都不应重置最高得分
        self.high_score = 0
        with open(get_resource_path('high_score.json')) as f_obj:
            self.high_score = json.load(f_obj)

    def reset_stats(self):
        """ 初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
