"""
statutes-rag MCP server.

本地中国法规 RAG（关键词检索版）。

Tools:
- lookup(law_name, article)
- search(query, top_k=5)
- list_laws()
- prepare_status() — 检测法规库是否已准备好

注意：法规原文不随项目分发；用户首次运行 `bash scripts/prepare-statutes.sh` 下载。
"""
from __future__ import annotations
import os
import re
from pathlib import Path
from typing import List, Dict, Any

try:
    from fastmcp import FastMCP
except ImportError:
    FastMCP = None  # type: ignore


def _default_statutes_dir() -> Path:
    return Path(__file__).resolve().parent / "statutes"


STATUTES_DIR = Path(os.environ.get("STATUTES_DIR") or _default_statutes_dir()).resolve()
INDEX_DIR = Path(
    os.environ.get("INDEX_DIR") or (Path(__file__).resolve().parent / "index")
).resolve()
INDEX_DIR.mkdir(parents=True, exist_ok=True)


_ARTICLE_RE = re.compile(r"^##\s*第\s*(\d+)\s*条\s*(.*)$", re.MULTILINE)
_LAW_TITLE_RE = re.compile(r"^#\s*《([^》]+)》", re.MULTILINE)
_PLACEHOLDER_MARK = "placeholder"  # placeholder 文件中含此标记


def _is_placeholder(text: str) -> bool:
    head = text[:600].lower()
    return _PLACEHOLDER_MARK in head and "prepare-statutes.sh" in text


def _parse_law(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if _is_placeholder(text):
        return {"law_name": path.stem, "path": str(path), "articles": {}, "placeholder": True}
    m = _LAW_TITLE_RE.search(text)
    law_name = m.group(1) if m else path.stem
    chunks = re.split(r"(?=^##\s*第\s*\d+\s*条)", text, flags=re.MULTILINE)
    articles: Dict[int, str] = {}
    for chunk in chunks:
        m = _ARTICLE_RE.search(chunk)
        if not m:
            continue
        articles[int(m.group(1))] = chunk.strip()
    return {"law_name": law_name, "path": str(path), "articles": articles, "placeholder": False}


_CACHE: List[Dict[str, Any]] = []


def _laws() -> List[Dict[str, Any]]:
    global _CACHE
    if _CACHE:
        return _CACHE
    if not STATUTES_DIR.exists():
        return []
    out = []
    for p in sorted(STATUTES_DIR.glob("*.md")):
        if p.name.startswith("_"):  # _INDEX.md 等元数据
            continue
        out.append(_parse_law(p))
    _CACHE = out
    return out


def _placeholder_warning() -> str:
    return (
        "⚠️ 本地法规库尚未下载真实原文。请在项目根目录运行：\n"
        "    bash scripts/prepare-statutes.sh\n"
        "然后重启 Claude Code。"
    )


if FastMCP is not None:
    mcp = FastMCP("statutes-rag")

    @mcp.tool()
    def lookup(law_name: str, article: int) -> Dict[str, Any]:
        """精确查询某部法规的某条原文。"""
        for law in _laws():
            if law_name in law["law_name"] or law["law_name"] in law_name:
                if law.get("placeholder"):
                    return {
                        "law": law["law_name"], "article": article,
                        "text": None, "verified": False,
                        "warning": _placeholder_warning(),
                    }
                art = law["articles"].get(article)
                if art:
                    return {
                        "law": law["law_name"], "article": article,
                        "text": art, "verified": True,
                    }
                return {
                    "law": law["law_name"], "article": article,
                    "text": None, "verified": False,
                    "warning": f"《{law['law_name']}》本地库中未找到第 {article} 条，请律师核对官方原文",
                }
        return {
            "law": law_name, "article": article, "text": None, "verified": False,
            "warning": (
                f"本地法规库未收录《{law_name}》。"
                + _placeholder_warning()
            ),
        }

    @mcp.tool()
    def search(query: str, top_k: int = 5) -> Dict[str, Any]:
        """关键词检索全部条款（含命中次数评分）。"""
        results = []
        any_placeholder = False
        for law in _laws():
            if law.get("placeholder"):
                any_placeholder = True
                continue
            for no, text in law["articles"].items():
                if query in text:
                    results.append({
                        "law": law["law_name"], "article": no,
                        "text": text, "score": text.count(query),
                    })
        results.sort(key=lambda r: -r["score"])
        return {
            "warning": _placeholder_warning() if any_placeholder and not results else "",
            "results": results[:top_k],
        }

    @mcp.tool()
    def list_laws() -> List[Dict[str, Any]]:
        """列出已收录的法规与状态。"""
        return [
            {
                "law_name": law["law_name"],
                "article_count": len(law["articles"]),
                "placeholder": law.get("placeholder", False),
                "path": law["path"],
            }
            for law in _laws()
        ]

    @mcp.tool()
    def prepare_status() -> Dict[str, Any]:
        """检测法规库是否已准备好（区分 placeholder vs 真实原文）。"""
        laws = _laws()
        total = len(laws)
        ready = sum(1 for l in laws if not l.get("placeholder") and l["articles"])
        placeholders = [l["law_name"] for l in laws if l.get("placeholder")]
        return {
            "total_files": total,
            "ready": ready,
            "placeholders": placeholders,
            "guide": _placeholder_warning() if placeholders else "✅ 法规库已准备好。",
        }

    if __name__ == "__main__":
        mcp.run()
else:
    if __name__ == "__main__":
        print("fastmcp not installed; pip install fastmcp")
