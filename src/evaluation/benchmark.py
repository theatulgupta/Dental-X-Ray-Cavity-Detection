"""
Benchmark utility (disabled).

This file previously contained a small utility to benchmark YOLO model
inference time on a directory of images. The project no longer invokes
this module automatically. To avoid accidental runs, the implementation
has been replaced with a short message.

If you want to re-enable benchmarking, consider moving this into
`tools/benchmark.py` or re-implementing with proper CI wiring.
"""
import sys

sys.exit("benchmark.py has been disabled. If you need this utility, restore it from version control or create a tools/benchmark.py script.")
