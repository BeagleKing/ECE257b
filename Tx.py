import socket
import numpy as np
import signal
import sys
import os

server_ip = "67.58.54.136"  # 替换为接收端 IP
server_port = 2000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, server_port))

device_id = os.getenv("DEVICE_ID", "device_01")
packet_count = 0  # 计数发送的数据包数

def handle_exit(sig, frame):
    """ 终止程序时打印发送的总包数 """
    print(f"\n终止发送！共发送 {packet_count} 个数据包")
    sock.close()
    sys.exit(0)

# 监听 Ctrl+C (终止信号)
signal.signal(signal.SIGINT, handle_exit)

while True:
    iq_data = np.random.randn(1024) + 1j * np.random.randn(1024)  # 生成模拟 I/$
    iq_bytes = iq_data.astype(np.complex64).tobytes()

    packet = f"{device_id}:".encode() + iq_bytes
    sock.sendall(packet)

    packet_count += 1  # 计数
    print(f"正在发送数据包 {packet_count}...")
