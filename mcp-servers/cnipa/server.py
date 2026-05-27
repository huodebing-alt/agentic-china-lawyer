"""
cnipa MCP server: 商标 / 专利检索。
公开版 stub。
"""
from __future__ import annotations
import os
from typing import Dict, Any, List

try:
    from fastmcp import FastMCP
except ImportError:
    FastMCP = None  # type: ignore

MODE = os.environ.get("CNIPA_MODE", "stub")
API_KEY = os.environ.get("CNIPA_API_KEY", "")


if FastMCP is not None:
    mcp = FastMCP("cnipa")

    @mcp.tool()
    def search_trademark(name: str = "", nice_class: int = 0, applicant: str = "") -> Dict[str, Any]:
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

    @mcp.tool()
    def search_patent(keyword: str = "", app_no: str = "", applicant: str = "") -> Dict[str, Any]:
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

    if __name__ == "__main__":
        mcp.run()
else:
    if __name__ == "__main__":
        print("fastmcp not installed")
