import sys
import os

# Get the directory that contains src
src_dir = os.path.dirname(os.path.abspath(__file__))

# Add src_dir to the Python path
sys.path.insert(0, src_dir)