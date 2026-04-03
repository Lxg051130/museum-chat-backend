"""
启动脚本 - 一键启动服务
"""
import os
import sys
import subprocess
from pathlib import Path

# 获取项目根目录
project_root = Path(__file__).parent

def check_env_file():
    """检查.env文件是否存在"""
    env_file = project_root / ".env"
    env_example_file = project_root / ".env.example"
    
    if not env_file.exists():
        print("⚠️  .env文件不存在，正在创建...")
        if env_example_file.exists():
            import shutil
            shutil.copy(env_example_file, env_file)
            print(f"✅ .env文件已创建，请编辑配置项")
        else:
            print("❌ .env.example文件不存在")
            sys.exit(1)

def create_logs_directory():
    """创建日志目录"""
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    print(f"✅ 日志目录已就绪: {logs_dir}")

def main():
    print("""
    ╔════════════════════════════════════════╗
    ║  Museum Chat Backend - 启动脚本        ║
    ║  v1.0.0                               ║
    ╚════════════════════════════════════════╝
    """)
    
    # 检查环境
    check_env_file()
    create_logs_directory()
    
    # 启动参数
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 8000))
    reload = os.getenv("DEBUG", "False") == "True"
    
    print(f"""
    📝 启动配置：
    - Host: {host}
    - Port: {port}
    - Debug: {reload}
    - Reload: {reload}
    """)
    
    print("🚀 启动服务中...")
    
    try:
        # 启动uvicorn服务器
        subprocess.run(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "app.main:app",
                f"--host={host}",
                f"--port={port}",
                "--reload" if reload else ""
            ],
            cwd=project_root
        )
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
