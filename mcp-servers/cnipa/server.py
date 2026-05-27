"""
cnipa MCP server (stub-by-default).
"""
from __future__ import annotations
import os
from typing import Dict, Any

try:
    from fastmcp import FastMCP
    FASTMCP_OK = True
except ImportError:
    FastMCP = None  # type: ignore
    FASTMCP_OK = False

MODE = os.environ.get("CNIPA_MODE", "stub")


def search_trademark(name: str = "示例商标", nice_class: int = 35, applicant: str = "") -> Dict[str, Any]:
    """商标检索。"""
    if MODE == "stub":
        return {
            "mode": "stub",
            "warning": "⚠️ stub 数据，请通过 sbj.cnipa.gov.cn 验证",
            "results": [
                {
                    "app_no": "999999",
                    "reg_no": "888888",
                    "name": name or "示例商标",
                    "nice_class": nice_class or 35,
                    "applicant": applicant or "示例公司",
                    "status": "已注册",
                    "filed_date": "2020-01-01",
                    "registered_date": "2021-06-15",
                    "stub": True,
                }
            ],
        }
    raise NotImplementedError("live mode 尚未实现")


def search_patent(keyword: str = "示例", app_no: str = "", applicant: str = "") -> Dict[str, Any]:
    """专利检索。"""
    if MODE == "stub":
        return {
            "mode": "stub",
            "warning": "⚠️ stub 数据，请通过 pss-system.cponline.cnipa.gov.cn 验证",
            "results": [
                {
                    "app_no": "CN20231012345.6",
                    "publication_no": "CN116666666A",
                    "title": keyword or "示例发明专利",
                    "type": "发明",
                    "applicant": applicant or "示例公司",
                    "filed_date": "2023-01-10",
                    "publication_date": "2023-07-15",
                    "status": "实质审查中",
                    "stub": True,
                }
            ],
        }
    raise NotImplementedError("live mode 尚未实现")


mcp = None
if FASTMCP_OK:
    mcp = FastMCP("cnipa")
    mcp.tool()(search_trademark)
    mcp.tool()(search_patent)


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
        sys.exit(run_selftest(sys.modules[__name__], expected=["search_trademark", "search_patent"]))
    if FASTMCP_OK and mcp is not None:
        mcp.run()
    else:
        print("fastmcp not installed; pip install fastmcp", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    _main()
