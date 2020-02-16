from api.players import create_player
import sys
import getpass
import os

print('Username:', flush=True)
username = sys.stdin.readline().rstrip()
print('password:', flush=True)
password = sys.stdin.readline().rstrip()

create_player(username, password)