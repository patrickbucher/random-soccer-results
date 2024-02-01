#!/usr/bin/env python3

import os
import sys


def read_lines(path):
    with open(path, 'r') as f:
        content = f.read().strip()
        return content.split('\n')


def generate_results(teams_dir, results_dir):
    team_files = os.listdir(teams_dir)
    teams_by_file = {f: read_lines(os.path.join(teams_dir, f))
                     for f in team_files}
    for file, teams in teams_by_file.items():
        n = len(teams)
        strength = map(lambda x: 1 + x / n, reversed(range(0, n)))
        print(list(zip(teams, strength)))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'usage: {argv[0]} TEAM-DIRECTORY RESULT-DIRECTORY')
        sys.exit(1)
    generate_results(sys.argv[1], sys.argv[2])
