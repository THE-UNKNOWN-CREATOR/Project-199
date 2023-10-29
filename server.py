import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
print("server is running")

questions = [
    "Who claimed that humans evolved from apes? \na. Charles Darwin     b. Albert Einstein      c. Doc Brown        d.Stephen Hawking",
    "Who stated that, in a triangle, the hypotenuse squared is equal to the sum of the squares of the other two sides? \na. Euclid      b.Einstein      c.Pythogarus        d.Thames",
    "Who invented the telephone? \na. Nikola Tesla     b. J.L. Baird     c. Moriarty     d. A.G. Bell",
    ]

answers = ['a', 'c', 'd']

def clientthread(conn):
    conn.send("Welcome to the quiz game".encode('utf-8'))
    score = 0
    conn.send("You will recieve a question answer with a, b, c or d\n".encode('utf-8'))
    conn.send("Good Luck\n\n".encode('utf-8'))

    q, an = get_random_q_a(conn)

    while True:
        try:
            messg = conn.recv(2048).decode('utf-8')
            if messg:
                if messg != 'a' and messg != 'b' and messg != 'c' and messg != 'd':
                    remove(conn)
                else:
                    if(messg == an):
                        score += 1
                        conn.send(f"Correct Answer, Your score is now {score}")
                        remove_q_a(q, an)
                        get_random_q_a(conn)
                    else:
                        conn.send(f"Incorrect Answer, Your score is still {score}")
                        remove_q_a(q, an)
                        q, an = get_random_q_a(conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(messg, conn):
    for client in list_of_clients:
        if client != conn:
            try:
                client.send(messg.encode('utf-8'))
            except:
                remove(client)

def get_random_q_a(conn):
    r_index = random.randint(0, len(questions)-1)
    c_q = questions[r_index]
    c_a = answers[r_index]
    
    conn.send(c_q.encode('utf-8'))

    return c_q, c_a

def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)


def remove_q_a(q, a):
    if q in questions and a in answers:
        questions.remove(q)
        answers.remove(a)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    new_thread = Thread(target = clientthread, args=(conn))
    new_thread.start()