"""Structured logging for Saygo agent.

Adds a per-thread / per-case context label that gets injected into every
log line. Dispatch mode runs N worker threads concurrently and their log
lines were interleaving with no way to attribute a Turn / step_progress /
evidence line back to its case — making post-hoc audit of LLM behavior
nearly impossible.

Usage:
    from saygo.logger import set_case_context

    # in dispatcher worker thread, before each case:
    set_case_context(f"W{worker_idx}/c{case_idx}")

    # after teardown / between cases:
    set_case_context(f"W{worker_idx}")   # or "" to clear
"""

import contextvars
import logging
import sys
from contextlib import contextmanager

# Per-thread context label (e.g. "W1/c40"). Lives in contextvars so each
# worker thread can set independently without polluting sibling threads.
_case_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "saygo_case_ctx", default=""
)
_redactions = contextvars.ContextVar('saygo_redactions', default=())


@contextmanager
def redact_values(value):
    """Do not print configured account values, including custom fields and nested tokens."""
    def strings(item):
        if isinstance(item, str) and item:
            yield item
        elif isinstance(item, dict):
            for child in item.values():
                yield from strings(child)
        elif isinstance(item, (list, tuple)):
            for child in item:
                yield from strings(child)
    values = tuple(sorted(set(_redactions.get()) | set(strings(value)), key=len, reverse=True))
    token = _redactions.set(values)
    try:
        yield
    finally:
        _redactions.reset(token)


class _RedactionFilter(logging.Filter):
    def filter(self, record):
        values = _redactions.get()
        if values:
            message = record.getMessage()
            exception = logging.Formatter().formatException(record.exc_info) if record.exc_info else record.exc_text
            for value in values:
                message = message.replace(value, '[REDACTED]')
                if exception:
                    exception = exception.replace(value, '[REDACTED]')
            record.msg, record.args = message, ()
            record.exc_text, record.exc_info = exception, None
        return True


def set_case_context(label: str) -> None:
    """Set the current thread's case context label. Empty string clears."""
    _case_ctx.set(label or "")


class _CaseContextFilter(logging.Filter):
    """Inject %(case_ctx)s into every LogRecord based on the current
    thread's _case_ctx ContextVar."""

    def filter(self, record: logging.LogRecord) -> bool:
        ctx = _case_ctx.get()
        record.case_ctx = f"[{ctx}] " if ctx else ""
        return True


LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(case_ctx)s%(message)s"
DATE_FORMAT = "%H:%M:%S"

# Level 统一挂在 "saygo" 父 logger 上：子 logger 留 NOTSET 继承父级 level，
# set_level 改父级即对已存在 + 之后新建的所有 saygo.* logger 生效。
# （handler 仍挂在各子 logger 上且 propagate=False，避免重复输出 — propagate
# 只影响 record 分发，不影响 effective level 的向上查找。）
logging.getLogger("saygo").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """Get a named logger under the 'saygo' namespace."""
    logger = logging.getLogger(f"saygo.{name}")
    if not any(isinstance(item, _RedactionFilter) for item in logger.filters):
        logger.addFilter(_RedactionFilter())
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr) if sys.stderr is not None else logging.NullHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        handler.addFilter(_CaseContextFilter())
        logger.addHandler(handler)
        # level 不在子 logger 上设（保持 NOTSET 继承 "saygo" 父级），
        # 否则 set_level("DEBUG") 永远压不过子级的 INFO，debug 日志全部不可达
        logger.propagate = False
    return logger


def set_level(level: str) -> None:
    """Set log level for all saygo loggers. E.g. 'DEBUG', 'WARNING'."""
    logging.getLogger("saygo").setLevel(getattr(logging, level.upper(), logging.INFO))
