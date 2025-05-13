from os import getenv
from talosbot.matchers.bert import BertMatcher
from talosbot.parsers.ner import NERParser
from talosbot.channels.telegram import TelegramChannel
from talosbot.talos import Bot

channel = TelegramChannel(getenv('TELEGRAM_TOKEN'))
matcher = BertMatcher(acceptance_threshold=0.6)
parser = NERParser(getenv('MODEL_PATH', './ner_model'))

bot = Bot(matcher=matcher, parser=parser, channel=channel)

@bot.match('Execute the job XXX in the project some/repository', ('PROJECT', 'JOB'))
def check_pipeline(JOB, PROJECT):
    return f"Checking pipeline {JOB} for project {PROJECT}..."

@bot.default_match()
def no_skill():
    return 'No skill, my bad!'


if __name__ == '__main__':
    bot.run()
