import discord

from interfaces import Actions

class BotActivityStatusAction(Actions):
    
    def __init__(self, client):
        super().__init__(client)

    def development(self):
        print('Bot Ready in Development')
        return self.client.change_presence(activity=discord.Game(name=f"開発環境での実行"))

    def test(self, ):
        print('Bot Ready in Test')
        return self.client.change_presence(activity=discord.Game(name=f"テスト環境での実行"))

    def production(self):
        print('Bot Ready')
        return self.client.change_presence(activity=discord.Game(name=f"がんばるます"))

class BotSendAction(Actions):

    def __init__(self, client,):
        super().__init__(client)

    def development(self, message):
        print('Development:{}'.format(message))
        return self.client.send('Development:{}'.format(message))

    def test(self, message):
        print('Test:{}'.format(message))
        return self.client.send('Test:{}'.format(message))

    def production(self, message):
        print(message)
        return self.client.send(message)

class BotReplyAction(Actions):
    def __init__(self, client):
        super().__init__(client)

    def development(self, message):
        print('Development:{}'.format(message))
        return self.client.reply(message)
    
    def test(self, message):
        print('Test:{}'.format(message))
        return self.client.reply(message)

    def production(self, message):
        print('{}'.format(message))
        return self.client.reply(message)

class BotReactionAction(Actions):
    def __init__(self, client):
        super().__init__(client)

    def development(self, emoji):
        print('Development:{}'.format(emoji))
        return self.client.add_reaction(emoji)
    
    def test(self, emoji):
        print('Test:{}'.format(emoji))
        return self.client.add_reaction(emoji) 

    def production(self, emoji):
        print('{}'.format(emoji))
        return self.client.add_reaction(emoji) 

class BotThreadAction(Actions):
    def __init__(self, client):
        super().__init__(client)

    def development(self, name, reason, time=1440):
        print('Development:{}, {}, {}'.format(name, reason, time))
        #return self.client.create_thread(name, auto_archive_duration=time, reason=reason)
        return self.client.create_thread(name=name, auto_archive_duration=time, reason=reason)
    
    def test(self, name, reason, time=1440):
        print('Development:{}, {}, {}'.format(name, reason, time))
        return self.client.create_thread(name=name, auto_archive_duration=time, reason=reason)

    def production(self, name, reason, time=1440):
        print('Development:{}, {}, {}'.format(name, reason, time))
        return self.client.create_thread(name=name, auto_archive_duration=time, reason=reason)