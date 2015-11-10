#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 Eremin V. Leonid (leremin@outlook.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import sys
import os
from os import path

def calculate_lines_count(root_path, empty_lines, empty_files, excludes, extensions):
    for root, subdirs, files in os.walk(root_path):
        for file_name in files:
            full_path = path.join(root, file_name)
            
            if not any(file_name.endswith('.' + e) for e in extensions):
                continue
            
            if any(e in full_path for e in excludes):
                continue
            
            with open(full_path, 'rb') as f:
                short_path = path.relpath(full_path, root_path)

                lines = list(line for line in (l.strip() for l in f) if line) if not empty_lines else f
                lines_count = sum(1 for line in lines)
                
                if empty_lines or lines_count > 0:
                    yield (short_path, lines_count)
        
def print_lines_count(counts, reverse, count):
    sorted_counts = sorted(counts, key = lambda count: count[1], reverse = reverse)
    if count is not None and count > 0:
        sorted_counts = sorted_counts[:count]
    elif count is not None and count < 0:
        sorted_counts = sorted_counts[count:]
            
    for c in sorted_counts:
        print('%s: %d' % (c[0], c[1]))
    
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help = 'root dir for finding files', required = True)
    parser.add_argument('-i', '--include', help = 'files extensions for calculation lines', nargs = '+', required = True)
    parser.add_argument('-x', '--exclude', help = 'patterns of files path to exclude from calculation lines', nargs = '+', default = '')
    parser.add_argument('-e', '--empty_lines', help = 'calculation empty lines in file', action = 'store_const', const = True, default = False)
    parser.add_argument('-E', '--empty_files', help = 'show empty files', action = 'store_const', const = True, default = False)
    parser.add_argument('-r', '--reverse', help = 'reverse output', action = 'store_const', const = True, default = False)
    parser.add_argument('-n', '--count', help = 'count of lines in output', default = None, type = int)
    return parser
                
if __name__ == '__main__':
    args = create_parser().parse_args(sys.argv[1:])
    root_dir = path.abspath(args.path)
    reverse = args.reverse
    empty_lines = args.empty_lines
    empty_files = args.empty_files
    includes = args.include
    excludes = args.exclude
    count = args.count

    counts = calculate_lines_count(root_dir, empty_lines, empty_files, excludes, includes)
    print_lines_count(counts, reverse, count)