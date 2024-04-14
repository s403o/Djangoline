import logging
import structlog
import os
import sys
import threading
from structlog.contextvars import bind_contextvars, bound_contextvars, get_contextvars
from typing import TYPE_CHECKING, Optional, Callable, Iterable, Any, Mapping
import warnings

from opentelemetry import trace


def add_open_telemetry_spans(_, __, event_dict):
    span = trace.get_current_span()
    if not span.is_recording():
        event_dict["span"] = None
        return event_dict

    ctx = span.get_span_context()
    parent = getattr(span, "parent", None)

    event_dict["span_id"] = format(ctx.span_id, "x")
    event_dict["trace_id"] = format(ctx.trace_id, "x")
    if parent is not None:
        event_dict["parent_span_id"] = format(parent.span_id, "x")
    return event_dict


def execption_liner(logger, method_name, event_dict):
    if "exception" in event_dict:
        # print(f"{event_dict['exception']=}")
        event_dict["exception"] = event_dict["exception"].replace("\n", "\\\n") #str(event_dict["exception"].splitlines())
    return event_dict

old_thread = threading.Thread
class Threadv2(threading.Thread):
    def __init__(self, group: None = None, target: Optional[Callable[..., object]] = None, name: Optional[str] = None, args: Iterable[Any] = (), kwargs: Optional[Mapping[str, Any]]= None, *, daemon: Optional[bool] = None) -> None:
        self.structlog_contextvars = get_contextvars()
        old_thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
    def run(self) -> None:
        with bound_contextvars(**self.structlog_contextvars):
            return super().run()

def patch_threading():
    threading.Thread = Threadv2


def patch_unhandled_exceptions(logger):
    def logger_excepthook(*exc_info):
        logger.critical("exception should be handled", exc_info=exc_info)
    sys.excepthook = logger_excepthook

_old_warnings = set()

def patch_warnings(logger):
    def rememberer(message, *args, **kwargs):
        if message in _old_warnings:
            return
        _old_warnings.add(message)
        logger.warning(message, args=args, **kwargs)
    warnings.warn = rememberer


def setup_log():
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_log_level_number,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.CallsiteParameterAdder(),
        structlog.processors.format_exc_info,
        add_open_telemetry_spans,
        # execption_liner,
    ]

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter_processors = [
       structlog.stdlib.ProcessorFormatter.remove_processors_meta,
    ]
    if sys.stdin.isatty() and os.environ.get("APP_LOGFMT") is None:
        formatter_processors.extend([
            structlog.dev.ConsoleRenderer(),  # type: ignore
        ])
    else:
        formatter_processors.extend([
            structlog.processors.JSONRenderer(), # type: ignore
        ])

    formatter = structlog.stdlib.ProcessorFormatter(
        # These run ONLY on `logging` entries that do NOT originate within
        # structlog.
        foreign_pre_chain=shared_processors,
        # These run on ALL entries after the pre_chain is done.
        processors=formatter_processors,
    )

    handler = logging.StreamHandler()
    # Use OUR `ProcessorFormatter` to format all `logging` entries.
    handler.setFormatter(formatter)
    log_level = os.environ.get("APP_LOG_LEVEL", "DEBUG")
    if log_level.isdigit():
        log_level = int(log_level)
    logging.captureWarnings(True)
    logging.basicConfig(
        handlers=[handler],
        level=log_level,
    )
    # logging.getLogger("pika").setLevel(logging.WARNING)
    # logging.getLogger("urllib3").setLevel(logging.WARNING)


    logger = structlog.stdlib.get_logger()
    patch_unhandled_exceptions(logger)
    # patch_warnings(logger)
    patch_threading()
