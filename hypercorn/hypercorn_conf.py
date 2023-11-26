import multiprocessing
import os

host = os.environ.get("HOST", "0.0.0.0")
port = os.environ.get("PORT", 8000)
bind_env = os.environ.get("BIND", None)

use_bind = bind_env if bind_env else f"{host}:{port}"
workers_per_core = os.getenv("WORKERS_PER_CORE", 1)
max_workers = os.getenv("MAX_WORKERS", None)
if max_workers:
    max_workers = int(max_workers)

cores = multiprocessing.cpu_count()
workers = max(min(max_workers, cores * workers_per_core), 1)
