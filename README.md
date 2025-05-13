# The TALOS framework
## ChatOps made easy

### About
With talosbot, you will be able to build operational bots without having to struggle with chat APIS or artifical intelligence, just focus in your tasks, aka skills, that are just functions with a return with the message that will be sent back.  
The framework has been implemented to be easy to use and extend any components if you need some custom experience.

### Components
A bot is made of 3 main independent components:

#### Channel
Deals with the messaging through a specific communication channel.

#### Matcher
Matches a received sentence to an similar example sentence associated to the skill.

#### Parser
The only optional component, will extract what are considered parameters inside a user sentence and make them available to the skill function without having to struggle parsing the sentence by yourself in the skill.

### Built-in models
You have available a built in model that is executed locally so no info is sent to third parties.
#### Matcher model
BertMatcher: It uses sentence-transformers library to perform a cosine similarity.
#### NER Parser
NERParser: It uses a Spacy pipeline with the NER component with a default `en_core_web_lg` downloaded model that you can change by another one when executing a training task with the talos cli (read below for more info).

### Workflow overview
1. A user calls the bot with a sentence in some communication channel, like a telegram group
1. The bot instance receives this sentence and performs the matching operation against all the available sentences
1. If a parser is configured, will extract all the parameters from the sentence and they will be available in a dictionary
1. The skill is executed and a message is sent back with the contents of the return in the skill.

### Quickstart
Install the framework with your favorite virtualenv manager, the install command is:
```bash
pip install talosbot
```
Then create a `bot.py` file with for example:
```python
from talosbot.matchers.bert import BertMatcher
from talosbot.parsers.ner import NERParser
from talosbot.channels.cli import CLIChannel
from talosbot.talos import Bot

channel = CLIChannel()
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

```
This will start a dummy CLI communication interactive channel so you can test it, notice that for the NER parser, you will need to load a pretrained model to identify your own entities. You can download a pretrained model [here](https://github.com/sergiopr89/talosbot-models).  
If you want to train a new NER model, you can use the `talos` cli with your own dataset with:
```bash
talos trainer --trainingset data.json --output ner_model
```
Or train from a specific Spacy model
```bash
talos trainer --trainingset data.json --output ner_model/ --model en_core_web_lg
```
In the [pretrained models repository](https://github.com/sergiopr89/talosbot-models) you will find some data.json examples with the expected format.  
For more examples, take a look at the [examples](examples/) directory on this project.
