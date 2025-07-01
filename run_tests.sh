#!/bin/bash
set -e
pip install --quiet -r requirements.txt >/dev/null 2>&1 || true
pip install --quiet pytest reportlab >/dev/null
pytest -q
