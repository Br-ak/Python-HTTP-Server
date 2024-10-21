
# *********************************
# * PREVIOUS ATTEMPTS AND METHODS *
# *********************************


# import socket
# from threading import Thread


# def main():
#     server_socket = socket.create_server(("localhost", 4221))
#     threads = []

#     try:
#         while True:
#             connection, address = server_socket.accept()  # wait for client
#             thread = Thread(target=handle_client, args=[connection])
#             threads.append(thread)
#             thread.run()
#     except KeyboardInterrupt:
#         print("\nServer is shutting down.")
#     finally:
#         server_socket.close()
#         print("Server has been shut down.")

# def handle_client(connection):
#     byte = []
#     try:
#         while (byte := connection.recv(1024)) != b"":
#             parsed_req = parse_request(byte)
#             if parsed_req == None:
#                 connection.send(str.encode("HTTP/1.1 500 No\r\n\r\n"))
#                 return connection.close()
#             else:
#                 # Recv & parsed request sucessfully
#                 connection.send(handle_request(connection, parsed_req))
#                 return connection.close()
#     except Exception as e:
#         print("handle_client error", e)        

# def parse_request(bytes):
#     output = {"method": "", "path": "", "headers": {}, "body": "",}
#     lines = bytes.decode("utf-8").split("\r\n")

#     if len(lines) < 3:
#         return None
#     reqLine = lines[0].split(" ")
#     if (not reqLine[0]) or reqLine[0] not in ["GET", "POST", "PUT", "HEAD"]:
#         return None
#     if (not reqLine[1]) or reqLine[1] != "/":
#         return None

#     output["method"] = reqLine[0]
#     output["path"] = reqLine[1]

#     # Ignore HTTP version
#     lines = lines[1:]
#     c = 0
#     for l in lines:
#         if l == "":
#             break
#         headLine = l.split(":")
#         output["headers"][headLine[0]] = headLine[1].lstrip()
#         c += 1
#     output["body"] = lines[c + 1]

#     return output

# def handle_request(connection, request):
#     if request["path"] == "/":

#         return reply(request, 200)
#     if request["path"].startswith("/echo/"):
#         return reply(request, 200, request["path"][6:])
#     if request["path"] == "/user-agent":
#         ua = request["headers"]["User-Agent"]
#         return reply(request, 200, ua)
#     return reply(request, 404)

# def reply(request, code, body="", headers={}):
#     b_reply = b""
#     match code:
#         case 200:
#             b_reply += b"HTTP/1.1 200 OK\r\n"
#         case 404:
#             b_reply += b"HTTP/1.1 404 Not Found\r\n"
#         case 500:
#             b_reply += b"HTTP/1.1 500 No\r\n"
#     if not "Content-Type" in headers:
#         headers["Content-Type"] = "text/plain"
#     if body != "":
#         headers["Content-Length"] = str(len(body))
#     for key, val in headers.items():
#         b_reply += bytes(key, "utf-8") + b": " + bytes(val, "utf-8") + b"\r\n"
#     b_reply += b"\r\n" + bytes(body, "utf-8")
    
#     return b_reply


# if __name__ == "__main__":
#     main()
















# import socket  # noqa: F401
# # cd OneDrive/Desktop/"GitHub Projects"/Portfolio/codecrafters-http-server-python/app
# # curl --verbose 127.0.0.1:4221/echo/abc

# # curl --verbose 127.0.0.1:4221/user-agent/foobar/1.2.3
# # curl -v --header "User-Agent: foobar/1.2.3" http://localhost:4221/user-agent

# def parse_request(request_data):
#     lines = request_data.split('\r\n')
#     start_line = lines[0]  # first line of the request
#     method, path, version = start_line.split(' ') # separate data
#     return method, path, version

# def generate_echo_response(path_segment):
#     body = path_segment # segment to be echoed back
#     headers = [
#         "HTTP/1.1 200 OK",
#         "Content-Type: text/plain",
#         f"Content-Length: {len(body)}",
#         "", # extra newline to end header section
#         body
#     ]

#     return "\r\n".join(headers)

# def generate_userAgent_response(path_segment):
#     body = path_segment # segment to be echoed back
#     headers = [
#         "HTTP/1.1 200 OK",
#         "Content-Type: text/plain",
#         f"Content-Length: {len(body)}",
#         "", # extra newline to end header section
#         body
#     ]

#     return "\r\n".join(headers)

# def handle_request(client_socket):
#     # Read data from the client
#     request_data = client_socket.recv(1024).decode()
#     method, path, version = parse_request(request_data)
#     print("*********request_data: ", request_data)
    
#     if path == '/':
#         # Root path response
#         response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"
#     elif path.startswith("/echo/"):
#         path_segment = path.split("/echo/")[1]
#         response = generate_echo_response(path_segment)
#     elif path == ("/user-agent"):
#         print("*********/user-agent*********")
#         path_segment = path.split("/user-agent")[1]
#         print("path_segment: ", path_segment)
#         response = generate_userAgent_response(path_segment)

#     else:
#         # Default 404 Not Found response for unrecognized paths
#         response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nPage not found."

#     client_socket.send(response.encode())

# def main():
#     # Create TCP/IP socket
#     server_socket = socket.create_server(("localhost", 4221))
#     print("Server is running on port 4221...")

#     try:
#         while True:
#             # Wait for connection
#             print("Waiting for connection...")
#             client_socket, addr = server_socket.accept()
#             print(f"Connection from {addr} has been established")

#             # Handle client's request
#             handle_request(client_socket)
#             client_socket.close()
#     except KeyboardInterrupt:
#         print("\nServer is shutting down.")
#     finally:
#         server_socket.close()
#         print("Server has been shut down.")


# if __name__ == "__main__":
#     main()
    