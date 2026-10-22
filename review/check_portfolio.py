"""Compatibility entry point for the current portfolio browser checks."""
import os
from pathlib import Path
import runpy
os.environ.setdefault('PORTFOLIO_TEST_URL', 'http://127.0.0.1:8080')
runpy.run_path(str(Path(__file__).with_name('check_expressive.py')), run_name='__main__')
