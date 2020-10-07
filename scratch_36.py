
import pygame
from pygame.base import *
#Get filename hostname (portname)

def parser(data):
    words = data.split(" ")
    if(len(words) > 4 or len(words) <3):
        return 'invalid command%'
    elif(len(words) == 4):
        if(words [0] != "GET" and words[0] != "POST"):
            return 'invalid command%'
        elif(words[0] == 'GET' and words[3].isdigit()):
            return "4 words GET%" + words [1] + "%" + words[3]
        elif(words[0] == "POST" and words[3].isdigit()):
            return "4 words POST%" + words[1] + "%" + words[3]
        else:
            return "invalid command%"
    '''else:
        if(words[0] != "GET" and words[0] != "POST"):
            return 'invalid command%'
        if(words[0] == "GET"):
            return "3 words GET%" + words[1]
        else:
            return "3 words POST%" + words[1]'''


from socket import *

def newConnectionRequest(conn, addr):
    command = conn.recv(1024).decode()
    command_type = parser(command)
    command_type = command_type.split("%")
    if(command_type[0] == "invalid command"):
        conn.sendall(b"invalid command")
        conn.close()
        return
    elif(command_type[0] == "4 words GET"):
        file_name = command_type[1]
        port_number = command_type[2]
        msg = ""
        try:
            msg = open(file_name, 'rb').read()
        except IOError:
            msg = "HTTP/1.0 404 Not Found\r\n"

        conn.sendall(b"HTTP/1.0 200 OK\r\n")
        conn.sendall(msg)
        conn.close()
    elif(command_type[0] == "4 words POST"):
        file_name = command_type[1]
        port_number = command_type[2]
        conn.sendall(b"HTTP/1.0 200 OK\r\n")
        data = conn.recv(1024).decode()
        print ('msg recvd')
        conn.close()
    else:
        return "Something went wrong, Please try again later."
    '''elif (command_type[0] == "3 words GET"):
        file_name = command_type[1]
        port_number = '8080'
        msg = ""
        try:
            msg = open(file_name, 'rb').read()
        except IOError:
            msg = "HTTP/1.0 404 Not Found\r\n"
        conn.sendall(b"HTTP/1.0 200 OK\r\n")
        conn.sendall(msg)
        conn.close()
    else:
        command_type[0] == "3 words POST"
        file_name = command_type[1]
        port_number = '8080'
        conn.sendall(b"HTTP/1.0 200 OK\r\n")
        data = conn.recv(1024).decode()
        print('msg recvd')
        conn.close()'''


                                         ######## CLIENT SIDE #######


import socket
from PIL import Image
import io

HOST = '127.10.17.18'
PORT = 8080

#with open('input.txt', 'r') as f:
 #   list_of_requests = f.readlines()
inputfile = open('input.txt', 'r')
for i in inputfile:

#for i in range(0, len(list_of_requests)):

    request = parser(i)
    request = request.split("%")
    request_type = request[0]
    file_extension = request[1].split(".")[1]


    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    if(request_type == "GET"):

        client_socket.sendall(i.encode())
        server_reply = client_socket.recv(17)
        print("ACK: ", server_reply.decode())

        if((server_reply.decode()).split(" ")[1] == "200"):
            data = ""
            while(1):
                stream_of_bytes = client_socket.recv(1024)
                data += stream_of_bytes

            if(file_extension == "txt"):
                file = open(request[1], 'wb')
                file.write(data)
                file.close()
                ++i
                break

            elif(file_extension == "html"):
                file = open(request[1], 'wb')
                file.write(data)
                file.close()
                ++i
                break

            elif(file_extension == "jpg" or file_extension == "jpeg"):
                image = Image.open(io.BytesIO(data))
                image.save(request[1], "JPEG")
                ++i
                break

            else:
                print('Sorry, the file extension of request id ' + i + ' is not supported.')
                ++i
                break
        else:
            ++i
            break

    elif(request_type == "POST"):
        client_socket.sendall(i.encode())
        server_reply = client_socket.recv(17)

        if ((server_reply.decode()).split(" ")[1] == "200"):
            print ("ACK: ", server_reply.decode())
            file = open(request[1], 'rb')
            client_socket.sendall(file)
            print('The file has been sent.')
            ++i
            break
        else:
            ++i
            break

    else:
        client_socket.sendall(i.encode())
        server_reply = client_socket.recv(17)
        ++i
        break

client_socket.close()
print ("run successfully")

