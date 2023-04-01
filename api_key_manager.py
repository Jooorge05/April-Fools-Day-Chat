import os
import openai
from flask import Flask, request, jsonify
import secrets
import json


def generate_api_key(length=32):
    return secrets.token_hex(length)


class APIKeyManager:
    def __init__(self, key_file='api_keys.json'):
        self.key_file = key_file
        try:
            with open(self.key_file, 'r') as f:
                self.api_keys = json.load(f)
        except FileNotFoundError:
            self.api_keys = {}
    
    def save_keys(self):
        with open(self.key_file, 'w') as f:
            json.dump(self.api_keys, f)
    
    def issue_key(self, user):
        new_key = generate_api_key()
        self.api_keys[new_key] = user
        self.save_keys()
        return new_key

    def is_valid_key(self, key):
        return key in self.api_keys