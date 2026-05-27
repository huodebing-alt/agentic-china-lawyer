"""
samr MCP server (stub-by-default).
"""
from __future__ import annotations
import os
from typing import Dict, Any, List

try:
    from fastmcp import FastMCP
    FASTMCP_OK = True
except ImportError:
    FastMCP = None  # type: ignore
    FASTMCP_OK = False

MODE = os.environ.get("SAMR_MODE", "stub")


def _stub_company(name: str) -> Dict[str, Any]:
    return {
        "name": name,
        "unified_social_credit_code": "91310000XXXXXXXXXX",
        "legal_representative": "（stub）张三",
        "registered_capital": "1,000 万元人民币（认缴）",
        "paid_in_capital": "800 万元人民币",
        "establishment_date": "2018-06-20",
        "status": "存续",
        "registered_address": "（stub）上海市浦东新区 XX 路 X 号",
        "business_scope": "（stub）一般项目：技术开发、技术咨询、技术服务……",
        "shareholders": [
            {"name": "（stub）某控股有限公司", "ratio": "70%"},
            {"name": "（stub）创始人", "ratio": "30%"},
        ],
        "administrative_penalties": [],
        "abnormal_records": [],
        "stub": True,
    }


def search(company_name: str = "未指定公司", uscc: str = "") -> Dict[str, Any]:
    """按公司名称或统一社会信用代码查询。"""
    if MODE == "stub":
        return {
            "mode": "stub",
            "warning": "⚠️ 公开 stub 数据，请通过 SAMR 官网 / 企查查 / 天眼查核实。",
            "data": _stub_company(company_name or uscc or "未指定公司"),
        }
    raise NotImplementedError("live mode 尚未实现")


def equity_penetration(company_name: str = "未指定公司", depth: int = 3) -> Dict[str, Any]:
    """股权穿透查询（最多 3 层）。"""
    return {
        "mode": MODE,
        "warning": "⚠️ stub 数据" if MODE == "stub" else "",
        "tree": {
            "name": company_name,
            "children": [
                {"name": "（stub）控股股东", "ratio": "70%", "children": []},
                {"name": "（stub）员工持股平台", "ratio": "20%", "children": []},
                {"name": "（stub）其他", "ratio": "10%", "children": []},
            ],
        },
    }


mcp = None
if FASTMCP_OK:
    mcp = FastMCP("samr")
    mcp.tool()(search)
    mcp.tool()(equity_penetration)


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
        sys.exit(run_selftest(sys.modules[__name__], expected=["search", "equity_penetration"]))
    if FASTMCP_OK and mcp is not None:
        mcp.run()
    else:
        print("fastmcp not installed; pip install fastmcp", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    _main()
