import socket
from threading import Thread
import sys

# import time # used for multithread testing

def handle_client(client):
            
            data = client.recv(1024).decode()
            request = data.split("\r\n")
            path = request[0].split(" ")[1]

            if path == "/":
                response = "HTTP/1.1 200 OK\r\n\r\n".encode()
            elif path.startswith("/echo"):
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}".encode()
            elif path.startswith("/user-agent"):
                user_agent = request[3].split(": ")[1]
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
            elif path.startswith("/files"):
                directory = sys.argv[2]
                filename = path[7:]
                if (request[0].startswith("GET")):
                    try:
                        with open(f"{directory}/{filename}", "r") as file:
                            body = file.read()
                        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
                    except Exception as e:
                        response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
                elif (request[0].startswith("POST")):
                    try:
                        with open(f"{directory}/{filename}", "w+") as file:
                            file.write(request[len(request) - 1])
                        response = f"HTTP/1.1 201 Created\r\n\r\n".encode()
                    except Exception as e:
                        response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
            
            client.send(response)
            print("Response Sent: ", response)
            client.close()
            print("Request Handled.")

def main():
    server_socket = socket.create_server(("localhost", 4221))
    threads = []
    try:
        print("Server is running on port 4221...")
        while True:
            client, addr = server_socket.accept()
            thread = Thread(target=handle_client, args=[client])
            threads.append(thread)
            thread.start()

    except KeyboardInterrupt:
        print("\nServer is shutting down.")
    finally:
        server_socket.close()
        print("Server has been shut down.")

if __name__ == "__main__":
    main()

# **************************************************
# * Commands for testing throughout various stages *
# * & example responses from the server.           *
# **************************************************

# Respond with 200 
    # curl -v http://localhost:4221
        # = HTTP/1.1 200 OK\r\n\r\n

# Extract URL path
    # curl -v http://localhost:4221/abcdefg 
        # = HTTP/1.1 404 Not Found\r\n\r\n

# Respond with body
    # curl -v http://localhost:4221/echo/abc
        # = HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\nabc

# Read header
    # curl -v --header "User-Agent: foobar/1.2.3" http://localhost:4221/user-agent 
        # = HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\nfoobar/1.2.3

# Concurrent connections
    # ran multiple command prompts to act as different clients accessing server at once. 
        # 'time.sleep(7)' used for multithread testing, inserted before line 44 'client.close()'

# Return a file
    # curl -i http://localhost:4221/files/hello.txt 
        # HTTP/1.1 200 OK
        # Content-Type: application/octet-stream
        # Content-Length: 4
        #
        # heyo
    # curl -i http://localhost:4221/files/index.html
        # HTTP/1.1 200 OK
        # Content-Type: application/octet-stream
        # Content-Length: 143
        #
        # <!DOCTYPE html>
        # <html>
        # <head>
        # <title>Page Title</title>
        # </head>
        # <body>
        #
        # <h1>This is a Heading</h1>
        # <p>This is a paragraph.</p>
        #
        # </body>
        # </html>
    # curl -i http://localhost:4221/files/non_existant_file
        # HTTP/1.1 404 Not Found\r\n\r\n

# Read request body
# used mode 'w+' to create file if it doesn't exist and open it in write mode
    # curl -vvv -d "hello world" localhost:4221/files/readme.txt
        # Response Sent:  b'HTTP/1.1 201 Created\r\n\r\n'
        # Request Handled.