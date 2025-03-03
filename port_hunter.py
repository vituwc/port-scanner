from concurrent.futures import ThreadPoolExecutor
import socket
import threading
import time
import os

# Function to clear the screen depending on the OS (Windows or Linux)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to try to obtain the banner from a service on the specified port
def get_banner(host, port):
    try:
        # Create a TCP socket and attempt to connect to the host and port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Set connection timeout to 1 second
            s.connect((host, port))  # Connect to the target host and port
            banner = s.recv(1024).decode('utf-8', errors='ignore')  # Try to read the service banner
            return banner.strip()  # Return the banner with extra spaces removed
    except (socket.error, UnicodeDecodeError):
        return None  # Return None if any error occurs (like connection failure or banner read failure)

# Function to scan a single TCP port on the given host
def scan_port_tcp(host, port, open_ports, service_info):
    try:
        # Create a TCP socket and attempt to connect to the host and port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Set connection timeout to 1 second
            result = s.connect_ex((host, port))  # Attempt to connect to the target port
            if result == 0:  # If connection is successful (result == 0)
                open_ports.append(port)  # Add the port to the open_ports list
                banner = get_banner(host, port)  # Try to get the service banner for the port
                service_info[port] = banner if banner else "Unknown Service"  # Store the banner or "Unknown Service" if no banner is found
    except socket.error:
        pass  # If any error occurs (like connection failure), simply pass and move on

# Function to scan a single UDP port on the given host
def scan_udp(host, port, open_ports_udp):
    try:
        # Create a UDP socket and attempt to send a packet to the host and port
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(1)  # Set timeout to 1 second
            s.sendto(b'', (host, port))  # Send an empty packet to the port
            s.recvfrom(1024)  # Wait for a response (if any)
            open_ports_udp.append(port)  # If a response is received, add the port to the open_ports_udp list
    except socket.error:
        pass  # If any error occurs (like no response), simply pass and move on

# Main function to execute the scan and display results
def main():
    start_time = time.time()  # Record the start time to calculate the scan duration
    host = input("Enter the address IP or host domain: ")  # Prompt user for the target IP or domain
    port_start = int(input("Enter the start port range: "))  # Prompt user for the starting port
    port_end = int(input("Enter the end of port range: "))  # Prompt user for the ending port

    clear_screen()  # Clear the screen after input

    # Print the scan start time and target host information
    print(f"\nStarting Scan at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Scan report for {host}")

    try:
        # Try to resolve the host to ensure it's online and measure the latency
        start_ping_time = time.time()
        socket.gethostbyname(host)  # Resolve the host to an IP address
        ping_time = round((time.time() - start_ping_time) * 1000, 4)  # Calculate the latency in milliseconds
        print(f"Host is up ({ping_time} ms latency).")  # Print the host status and latency
    except socket.error:
        # If the host cannot be resolved, print an error message and terminate
        print("Host is down :(")
        return

    print(f"Scanning {port_start}-{port_end} ports...")  # Inform the user about the port range being scanned

    open_ports_tcp = []  # List to store open TCP ports
    open_ports_udp = []  # List to store open UDP ports
    service_info = {}  # Dictionary to store service banners for open TCP ports

    # Use ThreadPoolExecutor to manage and execute threads for TCP port scanning
    with ThreadPoolExecutor(max_workers=50) as executor:
        tcp_futures = [executor.submit(scan_port_tcp, host, port, open_ports_tcp, service_info) for port in range(port_start, port_end + 1)]
        udp_futures = [executor.submit(scan_udp, host, port, open_ports_udp) for port in range(port_start, port_end + 1)]
        
        # Wait for all threads to complete and handle exceptions if any
        for future in tcp_futures + udp_futures:
            future.result()  # Calling result() ensures that any exceptions are raised and handled

    # Calculate the total duration of the scan
    scan_duration = round(time.time() - start_time, 2)
    print(f"Scan finished: 1 IP Address ({host}) scanned in {scan_duration} seconds.")

    # Display the results for open TCP ports, if any
    if open_ports_tcp:
        print("\nTCP Ports open:")
        for port in open_ports_tcp:
            print(f"[+] Port {port}: {service_info.get(port, 'Unknown Service')}")
    else:
        print("\nNo open TCP Ports found.")  # If no TCP ports are open, inform the user

    # Display the results for open UDP ports, if any
    if open_ports_udp:
        print("\nUDP Ports open:")
        for port in open_ports_udp:
            print(f"[+] Port {port} is open!")
    else:
        print("\nNo open UDP Ports found.")  # If no UDP ports are open, inform the user

    # Print a message with a link to your GitHub for other projects
    print("\nCheck my other projects on my github: https://github.com/vituwc/")

# Execute the main function if this script is run directly
if __name__ == "__main__":
    main()
