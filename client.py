import socket

def main():
    host = '127.0.0.1'
    port = 12363
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port)) 

    # message you send to server
    message = "hello message"
    s.send(message.encode('ascii'))

    while True:
        # message received from server
        data = s.recv(1024)

        # print the received message
        print('Received from the server :',str(data.decode('ascii')))

        # ask the client whether he wants to continue
        ans = input('\nEnter some command or type help: ')
        if ans=='quit':
            s.send(ans.encode('ascii'))
            break
        else:
            s.send(ans.encode('ascii'))

    # close the connection
    s.close()

if __name__ == '__main__':
    main()