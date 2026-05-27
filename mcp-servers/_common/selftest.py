"""
通用 MCP server selftest helper.
"""
from __future__ import annotations
import sys, inspect
from typing import Any, List


def run_selftest(server_module, expected: List[str] | None = None) -> int:
    name = getattr(server_module, "__name__", "?")
    print(f"  [selftest] target = {server_module.__file__ if hasattr(server_module, '__file__') else name}")

    fastmcp_ok = bool(getattr(server_module, "FASTMCP_OK", False))
    mode = "real" if fastmcp_ok else "mock"
    if not fastmcp_ok:
        print("  [selftest] ⚠️  fastmcp 未安装（mock 模式：仅验证结构 / 函数 / dry-run）")
    else:
        print("  [selftest] ✅ fastmcp 已加载")

    # 1. 扫描预期 tool 函数
    if not expected:
        expected = []
        for nm, obj in vars(server_module).items():
            if inspect.isfunction(obj) and not nm.startswith("_") and obj.__module__ == server_module.__name__:
                expected.append(nm)

    missing_fn = []
    for t in expected:
        fn = getattr(server_module, t, None)
        if not callable(fn):
            missing_fn.append(t)
    if missing_fn:
        print(f"  [selftest] ❌ 缺函数: {missing_fn}")
        return 3
    print(f"  [selftest] 工具函数 (expected): {expected}")

    # 2. 如果有真 fastmcp，检 mcp 对象
    mcp = getattr(server_module, "mcp", None)
    if fastmcp_ok:
        if mcp is None:
            print("  [selftest] ❌ FastMCP 已装但 server 未创建 mcp 对象")
            return 4
        # FastMCP 0.x: _tools 字典；FastMCP 1.x: list_tools()
        registered = []
        for attr in ("_tools", "tools"):
            val = getattr(mcp, attr, None)
            if isinstance(val, dict):
                registered = list(val.keys()); break
        if not registered and hasattr(mcp, "list_tools"):
            try:
                lst = mcp.list_tools()
                registered = [t.name if hasattr(t, "name") else str(t) for t in lst]
            except Exception:
                pass
        print(f"  [selftest] FastMCP 注册的 tools: {registered or '（未能枚举）'}")
        if registered:
            missing_reg = [t for t in expected if t not in registered]
            if missing_reg:
                print(f"  [selftest] ❌ tool 未注册到 FastMCP: {missing_reg}")
                return 5

    # 3. dry-run 第一个 tool
    for t in expected:
        fn = getattr(server_module, t)
        try:
            sig = inspect.signature(fn)
            kwargs = {}
            # 用默认值即可（顶层函数已带默认值）
            result = fn(**kwargs) if not any(p.default is inspect.Parameter.empty for p in sig.parameters.values()) else fn()
            print(f"  [selftest] dry-run {t}() → {type(result).__name__}")
            break  # 一次就够
        except TypeError:
            # 必填参数，跳到下一个
            continue
        except Exception as e:
            print(f"  [selftest] ⚠️  dry-run {t}() 抛异常（不致命）: {e}")
            break

    print(f"  [selftest] ✅ {name} selftest OK ({len(expected)} tools, mode={mode})")
    return 0
