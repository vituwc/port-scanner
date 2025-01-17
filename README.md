# **Port Scanner**

Este é um simples **Scanner de Portas TCP e UDP** desenvolvido em Python, criado para fins de treinamento e testes. Ele escaneia um intervalo de portas em um host remoto e tenta obter banners dos serviços nas portas abertas.

---

## **Como Usar**

1. Faça o download ou clone este repositório.
2. Execute o script no terminal:

```bash
python port_scanner.py
```

3. O script solicitará o **IP ou domínio do host** e o **intervalo de portas** para escanear.

---

## **Exemplo de Execução**

```bash
Enter the address IP or host domain: 172.67.192.199
Enter the start port range: 1
Enter the end of port range: 1024

Starting Scan...
Scan finished: 1 IP Address scanned.
TCP Ports open:
[+] Port 80: Unknown Service
[+] Port 443: Unknown Service

No open UDP Ports found.
```
