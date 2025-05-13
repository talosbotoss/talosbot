import logging
from os import getenv
from talosbot.logs import LoggingBuilder, DEFAULT_LOGGING_LEVEL

# Generate and make available a logger at the init of this module
log_level = getattr(logging, getenv('TALOS_LOG_LEVEL', '').upper(), DEFAULT_LOGGING_LEVEL)
logger = LoggingBuilder(level=log_level, log_file=getenv('TALOS_LOG_FILE')).get_logger('TALOS')
