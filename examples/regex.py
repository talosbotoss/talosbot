from talosbot.matchers.regex import RegexMatcher
from talosbot.parsers.regex import RegexParser
from talosbot.channels.cli import CLIChannel
from talosbot.talos import Bot

channel = CLIChannel()
matcher = RegexMatcher()
parser = RegexParser()

bot = Bot(matcher=matcher, parser=parser, channel=channel)

@bot.match('Execute the job ([a-zA-Z0-9_]+) in the project some/repository', {'PROJECT':'.*project ([a-zA-Z/]+).*', 'JOB':'.*job ([a-zA-Z0-9_]+).*'})
def check_pipeline(JOB, PROJECT):
    return f"Checking pipeline {JOB} for project {PROJECT}..."


if __name__ == '__main__':
    bot.run()
