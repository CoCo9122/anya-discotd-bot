import discord
import random
import datetime
import time
import os
from bisect import bisect


from DiscordActions import *
from config import *
from DiscordBotDataBase import * 

envs = {
    'development': Development,
    'test': Test,
    'production': Production,
}

client = discord.Client(intents=discord.Intents.all())
env = envs[os.environ['ENVIRONMENT']]()

# botのステータスのアクティビティの管理
@client.event
async def on_ready():
    bot_activity_status = BotActivityStatusAction(client)
    await bot_activity_status.exec()()
    del bot_activity_status

# チャンネル入退室時の通知処理 
@client.event
async def on_voice_state_update(member, before, after):

    def prob_choice(items, weights):
        total = weights[-1]
        hi = len(items) - 1
        return items[bisect(weights, random.random() * total, 0, hi)]

    # 通知メッセージを書き込むテキストチャンネル（チャンネルIDを指定）
    voise_channel_bot_send = BotSendAction(client.get_channel(int(os.environ['VOICE_CHAT_TEXT'])))

    # チャンネルへの入室ステータスが変更されたとき（ミュートON、OFFに反応しないように分岐）
    if before.channel != after.channel:

        # 入退室を監視する対象のボイスチャンネル（チャンネルIDを指定）
        announceChannelIds = [int(os.environ['AnnounceChannelId1']), int(os.environ['AnnounceChannelId2'])]

        inMember = [
            '__  が参加しました！おでけけ　おでけけ　ランラララン♪',
            '__  が参加しました！__{}__を知ると世界が平和に？'.format(member.name),
            '__  が参加しました！アーニャんちへ　いらさいませ！',
            '__  が参加しました！こ…ころしや…!!すぱい　ころしや　わくわくっ!!',
            "__  が参加しました！"
        ]
        inWeights = [1, 1, 1, 1, 96]

        outMember = [
            '__  が抜けました！あ～　アーニャ__{}__いなくて寂しい～'.format(member.name),
            '__  が抜けました！アーニャ売り飛ばされるー！'
            '__  が抜けました！アーニャおうちかえりたい',
            '__  が抜けました！ひとがごみのようだ',
            "__  が抜けました！",
        ]

        outWeights = [1, 1, 1, 1, 96]

        # 退室通知
        if before.channel is not None and before.channel.id in announceChannelIds:
            randint = random.randrange(0, len(outMember))
            # await botRoom.send("**" + before.channel.name + "** から、__" + member.name + prob_choice(outMember, outWeights))
        # 入室通知
        if after.channel is not None and after.channel.id in announceChannelIds:
            randint = random.randrange(0, len(inMember))
            await voise_channel_bot_send.exec()("**" + after.channel.name + "** に、__" + member.name + prob_choice(inMember, inWeights))

        del voise_channel_bot_send

# メッセージに対して返信処理
@client.event
async def on_message(message):

    def isint(s):  # 整数値を表しているかどうかを判定
        try:
            int(s, 10)  # 文字列を実際にint関数で変換してみる
        except ValueError:
            return False
        else:
            return True

    if message.author.bot: return

    sendMessageAuthor = str(message.author).split('#')[0]


    if int(message.channel.id) == int(os.environ['BulletinChannelId']):
        reaction = BotReactionAction(message)
        if '[報告]' in str(message.content):
            await reaction.exec()('<:report:1010849795541315604>')

        if '[要求]' in str(message.content):
            await reaction.exec()('<:request:1010850049623859260>')

            if '[要求]/thread/' in str(message.content):
                content = str(message.content).split('\n')[0]
                timeWhileArchive = str(content).split('/')[-1]
                threadTitle = str(content).split('/')[-2]

                reply = BotReplyAction(message)
                thread = BotThreadAction(message)

                if len(str(message.content).split('/')) == 4 and isint(timeWhileArchive):
                    await reply.exec()('{}さん、スレッドを作成しました。\nこのスレッドは後{}日でアーカイブされます。'.format(sendMessageAuthor, timeWhileArchive))
                    await thread.exec()(threadTitle, '{}が[要求]で作成しました'.format(sendMessageAuthor), time=1440*int(timeWhileArchive))
                else:
                    await reply.exec()('スレッド作成規約に反しています。[提案]/thread/スレッド名/日にち(整数型)になります。')
                del reply
                del thread

        if '[提案]' in str(message.content):
            await reaction.exec()('<:proposal:1010849591253540935>')

            if '[提案]/thread/' in str(message.content):
                content = str(message.content).split('\n')[0]
                timeWhileArchive = str(content).split('/')[-1]
                threadTitle = str(content).split('/')[-2]
                reply = BotReplyAction(message)
                thread = BotThreadAction(message)

                if len(str(message.content).split('/')) == 4 or isint(timeWhileArchive):
                    await reply.exec()('{}さん、スレッドを作成しました。\nこのスレッドは後{}日でアーカイブされます。'.format(sendMessageAuthor, timeWhileArchive))
                    await thread.exec()(threadTitle, '{}が[提案]で作成しました'.format(sendMessageAuthor), time=1440*int(timeWhileArchive))
                else:
                    await reply.exec()('スレッド作成規約に反しています。[提案]/thread/スレッド名/日にち(整数型)になります。')
                del reply
                del thread

        if '\example' in str(message.content):
            reply = BotReplyAction(message)
            await reply.exec()('例）\n[報告]\n・アーニャ像完成\n[提案]\n・アーニャトラップ作成どう？\n[要求]\n・丸石100スタックほしい\n\n・スレッド作成方法\n[提案 or 報告 or 要求]/thread/スレッド名/日にち(整数型)になります。')
        del reaction

# ゲームのデータログの保存
playingData = IsPlayingDataBase()
@client.event
async def on_member_update(before, after):

    # ゲーム通知
    if after.activity is not None:
        # ゲームをしていない状態からゲームを開始したときに処理
        if before.activity is None and after.name not in playingData.get_data().keys():
            playingData.start(before, after)
        else:
            # ゲーム１をしている状態からゲーム２を開始したときに処理
            if before.activity.name != after.activity.name:
                playingData.finish(before, after)
                playingData.start(before, after)
    else:
        # ゲームをしている状態からゲームを終了したときに処理
        if after.name in playingData.get_data().keys():
            playingData.finish(before, after)

# Botのトークンを指定（デベロッパーサイトで確認可能）
client.run(env.get_token())