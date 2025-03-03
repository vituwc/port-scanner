Here’s a README for your Python port scanner:

---

# Python Port Scanner

This is a simple, multi-threaded TCP and UDP port scanner written in Python. It is designed to check the availability of open ports on a remote host and retrieve service banners for TCP services.

## Features

- **TCP Port Scanning**: Scans a given range of ports for open TCP services and attempts to retrieve their banners.
- **UDP Port Scanning**: Scans a given range of ports for open UDP services.
- **Concurrent Scanning**: Uses Python's `ThreadPoolExecutor` for efficient parallel scanning of ports.
- **Banner Grabbing**: Attempts to grab banners from open TCP ports to identify the services running on them.
- **Cross-Platform**: Works on both Linux and Windows.
- **Host Availability Check**: Verifies if the target host is reachable before performing the port scan.

## Requirements

- Python 3.x
- No additional libraries are required beyond Python's standard library.

## Usage

1. Clone or download the repository.
2. Run the script in your terminal or command prompt.

   ```bash
   python port_scanner.py
   ```

3. Follow the prompts to enter the IP address (or hostname) of the target host and the port range you wish to scan.
4. The scanner will check the availability of the specified ports and display the results, including banners for TCP services, if available.

## Example Output

```
Enter the address IP or host domain: example.com
Enter the start port range: 1
Enter the end of port range: 1024

Starting Scan at 2025-03-02 15:00:00
Scan report for example.com
Host is up (50.123 ms latency).
Scanning 1-1024 ports...
Scan finished: 1 IP Address (example.com) scanned in 4.35 seconds.

TCP Ports open:
[+] Port 22: OpenSSH 7.9p1 Debian 10+deb10u2
[+] Port 80: Apache httpd 2.4.38 (Debian)

UDP Ports open:
[+] Port 53 is open!
```

## How it Works

- **TCP Port Scan**: The script attempts to establish a TCP connection with each port in the specified range. If successful, it marks the port as open and attempts to retrieve the service banner.
- **UDP Port Scan**: The script sends a small packet to each UDP port and waits for a response. If a response is received, the port is considered open.

The scanning is done using multiple threads for better performance, especially for large port ranges.

## Sources

This project is based on tutorials and concepts from the following resources:

- [How to build a Python port scanner - TechTarget](https://www.techtarget.com/searchsecurity/tutorial/How-to-build-a-Python-port-scanner)
- [Port Scanner using Python - GeeksforGeeks](https://www.geeksforgeeks.org/port-scanner-using-python/)

## License

This project is open-source and available under the MIT License.

---

Feel free to modify it as needed! This README explains the purpose of the script, its usage, and how it works, while also giving credit to the sources you used.
