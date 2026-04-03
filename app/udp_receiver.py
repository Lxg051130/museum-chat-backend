#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云服务器UDP接收端：监听全网UDP数据（0.0.0.0）
"""
import socket
import sys
import json

def start_udp_server(port=8081, buffer_size=1024):
    # 1. 创建UDP套接字（SOCK_DGRAM = UDP协议）
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"✅ UDP套接字创建成功")
    except socket.error as e:
        print(f"❌ 创建UDP套接字失败：{e}")
        sys.exit(1)

    # 2. 绑定端口（关键！必须绑定0.0.0.0，否则外网无法访问）
    bind_addr = ("0.0.0.0", port)  # 0.0.0.0 = 监听服务器所有网卡（公网/内网）
    try:
        udp_socket.bind(bind_addr)
        print(f"✅ 已绑定 UDP {bind_addr}，等待接收数据...")
        print(f"📌 别人可往 你的服务器公网IP:{port} 发送UDP数据")
    except socket.error as e:
        print(f"❌ 绑定端口失败（可能端口被占用/无权限）：{e}")
        udp_socket.close()
        sys.exit(1)

    # 3. 循环接收UDP数据（持续运行）
    try:
        while True:
            # recvfrom：接收数据，返回 (数据字节, (发送方IP, 发送方端口))
            data, sender_addr = udp_socket.recvfrom(buffer_size)
            # 解码字节数据为字符串（兼容中文）
            data_str = data.decode("utf-8", errors="ignore")
            json_data=json.loads(data_str)
            list1=json_data.get("list_data")
            print(list1)
            # 打印接收结果
            print(f"\n📥 收到UDP数据：")
            print(f"   发送方：{sender_addr}")
            print(f"   内容：{data_str}")
    except KeyboardInterrupt:
        print(f"\n⚠️ 用户终止程序，正在关闭...")
    except Exception as e:
        print(f"\n❌ 接收数据异常：{e}")
    finally:
        # 4. 关闭套接字
        udp_socket.close()
        print(f"✅ UDP服务器已关闭")

if __name__ == "__main__":
    # 自定义端口（建议选1024以上，避免权限问题）
    UDP_PORT = 8081  # 可改成你想使用的端口（如9999）
    start_udp_server(port=UDP_PORT)