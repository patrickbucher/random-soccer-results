#!/usr/bin/env python3

import sys


def generate_results(teams_dir, results_dir):
    print(teams_dir, results_dir)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'usage: {argv[0]} TEAM-DIRECTORY RESULT-DIRECTORY')
        sys.exit(1)
    generate_results(sys.argv[1], sys.argv[2])
