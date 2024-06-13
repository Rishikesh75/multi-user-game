from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font
import threading 
import socket
import pickle
import hi

IP = socket.gethostbyname(socket.gethostname())
port = 1234
print(f"{IP}")
addr = (IP,port)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(addr)
SIZE  = 1024
FORMAT = "utf - 8"

#this is a list for gammer conn 
li_conn= []
li_score = []
team_1 = 0
team_2 = 0

def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        # Flag to optimize the algorithm
        swapped = False

        # Last i elements are already in place, so no need to check them again
        for j in range(0, n-i-1):
            if arr[j][0] > arr[j+1][0]:
                # Swap the elements
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True

        # If no two elements were swapped in the inner loop, the array is already sorted
        if not swapped:
            break
    return(arr)
def handle_clinet_1(conn,i):
    global li_score
    global team_1 
    global team_2 
    
    user_name = conn.recv(SIZE).decode(FORMAT)
    print(f"{user_name} is playing the game.")
    data = pickle.dumps(hi.play_game)  # Serialize the function
    conn.send(data)
    score = conn.recv(SIZE).decode(FORMAT)
    if i%2 ==0:
       team_1 = team_1 + int(score)
    else:
        team_2 = team_2 + int(score)
    t = (score,user_name,conn,i)
    
    li_score.append((t))
    x = True
    while x:
        if len(li_score) == 4:
            sorting_list()
            x = False
        else:
            continue
    print(len(li_score))
    for i in range(len(li_score)-1,-1,-1):
        conn_1 = li_score[i][2]
        msg = len(li_score) - i
        if conn_1 == conn:
            conn_1.send(str(msg).encode())
            if li_score[i][3]%2 ==0 and team_1 > team_2:
                m = 'YOUR Team Has WON'
                conn_1.send(str(m).encode())
            elif li_score[i][3]%2 ==0 and team_1 < team_2:
                m = 'YOUR Team Has LOST'
                conn_1.send(str(m).encode())
            if li_score[i][3]%2 !=0 and team_1 > team_2:
                m = 'YOUR Team Has LOST'
                conn_1.send(str(m).encode())
            elif li_score[i][3]%2 !=0 and team_1 < team_2:
                m = 'YOUR Team Has WON'
                conn_1.send(str(m).encode())

def sorting_list():
    global li_score
       
        
    li_score = bubble_sort(li_score)
    
    
def main():
    global li_score
    x = 0
    while x<4:
        server.listen()
        conn,client_addr  = server.accept()
        
        li_conn.append(conn)
        x = len(li_conn)
    
    
    for i in range(0,x):
        thread = threading.Thread(target=handle_clinet_1, args=(li_conn[i],i))
        thread.start()
        
    
    
if __name__ == "__main__":
    main()