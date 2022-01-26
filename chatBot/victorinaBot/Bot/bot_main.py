import asyncio
import random

import twitchio.ext.commands
from twitchio.ext import commands
from victorinaBot.models import Question, Statistic, Channel, Config
from apscheduler.schedulers.background import BackgroundScheduler
from django.db import models
from asgiref.sync import sync_to_async
import time


class Bot(commands.Bot):
    I = len(Question.objects.all()) - 1
    QUESTION_LIST = []
    QUESTION_LISTv2 = ''
    AUTHOR_NAME = "None"
    J = 0
    TWITCH_TOKEN_API_ENDPOINT = 'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials'
    TWITCH_STREAM_API_ENDPOINT = "https://api.twitch.tv/helix/streams?user_login={}"
    CLIENT_ID='khkolfq5pe4tvbpxucies2ntc6wsyf'
    SECRET_ID='elx4sxh13eyc6ohtnqj7tyi7vvp3ch'
    TOKEN = "5ae843v501khzqctopflmujri5p096"
    NAME = "victorina_BoT"
    CHANNEL = ['karachlen', 'victorina_bot']
    #for item in Channel.objects.all():
     #   CHANNEL.append(item.channel_name)

    def __init__(self):
        super().__init__(token=self.TOKEN, prefix='!', initial_channels=self.CHANNEL)

    async def event_ready(self):
        print(f'Logged in as | {self.nick} | {self.connected_channels}')
        await self.get_list()
        planTime = BackgroundScheduler(timezone="Europe/Moscow")
        if self.J == 0:
            planTime.add_job(self.send_question, 'interval', minutes=30)
        planTime.start()

    @sync_to_async()
    def get_list(self):
        for i in Question.objects.all():
            self.QUESTION_LIST.append(str(i))
        random.shuffle(self.QUESTION_LIST)

    async def event_message(self, message):
        if message.echo:
            return
        if str(message.content) == self.modernAnswer() or message.content.lower() == self.modernAnswer():
            if self.J == 0:
                self.AUTHOR_NAME = message.author.name
                self.J += 1
            await self.saveModel(message.channel.name, self.AUTHOR_NAME, self.J)
        await self.handle_commands(message)


    @sync_to_async()
    def saveModel(self,channel, nameAuthor, j):
        statistic = Statistic(channel_name=channel, winner=nameAuthor, wins=j)
        sync_to_async(statistic.save())

    def modernQuestion(self):
        index = self.QUESTION_LIST[self.I].find('вопрос=') + 7
        index2 = self.QUESTION_LIST[self.I].find(',')
        question = self.QUESTION_LIST[self.I][index:index2]
        return question

    def modernAnswer(self):
        index = self.QUESTION_LISTv2.find('ответ=') + 6
        index2 = self.QUESTION_LISTv2.find(')')
        question = self.QUESTION_LISTv2[index:index2]
        return question


    def send_question(self):
        try:
            i=0
            while True:
                if i==len(self.CHANNEL):
                    break
                else:
                    chan = self.get_channel(self.CHANNEL[i])
                    asyncio.run(chan.send(content="❓ Проверь свои знания ❓" + str(self.modernQuestion())))
                    i+=1
                    time.sleep(1)
            self.QUESTION_LISTv2 = self.QUESTION_LIST[self.I]
            self.QUESTION_LIST.remove(self.QUESTION_LIST[self.I])
            self.I -= 1
            self.QUESTION_LIST = self.question_none(self.QUESTION_LIST)
        except:
            if ValueError:
                print("В базе нет вопросов")

    def question_none(self, questions_new):
        if len(questions_new) == 0:
            for i in Question.objects.all():
                self.QUESTION_LIST.append(str(i))
                random.shuffle(self.QUESTION_LIST)
            self.I = len(questions_new) - 1
        return questions_new

    @commands.command()
    async def в(self, ctx: commands.Context):
        await ctx.send(
            f'Кол-во вопросов: {QuestionWork.count}, каждый вопрос после запуска стрима высылается через 10 мин, последующие рез 30 мин, если никто не ответил правильно, то через 15 мин.')

class QuestionWork(models.Manager):
    list = []
    count = 0
    for list in Question.objects.all():
        count += 1
