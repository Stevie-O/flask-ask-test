import logging
import yaml
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import re
import sonysend
import sys

verb_map = {
    'turn on': 'turn_on',
    'power on': 'turn_on',
    'turn off': 'turn_off',
    'power off': 'power_off',
    'mute': 'mute',
}

noun_map = {
    'tv': 'tv',
    'television': 'tv',
}

def make_sony_command(name, code):
    def _function():
        passwds = load_passwords()
        host = passwds['itach']['FR'];
        sonysend.call_sony(host, code)
    _function.__name__ = name
    return _function

device_commands = {
    'tv': {
            'turn_on': make_sony_command('tv_on', '1-46'),
            'turn_off': make_sony_command('tv_off', '1-47'),
            'mute': make_sony_command('tv_mute', '1-20'),
        }
}

def load_passwords():
    with open('passwords.yaml', 'r') as f:
        return yaml.load(f)

def HomeControl(app, path):
    ask = Ask(app, path)

    logging.getLogger("flask_ask").setLevel(logging.DEBUG)

    @ask.launch
    def new_game():

        welcome_msg = 'What do you want tars to do?'

        return question(welcome_msg)

    @ask.intent("ControlIntent")

    def control(verb, noun):
        
        try:
            device_name = noun_map[noun.lower()]
            device_command = verb_map[verb.lower()]
            
            device_commands[device_name][device_command]()
            
            return statement('OK')
        
        except:
            logging.getLogger("flask_ask").exception('Error in ControlIntent:')
            return statement("I'm sorry Dave, I can't let you do that")

