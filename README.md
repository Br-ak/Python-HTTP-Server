# Python-HTTP-Server

A lightweight HTTP server built with Python that can handle basic HTTP requests, read request bodies, echo them back, manage multiple concurrent connections, and read/write files.

## Features

- **Handles Basic HTTP Requests**: Supports GET and POST requests.
- **Echo Request Bodies**: Automatically echoes back the body of requests.
- **Header Interpretation**: Reads and interprets HTTP headers.
- **Concurrent Connections**: Manages multiple simultaneous connections using threading.
- **File Read/Write**: Ability to read and write files from the server.

### Making Requests

You can test the server using tools like `curl` or Postman.

#### Example GET Request:

```bash
curl -v http://localhost:4221
```
```bash
curl -v http://localhost:4221/echo/abc
```

### Reading/Writing Files

You can use the server to serve static files. Place your files in the `files` directory, which will be accessible via the server.

Example read request
```bash
curl -i http://localhost:4221/files/hello.txt
```
Example write request
```bash
curl -vvv -d "hello world" localhost:4221/files/readme.txt
```
At the bottom of the file, you can find additional testing commands and their responses to check the server is working as intended. 
## Code Structure

- `main.py`: Main server code that handles requests and manages connections.
- `/files`: Directory for storing files for testing.
- `unused attempts.py`: Older code from previous attempts and methods of creating the server.
