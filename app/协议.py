 # -*- coding: utf-8 -*-
"""
================================================
UWB 动态定位系统 - 远程数据接收协议 (V1.2)
================================================
本脚本用于接收来自 UWB 定位主机的实时坐标与置信度数据。

1. 传输层协议: UDP (User Datagram Protocol)
2. 主机端口: 10004
3. 交互模式: 订阅模式 (Subscription)
   - 客户端需向主机发送任意数据(如 b"HELLO")以激活订阅。
   - 主机会记录客户端 IP 并开始持续推送数据。
   - 建议每 2 秒发送一次心跳包(PING)以维持订阅状态。

4. 数据格式: UTF-8 编码的 JSON 字符串 + 换行符(\n)
   示例:
   {
     "timestamp": 1678886400.123,
     "position": {"x": 5.23, "y": 3.81},
     "confidence": 0.92,
     "mode_id": 3,
     "feature_vector": {"H": 0.12, "J": 0.05, "R": 0.01}
   }

5. 字段含义:
   - timestamp: 高精度 Unix 时间戳
   - position:  预估位置坐标 (单位: 米)
   - confidence: 定位置信度 (0.0~1.0，越接近 1 越可靠)
   - mode_id:   环境模态 (1: 高遮挡干扰, 2: 非视距NLOS, 3: 稳定视距LOS)
   - feature_vector: 原始信号特征 (H:RSSI波动, J:AOA抖动, R:TOA延时)
================================================
"""

import socket
import json
import time
import threading

# ---------------- 配置区域 ----------------
# 请在此处填写运行定位程序的电脑 IP 地址
SERVER_IP = "192.168.1.XXX"  # 替换为实际的UWB主机IP
SERVER_PORT = 10004
# ------------------------------------------

class UWBRemoteClient:
    def __init__(self, ip, port):
        self.server_addr = (ip, port)
        # 创建UDP套接字
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(5.0)  # 设置5秒超时
        self.running = True  # 运行状态标记

    def heartbeat(self):
        """每隔 2 秒向服务器发送一次心跳，确保订阅活跃"""
        print(f"[*] 已启动心跳线程，目标: {self.server_addr}")
        while self.running:
            try:
                # 发送心跳包维持订阅
                self.sock.sendto(b"SUBSCRIBE_HEARTBEAT", self.server_addr)
                time.sleep(2)
            except Exception as e:
                print(f"[!] 心跳发送失败: {e}")
                time.sleep(5)  # 失败后延迟5秒重试

    def start_receiving(self):
        """主接收循环：接收并解析UWB数据"""
        # 首次发送订阅激活包
        self.sock.sendto(b"HELLO", self.server_addr)
        print(f"[*] 已发送订阅请求，开始接收 UWB 数据流...")
        
        while self.running:
            try:
                # 接收UDP数据（缓冲区4096字节）
                data, addr = self.sock.recvfrom(4096)
                if not data:
                    continue

                # 解析JSON数据（处理可能的换行符）
                try:
                    # 去除首尾空白字符（包括换行符）
                    json_data = data.decode('utf-8').strip()
                    msg = json.loads(json_data)
                    self.process_data(msg)
                except json.JSONDecodeError as e:
                    print(f"[!] JSON解析失败: {e} | 原始数据: {data}")
            except socket.timeout:
                print("[!] 接收超时，重新发送订阅请求...")
                self.sock.sendto(b"RE-SUBSCRIBE", self.server_addr)
            except Exception as e:
                print(f"[!] 接收数据出错: {e}")
                break

    def process_data(self, data):
        """
        业务处理逻辑：可根据需求修改（如存数据库、更新UI、触发警报等）
        """
        # 提取核心数据（带默认值防止字段缺失）
        timestamp = data.get("timestamp", time.time())
        position = data.get("position", {"x": 0.0, "y": 0.0})
        confidence = data.get("confidence", 0.0)
        mode_id = data.get("mode_id", "Unknown")
        feature_vector = data.get("feature_vector", {})

        # 格式化输出
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        print(f"\n[数据接收] {time_str}")
        print(f"  坐标: X={position['x']:.2f}m, Y={position['y']:.2f}m")
        print(f"  置信度: {confidence:.3f} (越高越可靠)")
        print(f"  环境模态: {mode_id} (1=高遮挡, 2=非视距, 3=稳定视距)")
        print(f"  信号特征: {feature_vector}")

    def stop(self):
        """停止客户端运行"""
        self.running = False
        self.sock.close()
        print("[*] UWB客户端已停止")

if __name__ == "__main__":
    # 打印本机IP（方便服务器端确认）
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"[*] 本机局域网IP: {local_ip}")
        print(f"[*] 目标UWB服务器: {SERVER_IP}:{SERVER_PORT}")
    except Exception as e:
        print(f"[!] 获取本机IP失败: {e}")

    # 初始化客户端
    uwb_client = UWBRemoteClient(SERVER_IP, SERVER_PORT)

    # 启动心跳线程（守护线程，主程序退出时自动结束）
    heartbeat_thread = threading.Thread(target=uwb_client.heartbeat, daemon=True)
    heartbeat_thread.start()

    # 启动数据接收（捕获Ctrl+C退出）
    try:
        uwb_client.start_receiving()
    except KeyboardInterrupt:
        print("\n[*] 检测到用户中断，正在停止...")
        uwb_client.stop()
    except Exception as e:
        print(f"[!] 程序异常退出: {e}")
        uwb_client.stop()