import socket
import os
from _thread import *
import logging
import queue
from encryption import Encryption

cipher_tool = Encryption()
cipher_tool.create_keys()
task_bucket = queue.PriorityQueue(20)
logging.basicConfig(filename="server.log" ,filemode='w',level=logging.DEBUG,format='%(asctime)s - %(message)s')



socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8080
priority_count = 0

try:
    socket_server.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
socket_server.listen(5)

def Worker():
    while True:
        if not task_bucket.empty():
            task = task_bucket.get()
            try:
                os.system(task.data)
                task.connection.send(cipher_tool.encrypt_message("ACK"))
                logging.debug("{} ACK".format(task.priority))
                print("task completed")
            except:
                task.connection.send(cipher_tool.encrypt_message("NOACK"))
                logging.debug("{} NOACK".format(task.priority))
            finally:
                task.connection.close()
                logging.debug('Disconnected from: ' + task.address[0] + ':' + str(task.address[1]))

class TaskCommand:
    def __init__(self,priority,data,connection,address):
        self.priority = priority
        self.data = data
        self.connection = connection
        self.address = address

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)




def Client(connection,address):
    global priority_count
    while True:
        try:    
            data = connection.recv(2048)
            if not data:
                break
            user_message = cipher_tool.decrypt_message(data)

            logging.debug('Decrypting Message from: ' + address[0] + ':' + str(address[1]))
            if user_message.startswith("cmd"):
                __,command = user_message.split("cmd")
                priority_count+=1
                print("Queuing data.......")
                task_bucket.put(TaskCommand(priority_count,command,connection,address))
                logging.debug("{} Queuing data".format(address[0]))
            else:
                connection.send(cipher_tool.encrypt_message("You send Text Message"))
                logging.debug('Encrypting Message and Sending Message for : ' + address[0] + ':' + str(address[1]))
                logging.debug('Disconnected from: ' + address[0] + ':' + str(address[1]))
                connection.close()
                break
        except:
            pass
        
start_new_thread(Worker,())
while True:
    conn, address = socket_server.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    logging.debug('Connected to: ' + address[0] + ':' + str(address[1]))
    try:
        start_new_thread(Client, (conn,address,  ))
    
    except:
        pass
socket_server.close()
