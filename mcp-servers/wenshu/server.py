"""
wenshu MCP server (stub-by-default).
"""
from __future__ import annotations
import os
from typing import List, Dict, Any

try:
    from fastmcp import FastMCP
    FASTMCP_OK = True
except ImportError:
    FastMCP = None  # type: ignore
    FASTMCP_OK = False

MODE = os.environ.get("WENSHU_MODE", "stub")
API_KEY = os.environ.get("WENSHU_API_KEY", "")
PRIVATE_ENDPOINT = os.environ.get("WENSHU_PRIVATE_ENDPOINT", "")


def _stub_search(query: str, court: str = "", year: str = "", limit: int = 5) -> List[Dict[str, Any]]:
    return [
        {
            "doc_no": f"(2023)沪 01 民终 {1000+i} 号",
            "court": "上海市第一中级人民法院",
            "judgment_date": f"2023-0{i+1}-15",
            "case_type": "民事",
            "issue": f"与「{query}」相关的争议（stub）",
            "holding": "（stub）本案核心裁判要旨：……",
            "applicable_laws": ["《民法典》第 1062 条"],
            "relevance": "中",
            "stub": True,
        }
        for i in range(min(limit, 3))
    ]


def search(query: str = "合同纠纷", court: str = "", year: str = "", limit: int = 5) -> Dict[str, Any]:
    """裁判文书网检索。"""
    if MODE == "stub":
        return {
            "mode": "stub",
            "warning": "⚠️ 公开 API 受限，以下案例为示意。请通过付费数据库验证。",
            "results": _stub_search(query, court, year, limit),
        }
    raise NotImplementedError("live mode 尚未实现，请配置私有 API 或使用 stub 模式")


mcp = None
if FASTMCP_OK:
    mcp = FastMCP("wenshu")
    mcp.tool()(search)


def _main():
    import sys, os
    here = os.path.dirname(os.path.abspath(__file__))
    common = os.path.normpath(os.path.join(here, "..", "_common"))
    if "--selftest" in sys.argv:
        sys.path.insert(0, os.path.dirname(common))
        try:
            from _common.selftest import run_selftest
        except ImportError:
            sys.path.insert(0, common)
            from selftest import run_selftest
        sys.exit(run_selftest(sys.modules[__name__], expected=["search"]))
    if FASTMCP_OK and mcp is not None:
        mcp.run()
    else:
        print("fastmcp not installed; pip install fastmcp", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    _main()
