from interfaces import DataBase
import os
import datetime
import time

class IsPlayingDataBase(DataBase):

    def __init__(self,):
        super().__init__(env=os.environ['ENVIRONMENT'], name='is_playing_time')
        # ゲームのプレイ開始終了の管理
        self.isPlayerGaming = {}
        # ゲームのプレイ時間の管理
        self.isPlayingTime = []

    
    def start(self, before, after):
        
        self.isPlayerGaming.setdefault(after.name, [after.activity.name, datetime.datetime.now(), time.time()])
        print("__" + after.name + "__が" + after.activity.name, "を開始しました。")

    def finish(self, before, after):

        playingTime = (time.time() - self.isPlayerGaming[before.name][-1])
        self.isPlayingTime.append([before.name, self.isPlayerGaming[before.name][0], self.isPlayerGaming[before.name][1], datetime.datetime.now(), time.strftime("%H時間%M分", time.gmtime(int(playingTime)))])
        del self.isPlayerGaming[before.name]
        print("__" + before.name + "__が" + before.activity.name, "を{}プレイをして終了しました。".format(time.strftime("%H時間%M分", time.gmtime(int(playingTime)))))

    def get_data(self, ):
        return self.isPlayerGaming

    def define_columns(self, ):
        raise NotImplementedError()

    def update(self,):
        raise NotImplementedError()

    def commit(self, ):
        raise NotImplementedError()