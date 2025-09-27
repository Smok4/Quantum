#!/usr/bin/env python3
import time
import psutil

class BlockchainMonitor:
    def __init__(self):
        self.start_time = time.time()
    
    def get_system_info(self):
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'uptime': time.time() - self.start_time
        }
    
    def monitor_loop(self):
        while True:
            info = self.get_system_info()
            print(f"📊 CPU: {info['cpu_percent']}% | RAM: {info['memory_usage']}%")
            time.sleep(10)

if __name__ == "__main__":
    monitor = BlockchainMonitor()
    monitor.monitor_loop()