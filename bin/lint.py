#!/usr/bin/env python3

from pathlib import Path
import pylint
import pylint.lint

py_files = map(str, Path('.').glob('*.py'))
pylint.lint.Run(['bin', 'lib', 'web', *py_files])
