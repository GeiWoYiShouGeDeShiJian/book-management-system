#!/usr/bin/env python3
"""
环境配置脚本
用于跨设备快速部署和配置项目运行环境
支持Windows和Linux操作系统
"""

import os
import sys
import platform
import subprocess
import time
from pathlib import Path

# 项目根目录（使用相对路径）
PROJECT_ROOT = Path(__file__).parent
BOOK_MANAGEMENT_DIR = PROJECT_ROOT / "book_management_system"

# 依赖包列表
REQUIREMENTS = [
    "Django>=4.2.0,<5.0",
    "Pillow>=10.0.0",
    "django-bootstrap5>=23.3.0",
    "psycopg2-binary>=2.9.0",
    "dj-database-url>=2.0.0",
    "django-debug-toolbar>=4.1.0",
    "pytest-django>=4.5.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "gunicorn>=21.0.0",
    "whitenoise>=6.5.0"
]

def get_os_info():
    """获取操作系统信息"""
    os_name = platform.system()
    os_version = platform.version()
    return os_name, os_version

def check_python():
    """检查Python版本"""
    print("检查Python版本...")
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 9):
        print(f"错误: Python版本 {python_version.major}.{python_version.minor} 过低，需要Python 3.9+")
        return False
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro} (满足要求)")
    return True

def install_pip_packages():
    """安装pip包"""
    print("\n安装依赖包...")
    try:
        # 升级pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True, text=True)
        print("pip已升级到最新版本")
        
        # 安装依赖包
        for package in REQUIREMENTS:
            print(f"安装: {package}")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"✓ {package} 安装成功")
            else:
                print(f"✗ {package} 安装失败: {result.stderr}")
                return False
        return True
    except Exception as e:
        print(f"安装依赖包时出错: {e}")
        return False

def setup_project():
    """设置项目"""
    print("\n设置项目...")
    try:
        # 进入项目目录
        os.chdir(BOOK_MANAGEMENT_DIR)
        
        # 运行数据库迁移
        print("运行数据库迁移...")
        result = subprocess.run(
            [sys.executable, "manage.py", "migrate"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("数据库迁移成功")
        else:
            print(f"数据库迁移失败: {result.stderr}")
            return False
        
        # 创建超级用户（如果不存在）
        print("检查超级用户...")
        create_superuser_script = '''
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123', first_name='管理员')
    print('超级用户创建成功')
else:
    print('超级用户已存在')
'''
        result = subprocess.run(
            [sys.executable, "manage.py", "shell"],
            input=create_superuser_script, text=True, capture_output=True
        )
        print(result.stdout)
        if "创建成功" in result.stdout or "已存在" in result.stdout:
            print("超级用户设置完成")
        else:
            print(f"超级用户设置失败: {result.stderr}")
        
        return True
    except Exception as e:
        print(f"设置项目时出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Django图书管理系统环境配置脚本")
    print("=" * 60)
    
    # 显示系统信息
    os_name, os_version = get_os_info()
    print(f"操作系统: {os_name} {os_version}")
    
    # 检查Python
    if not check_python():
        return
    
    # 安装依赖包
    if not install_pip_packages():
        return
    
    # 设置项目
    if not setup_project():
        return
    
    print("\n" + "=" * 60)
    print("环境配置完成！")
    print("可以通过以下命令启动系统:")
    print(f"cd {BOOK_MANAGEMENT_DIR}")
    print("python manage.py runserver")
    print("=" * 60)

if __name__ == "__main__":
    main()
