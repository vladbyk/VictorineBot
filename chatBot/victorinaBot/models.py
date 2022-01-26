from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=400, null=True)
    answer = models.CharField(max_length=100)

    def __str__(self) -> str:
        return 'Вопрос (вопрос=' + str(self.question_text) + ', ответ=' + self.answer + ')'

class Channel(models.Model):
    channel_name = models.CharField(max_length=400)

    def __str__(self) -> str:
        return 'Канал (название=' + self.channel_name + ')'


class ChannelQuestion(models.Model):
    channel_name = models.CharField(max_length=400)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date_asked = models.DateTimeField()
    date_answered = models.DateTimeField(null=True)
    winner = models.CharField(max_length=400, null=True)

    def __str__(self) -> str:
        return 'Вопрос Канала (канал=' + self.channel_name + ', вопрос=' + self.question.question_text + ')'

class Config(models.Model):
    client_id = models.CharField(max_length=250,null=True)
    token = models.CharField(max_length=250,null=True)
    client_secret = models.CharField(max_length=250,null=True)

    def __str__(self) -> str:
        return 'Настройка: ' + self.token


class Statistic(models.Model):
    channel_name = models.CharField(max_length=400)
    winner = models.CharField(max_length=400)
    wins = models.IntegerField(default=0)

    def __str__(self) -> str:
        return 'Канал: ' + self.channel_name + '. Победитель: ' + self.winner + ' - ' + str(self.wins) + ' побед(-ы)'