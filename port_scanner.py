import socket
import threading
import time
import os

def clear_screen():
    # Detecta o sistema operacional e executa o comando adequado
    os.system('cls' if os.name == 'nt' else 'clear')

# Funcao para tentar obter o banner de um servico na porta especificada
def get_banner(host, port):
    try:
        # Cria um socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Define o tempo limite de conexao para 1 segundo
            s.connect((host, port))  # Conecta o host e a porta
            banner = s.recv(1024).decode('utf-8', errors='ignore')  # Tenta ler o banner do servico
            return banner.strip()  # Retorna o banner sem espaços extras
    except socket.error:
        return None  # Se ocorrer um erro (como nao conseguir se conectar), retorna None

# Funcao para escanear portas TCP
def scan_port_tcp(host, port, open_ports, service_info):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))  # Tenta conectar à porta
            if result == 0:  # Se a conexao for bem sucedida (resultado 0)
                open_ports.append(port)  # Adiciona a porta à lista de portas abertas
                banner = get_banner(host, port)  # Tenta obter o banner do serviço
                if banner:
                    service_info[port] = banner  # Armazena o banner (ou "Unknow Service" se nao houver)
                else:
                    service_info[port] = "Unknow Service"
    except socket.error:
        pass  # Se nao conseguir se conectar à porta, ignora

# Funcao para escanear portas UDP
def scan_udp(host, port, open_ports_udp):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:  # Usando o socket UDP
            s.settimeout(1)
            s.sendto(b'', (host, port))  # Envia um pacote vazio para testar a resposta da porta UDP
            s.recvfrom(1024)  # Espera por uma resposta (se houver)
            open_ports_udp.append(port)  # Se receber uma resposta, adiciona a porta à lista de portas abertas UDP
    except socket.error:
        pass

# Funcao principal para realizar o escaneamento e exibir os resultados
def main():
    start_time = time.time()  # Marca o tempo de inicio para calcular a duracao do escaneamento

    # E bem obvio mas tenho q fazer comentarios pq eu fixo melhor assim
    # solicita ao usuario o IP do host e o intervalo de portas
    host = input("Enter the adress IP or host domain: ")
    port_start = int(input("Enter the start port range: "))  # Convertido para inteiro
    port_end = int(input("Enter de end of port range: "))  # Convertido para inteiro

    clear_screen()  # Limpa a tela após os inputs

    # Mostra a data e a hora de inicio (sim, igual ao do nmap :])
    print(f"\nStarting Scan at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Scan report for {host}")

    # Verificando se o host está online e calcula a latência
    try:
        start_ping_time = time.time()  # Marca o tempo para calcular a latência
        socket.gethostbyname(host)  # Tenta resolver o nome de domínio para o endereço IP
        ping_time = round((time.time() - start_ping_time) * 1000, 4)  # Calcula a latência em ms
        print(f"Host is up ({ping_time}s latency).")
    except socket.error:
        print("Host is down :(")  # autoexplicativo (se não for resolvido, está off)
        return  # Encerra a execução do script

    print(f"Scanning {port_start}-{port_end} ports...")  # Informa as portas que serão escaneadas

    open_ports_tcp = []  # Lista para armazenar portas TCP abertas
    open_ports_udp = []  # Lista para armazenar portas UDP abertas
    service_info = {}  # Dicionario para armazenar informações sobre os banners dos serviços

    # Cria threads para escanear portas TCP em paralelo
    threads_tcp = []
    for port in range(port_start, port_end + 1):
        thread_tcp = threading.Thread(target=scan_port_tcp, args=(host, port, open_ports_tcp, service_info))
        threads_tcp.append(thread_tcp)  # Corrigido para adicionar a thread, não a lista
        thread_tcp.start()  # Inicia a thread para fazer o scan TCP

    # Cria threads para escanear portas UDP em paralelo
    threads_udp = []
    for port in range(port_start, port_end + 1):
        thread_udp = threading.Thread(target=scan_udp, args=(host, port, open_ports_udp))
        threads_udp.append(thread_udp)  # Corrigido para adicionar a thread, não a lista
        thread_udp.start()  # Inicia a thread para fazer o scan UDP

    # Aguarda a conclusão de todas as threads
    for thread in threads_tcp:
        thread.join()

    for thread in threads_udp:
        thread.join()

    # Calcula a duração total do escaneamento
    scan_duration = round(time.time() - start_time, 2)

    # Exibe o tempo total do scan e a quantidade de IPs escaneados
    print(f"Scan finished: 1 IP Address ({host}) scanned in {scan_duration} seconds.")

    # Exibe as portas TCP abertas, se houver
    if open_ports_tcp:
        print("\nTCP Port open:")
        for port in open_ports_tcp:
            print(f"[+] Port {port}: {service_info.get(port, 'Unkown Service')}")
    else:
        print("\nNo open TCP Ports found :(")  # Se não houver portas abertas TCP, informa o usuário

    # Agora Exibe as portas UDP abertas
    if open_ports_udp:
        print("\nUDP Ports open:")
        for port in open_ports_udp:
            print(f"[+] Port {port} is open!")
    else:
        print("\nNo open UDP Ports found.")  # Se não houver portas abertas UDP, informa o usuário

    # Link do meu repositório, o mais hackers de todos os tempos
    print("\nCheck my other projects on my github: https://github.com/vituwc/")

# Inicia o programa chamando a função principal
if __name__ == "__main__":
    main()