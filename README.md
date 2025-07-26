# 🤖 The TALOS Framework
## 💬 ChatOps made easy

### 📖 About

With **TalosBot**, you can build operational bots without struggling with chat APIs or artificial intelligence.  
Just focus on your **skills** —simple Python functions that return the message to send back.

The framework is designed to be:
- 🧩 Easy to use
- 🔧 Fully extensible
- 🚀 Production-ready

### 🧱 Components

A bot in Talos is composed of **three main components**:

- **Channel**: Handles messaging through a communication platform.
- **Matcher**: Matches an input sentence to an example sentence tied to a skill.
- **Parser** *(optional)*: Extracts parameters from user input and passes them to the skill without needing to manually parse anything.

### 🧠 Built-in Models

Talos runs locally —no data is sent to third parties.  
Out-of-the-box models include:

- **`BertMatcher`**: Uses `sentence-transformers` to perform cosine similarity.
- **`NERParser`**: Uses a spaCy pipeline with NER via the default `en_core_web_lg` model. You can replace it with a custom one using the CLI trainer (explained below).

### 🌐 Built-in Channels

Talos supports several channels, so you don’t have to deal with chat platform intricacies:

- **Slack**:  
  Uses `slack-bolt` with slash commands and no public endpoint required.  
  Simply:
  - Create a new Slack App
  - Add the `chat:write` OAuth scope
  - Enable **Socket Mode**
  - Register a slash command (default: `/talos`)  
  You’ll receive the **app token** and **bot token**, both required for the connection.

- **Telegram**:  
  Create a bot via Telegram’s [@BotFather](https://core.telegram.org/bots#6-botfather), and get your bot token.  
  Plug it into Talos and you're ready to go.

### 🔄 Workflow Overview

1. A user sends a sentence via a supported channel (e.g., a Telegram group).
2. The bot matches the sentence against all registered examples.
3. If a parser is configured, parameters are extracted into a dictionary.
4. The matching skill is executed and the return message is sent back through the channel.

### ⚡ Quickstart

Install Talos with pip:

```bash
pip install talosbot
```

Then create a simple bot in `bot.py`:

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

This launches a CLI channel for quick local testing.  
For the NER parser, you’ll need a trained model to detect your entities.  
You can download a pre-trained one [here](https://github.com/sergiopr89/talosbot-models).

---

### 🧪 Training a New NER Model

Train from a dataset:
```bash
talos trainer --trainingset data.json --output ner_model
```

Train from a specific spaCy model:
```bash
talos trainer --trainingset data.json --output ner_model/ --model en_core_web_lg
```

You’ll find `data.json` examples in the [pretrained models repo](https://github.com/sergiopr89/talosbot-models).

---

### 📁 More Examples

Explore the [examples](examples/) directory in this repo to see how to use Talos in different setups and contexts.
