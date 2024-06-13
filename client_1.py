from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font
import threading 
import socket
import pickle
import tkinter as tk
port = 1234
IP = '192.168.56.1'
addr = (IP, port)
SIZE = 1024
FORMAT = "utf-8"


global score, egg_speed, egg_interval
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)
    msg_1 = input("Enter the user name:")
    client.send(msg_1.encode(FORMAT))
    data = client.recv(1024)
    received_game_data = pickle.loads(data)
    
    
    
    score = received_game_data()
    print(f"Game Score: {score}")
    client.send(str(score).encode(FORMAT))
    msg =client.recv(SIZE).decode(FORMAT)
    print(f"{msg_1} has secured place {msg}")
    msg =client.recv(SIZE).decode(FORMAT)
    print(f"{msg}")
    
if __name__ == "__main__":
    main()

