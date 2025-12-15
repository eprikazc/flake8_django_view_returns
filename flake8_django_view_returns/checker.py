from __future__ import annotations

import ast
from typing import Iterator, Tuple


class DjangoViewReturnChecker:
    """
    Heuristic rule:
      if filename contains 'views'
      AND (first arg is 'request' OR first two args are ('self'|'cls', 'request'))
      THEN assume this is a django endpoint and emit warning if it returns None / implicit None
      (django endpoints should return Http Response and never None)
    """

    name = "flake8-django-view-returns"
    version = "0.1.0"

    CODE = "DJV001"
    MSG = f"{CODE} Django view-like callable returns None (missing HttpResponse return)"

    def __init__(self, tree: ast.AST, filename: str = "") -> None:
        self.tree = tree
        self.filename = filename or ""

    def run(self) -> Iterator[Tuple[int, int, str, type]]:
        path = self.filename.replace("\\", "/")
        if "views" not in path:
            return

        for node in ast.walk(self.tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            if not self._looks_like_view(node):
                continue

            if self._returns_none_or_implicit(node):
                yield (node.lineno, node.col_offset, self.MSG, type(self))

    def _looks_like_view(self, fn: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        args = fn.args.args
        if not args:
            return False

        if fn.name.startswith("_"):  # view names are not private
            return False

        # Function-based view: (request, ...)
        if args[0].arg == "request":
            return True

        # Method-based view: (self|cls, request, ...)
        if len(args) >= 2 and args[0].arg in {"self", "cls"} and args[1].arg == "request":
            return True

        return False

    def _returns_none_or_implicit(self, fn: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        for n in ast.walk(fn):
            if isinstance(n, ast.Return):
                if n.value is None:
                    return True
                if isinstance(n.value, ast.Constant) and n.value.value is None:
                    return True
        return False
