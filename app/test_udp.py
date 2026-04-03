#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UDP发送端（JSON版）：发送标准JSON格式数据到服务器
"""
import socket
import json

def send_udp_json(server_ip, server_port, json_data, buffer_size=65535):
    """
    发送UTF-8编码的JSON数据到指定UDP服务器
    :param server_ip: 目标服务器IP
    :param server_port: 目标UDP端口
    :param json_data: 要发送的JSON字典/列表
    :param buffer_size: UDP缓冲区
    """
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buffer_size)

    try:
        # 1. 将Python对象转为JSON字符串（ensure_ascii=False支持中文）
        json_str = json.dumps(json_data, ensure_ascii=False)
        # 2. 编码为UTF-8字节
        send_data = json_str.encode("utf-8")
        data_len = len(send_data)

        if data_len > 65507:
            print(f"⚠️ JSON数据过大（{data_len}字节），建议拆分/改用TCP！")
        
        # 3. 发送数据
        target_addr = (server_ip, server_port)
        udp_socket.sendto(send_data, target_addr)

        # 打印结果
        print(f"✅ UDP JSON发送成功：")
        print(f"   目标服务器：{target_addr}")
        print(f"   数据长度：{data_len}字节")
        print(f"   JSON内容：\n{json.dumps(json_data, ensure_ascii=False, indent=2)}")

    except json.JSONDecodeError as e:
        print(f"❌ JSON格式化失败：{e}")
    except Exception as e:
        print(f"❌ 发送失败：{e}")
    finally:
        udp_socket.close()

if __name__ == "__main__":
    SERVER_IP = "8.136.220.87"
    SERVER_PORT = 8081
    

    # 要发送的JSON数据（支持复杂结构）
    json_data = {
        "device_id": "dev_123456",
        "timestamp": 1711234567,
        "data": {
            "temperature": 25.6,
            "humidity": 60.2,
            "status": "normal",
            "备注": "这是包含中文的JSON数据"
        },
        "list_data": [1, 2, 3, "测试"]
    }

    # 调用发送函数
    send_udp_json(SERVER_IP, SERVER_PORT, json_data)