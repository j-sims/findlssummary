import os
import re
import sys
import argparse
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

# Regular expression to extract file size and path safely
FIND_LS_REGEX = re.compile(r"^\s*\d+\s+\d+\s+(\S+)\s+\d+\s+\S+\s+\S+\s+(\d+)\s+\w+\s+\d+\s+[\d:]+\s+(.+)$")

def process_line(line):
    """Parse a single line of the find output and return relevant data."""
    match = FIND_LS_REGEX.match(line)
    if not match:
        return None  # Skip malformed lines
    
    file_type, size, path = match.groups()
    size = int(size)  # Convert to integer
    is_dir = file_type.startswith('d')  # Check if it's a directory
    
    return (path, size, is_dir)

def format_size(size):
    """Format bytes into a human-readable format without external dependencies."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def process_input(input_stream, workers=4):
    """Processes the input stream using multiprocessing."""
    dir_summary = defaultdict(lambda: {'files': 0, 'dirs': 0, 'size': 0})
    
    with ProcessPoolExecutor(max_workers=workers) as executor:
        for result in executor.map(process_line, input_stream):
            if result is None:
                continue
            path, size, is_dir = result

            dir_summary[path]['size'] += size
            if is_dir:
                dir_summary[path]['dirs'] += 1
            else:
                dir_summary[path]['files'] += 1
            
            # Update parent directories iteratively (avoid recursion)
            parent = path
            while '/' in parent:
                parent = parent.rsplit('/', 1)[0]  # Faster than os.path.dirname()
                dir_summary[parent]['size'] += size
                if is_dir:
                    dir_summary[parent]['dirs'] += 1
                else:
                    dir_summary[parent]['files'] += 1
    
    return dir_summary

def print_summary(dir_summary):
    """Prints the directory statistics in a human-readable format."""
    print(f"{'Directory':<40} {'Files':<10} {'Dirs':<10} {'Size':<15}")
    print("=" * 80)
    for directory, stats in sorted(dir_summary.items()):
        print(f"{directory:<40} {stats['files']:<10} {stats['dirs']:<10} {format_size(stats['size']):<15}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse 'find -ls' output and summarize disk usage.")
    parser.add_argument('-f', '--file', type=str, help="Input file containing 'find -ls' output. If not provided, reads from stdin.")
    args = parser.parse_args()
    
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as file:
            summary = process_input(file, workers=8)
    else:
        summary = process_input(sys.stdin, workers=8)
    
    print_summary(summary)
