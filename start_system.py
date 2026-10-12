#!/usr/bin/env python3
"""
系统快速启动脚本
用于实现系统关闭后快速重启功能
支持Windows和Linux操作系统
"""

import os
import sys
import platform
import subprocess
import json
import time
from pathlib import Path
import psutil

# 项目根目录（使用相对路径）
PROJECT_ROOT = Path(__file__).parent
BOOK_MANAGEMENT_DIR = PROJECT_ROOT / "book_management_system"
STATE_FILE = PROJECT_ROOT / "system_state.json"

def get_os_info():
    """获取操作系统信息"""
    os_name = platform.system()
    return os_name

def save_system_state():
    """保存系统状态"""
    print("保存系统状态...")
    try:
        state = {
            'timestamp': time.time(),
            'os': get_os_info(),
            'cwd': os.getcwd(),
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'processes': []
        }
        
        # 记录Django相关进程
        for process in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = process.info.get('cmdline', [])
                if cmdline and isinstance(cmdline, list):
                    cmdline_str = ' '.join(cmdline)
                    if 'manage.py' in cmdline_str or 'django' in cmdline_str.lower():
                        state['processes'].append({
                            'pid': process.info['pid'],
                            'name': process.info['name'],
                            'cmdline': process.info['cmdline']
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # 保存状态到文件
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        print(f"系统状态已保存到: {STATE_FILE}")
        return True
    except Exception as e:
        print(f"保存系统状态失败: {e}")
        return False

def load_system_state():
    """加载系统状态"""
    print("加载系统状态...")
    try:
        if not STATE_FILE.exists():
            print("系统状态文件不存在，使用默认配置")
            return None
        
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        print(f"系统状态加载成功 (保存时间: {time.ctime(state['timestamp'])})")
        return state
    except Exception as e:
        print(f"加载系统状态失败: {e}")
        return None

def start_django_server():
    """启动Django服务器"""
    print("启动Django服务器...")
    try:
        os.chdir(BOOK_MANAGEMENT_DIR)
        
        # 检查是否已经在运行
        for process in psutil.process_iter(['cmdline']):
            try:
                cmdline = process.info.get('cmdline', [])
                if cmdline and isinstance(cmdline, list):
                    cmdline_str = ' '.join(cmdline)
                    if 'manage.py' in cmdline_str and 'runserver' in cmdline_str:
                        print("Django服务器已经在运行")
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # 启动服务器
        print("正在启动Django服务器...")
        print("服务器将在后台运行")
        print("访问地址: http://127.0.0.1:8000/")
        
        if get_os_info() == 'Windows':
            # Windows后台启动
            subprocess.Popen([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            # Linux后台启动
            subprocess.Popen([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务器启动
        time.sleep(3)
        print("Django服务器启动成功")
        return True
    except Exception as e:
        print(f"启动Django服务器失败: {e}")
        return False

def check_server_status():
    """检查服务器状态"""
    print("检查服务器状态...")
    try:
        for process in psutil.process_iter(['cmdline']):
            try:
                cmdline = process.info.get('cmdline', [])
                if cmdline and isinstance(cmdline, list):
                    cmdline_str = ' '.join(cmdline)
                    if 'manage.py' in cmdline_str and 'runserver' in cmdline_str:
                        print("✓ Django服务器正在运行")
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        print("✗ Django服务器未运行")
        return False
    except Exception as e:
        print(f"检查服务器状态失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Django图书管理系统快速启动脚本")
    print("=" * 60)
    
    # 显示系统信息
    os_name = get_os_info()
    print(f"操作系统: {os_name}")
    
    # 加载系统状态
    state = load_system_state()
    
    # 检查并启动Django服务器
    if not check_server_status():
        start_django_server()
    
    # 再次检查状态
    if check_server_status():
        print("\n" + "=" * 60)
        print("系统启动成功！")
        print("访问地址: http://127.0.0.1:8000/")
        print("管理员账号: admin / admin123")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("系统启动失败，请检查错误信息")
        print("=" * 60)
    
    # 保存当前状态
    save_system_state()

if __name__ == "__main__":
    main()
