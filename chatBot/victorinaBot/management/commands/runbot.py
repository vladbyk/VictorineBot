from django.core.management.base import BaseCommand
from victorinaBot.Bot.bot_main import Bot


class Command(BaseCommand):
    help = 'Starts the bot'

    def handle(self, *args, **options):
        bot = Bot()
        bot.run()