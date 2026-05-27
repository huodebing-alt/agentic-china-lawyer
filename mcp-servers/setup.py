"""
最小化 setup.py — 把 statutes-rag / wenshu / samr / cnipa 暴露为
mcp_servers.statutes_rag / mcp_servers.wenshu / mcp_servers.samr / mcp_servers.cnipa

实际安装：pip install -e mcp-servers/
"""
from setuptools import setup, find_packages
setup(
    name="agentic-china-lawyer-mcp-servers",
    version="0.1.0",
    packages=find_packages(),
    package_dir={
        "mcp_servers.statutes_rag": "statutes-rag",
        "mcp_servers.wenshu": "wenshu",
        "mcp_servers.samr": "samr",
        "mcp_servers.cnipa": "cnipa",
    },
)
