import threading
import queue
import requests

# Function to check server availability and fetch available models
def check_server_and_get_info(q, results):
    while not q.empty():
        server_url = q.get()
        try:
            # Check if the server is available
            response = requests.get(f"{server_url}/v1/models", timeout=5)
            response2 = requests.get(f"{server_url}/api/version", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                version = response2.json()["version"]
                results[server_url] = f"Available - Version {version} - Models: {', '.join(models) if models else 'No models found'}"
            else:
                results[server_url] = f"Unavailable (Status Code: {response.status_code})"
        except Exception as e:
            results[server_url] = f"Error: {str(e)}"
        finally:
            q.task_done()

# Main function
def main():
    # File containing the server list (one URL or IP per line)
    file_path = "servers.txt"

    # Load server list from file
    with open(file_path, 'r') as file:
        servers = [line.strip() for line in file if line.strip()]

    # Create a queue and populate it with server URLs
    q = queue.Queue()
    for server in servers:
        q.put(server)

    # Dictionary to store the results
    results = {}

    # Number of threads to use
    num_threads = 5

    # Create and start threads
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=check_server_and_get_info, args=(q, results))
        t.start()
        threads.append(t)

    # Wait for all tasks in the queue to be processed
    q.join()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Print the results
    print("Server Status:")
    for server, status in results.items():
        print(f"- {server}: {status}")

if __name__ == "__main__":
    main()

