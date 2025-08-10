#!/usr/bin/env python
"""
Melody Hunter 项目启动脚本
用于快速初始化和启动项目
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """运行命令并显示描述"""
    print(f"\n{description}...")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"错误: {description} 失败")
        return False
    return True

def main():
    """主函数"""
    print("=== Melody Hunter 项目初始化 ===")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        return
    
    # 检查是否在虚拟环境中
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("警告: 建议在虚拟环境中运行此项目")
        response = input("是否继续? (y/N): ")
        if response.lower() != 'y':
            return
    
    # 安装依赖
    if not run_command("pip install -r requirements.txt", "安装Python依赖"):
        return
    
    # 运行数据库迁移
    if not run_command("python manage.py makemigrations", "创建数据库迁移文件"):
        return
    
    if not run_command("python manage.py migrate", "执行数据库迁移"):
        return
    
    # 创建超级用户（可选）
    print("\n是否创建管理员账户?")
    response = input("(y/N): ")
    if response.lower() == 'y':
        run_command("python manage.py createsuperuser", "创建管理员账户")
    
    # 收集静态文件
    run_command("python manage.py collectstatic --noinput", "收集静态文件")
    
    # 初始化基础数据
    run_command("python manage.py loaddata initial_data.json", "加载初始数据")
    
    print("\n=== 初始化完成 ===")
    print("项目已成功初始化！")
    print("\n下一步操作:")
    print("1. 复制 .env.example 为 .env 并配置数据库连接")
    print("2. 启动Redis服务 (用于Celery)")
    print("3. 启动Celery Worker: celery -A melody_hunter worker -l info")
    print("4. 启动开发服务器: python manage.py runserver")
    print("5. 访问管理后台: http://127.0.0.1:8000/admin/")
    print("6. API文档: http://127.0.0.1:8000/api/")

if __name__ == "__main__":
    main()