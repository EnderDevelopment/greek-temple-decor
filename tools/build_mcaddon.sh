#!/usr/bin/env bash
# Build the Greek Temple Decorations Bedrock addon.
# Requires Python 3 and Pillow (pip install Pillow).
cd "$(dirname "$0")/.."
python3 tools/build_addon.py
