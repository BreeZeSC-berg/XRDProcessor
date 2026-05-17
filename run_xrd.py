#!/usr/bin/env python
"""Launcher script for XRD Analyzer."""
import sys
import os

# Ensure the project directory is in the path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from xrd_analyzer import main

if __name__ == "__main__":
    main()
