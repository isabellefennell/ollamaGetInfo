# Multi-threaded Server Status Checker

This Python script concurrently checks the availability and model information of multiple servers. It utilizes multi-threading to improve efficiency, making it particularly suitable for scenarios where a large number of servers need to be checked.

## Key Features

- Reads server list from a file
- Concurrently checks the status of each server
- Retrieves version and model information for available servers
- Outputs a status summary for each server

## Dependencies

- Python 3.x
- `requests` library

## Usage

1. Prepare a file named `servers.txt` with one server URL or IP address per line.
2. Run the script:
   ```
   python main.py
   ```

## Code Structure

### Main Functions

#### `check_server_and_get_info(q, results)`

This function is responsible for checking the status and information of a single server. It retrieves server URLs from the queue and sends HTTP requests to check availability and fetch information.

#### `main()`

The main function controls the overall flow of the program:
1. Reads the server list
2. Creates a thread pool
3. Initiates the checking process
4. Collects and prints results

### Key Code Segment

```python
# Create and start threads
threads = []
for _ in range(num_threads):
    t = threading.Thread(target=check_server_and_get_info, args=(q, results))
    t.start()
    threads.append(t)

# Wait for all tasks to complete
q.join()

# Wait for all threads to finish
for t in threads:
    t.join()
```

This code segment creates multiple threads to process server checking tasks concurrently, improving efficiency.

## Notes

- Ensure the `servers.txt` file is correctly formatted with one server address per line.
- The number of concurrent threads can be adjusted by modifying the `num_threads` variable.
- The script uses a 5-second timeout, which can be adjusted as needed.

## Sample Output

```
Server Status:
- http://server1.example.com: Available - Version 1.0 - Models: model1, model2
- http://server2.example.com: Unavailable (Status Code: 404)
- http://server3.example.com: Error: Connection timed out
```

This script provides a simple yet effective method for monitoring the status of multiple servers, suitable for scenarios requiring regular checks of server health.
