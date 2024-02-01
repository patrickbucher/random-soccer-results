#!/usr/bin/env python3

import os
import random
import sys


def read_lines(path):
    with open(path, 'r') as f:
        content = f.read().strip()
        return content.split('\n')


def pair_up(teams):
    n = len(teams)
    assert n % 2 == 0
    m = int(n / 2)
    head = teams[0]
    tail = teams[1:]
    pairings = []
    for i in range(n):
        whole = [head] + tail
        pairs = list(zip(whole[:m], whole[m:]))
        tail = tail[1:] + [tail[0]]
        pairings.append(pairs)
    return pairings


def reverse_pairs(pairings):
    reversed_pairs = []
    for pairing in pairings:
        reversed_pairs.append(list(reversed(pairing)))
    return reversed_pairs


def rand_goals(strength):
    number = int(random.normalvariate(mu=strength, sigma=1.0))
    if number < 0:
        number = 0
    return number


def generate_results(teams_dir, results_dir):
    team_files = os.listdir(teams_dir)
    teams_by_file = {f: read_lines(os.path.join(teams_dir, f))
                     for f in team_files}
    for file, teams in teams_by_file.items():
        n = len(teams)
        strength = map(lambda x: 1 + x / n, reversed(range(0, n)))
        team_strengths = dict(zip(teams, strength))
        out_dir = os.path.join(results_dir, file.split('.')[0])
        first_leg = pair_up(teams)
        second_leg = reverse_pairs(first_leg)
        rounds = first_leg + second_leg

        assert len(rounds) == 2 * n
        assert all(map(lambda r: len(set(r)) == len(r), rounds))
        for r in rounds:
            for p in r:
                home, away = p[0], p[1]
                home_s, away_s = team_strengths[home], team_strengths[away]
                home_g, away_g = rand_goals(home_s), rand_goals(away_s)
                print('%s %d:%d %s' % (home, home_g, away_g, away))
                # TODO: output in individual round files


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'usage: {argv[0]} TEAM-DIRECTORY RESULT-DIRECTORY')
        sys.exit(1)
    generate_results(sys.argv[1], sys.argv[2])
