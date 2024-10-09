#!/usr/bin/env python3

import json
import os
import random
import shutil
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
    rounds = []
    for i in range(n-1):
        whole = [head] + tail
        pairs = list(zip(whole[:m], whole[m:]))
        tail = tail[1:] + [tail[0]]
        rounds.append(pairs)
    return rounds


def reverse(rounds):
    return list(map(lambda ps: [tuple(reversed(p)) for p in ps], rounds))


def rand_goals(strength):
    number = int(random.normalvariate(mu=strength, sigma=1.5))
    if number < 0:
        number = 0
    return number


def generate_results(teams_dir, results_dir, as_json=False):
    if not os.path.exists(results_dir):
        os.mkdir(out_dir)

    team_files = os.listdir(teams_dir)
    teams_by_file = {f: read_lines(os.path.join(teams_dir, f))
                     for f in team_files}

    for file, teams in teams_by_file.items():
        out_dir = os.path.join(results_dir, file.split('.')[0])
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        os.mkdir(out_dir)

        n = len(teams)
        strength = map(lambda x: 1 + x / n, reversed(range(0, n)))
        team_strengths = dict(zip(teams, strength))
        first_leg = pair_up(teams)
        second_leg = reverse(first_leg)
        rounds = first_leg + second_leg

        assert len(rounds) == 2 * (n - 1)
        assert all(map(lambda r: len(set(r)) == len(r), rounds))

        def to_lines(results):
            lines = []
            for r in results:
                home, away = r[0], r[1]
                home_s, away_s = team_strengths[home], team_strengths[away]
                home_g, away_g = rand_goals(home_s), rand_goals(away_s)
                if as_json:
                    lines.append({'homeTeam': home,
                                  'awayTeam': away,
                                  'homeGoals': home_g,
                                  'awayGoals': away_g})
                else:
                    lines.append('%s %d:%d %s\n' %
                                 (home, home_g, away_g, away))
            return lines

        for (i, r) in enumerate(rounds):
            round_file = os.path.join(out_dir, f'day{i+1:02d}')
            if as_json:
                round_file += '.json'
            else:
                round_file += '.txt'
            lines = to_lines(r)
            with open(round_file, 'w') as f:
                if as_json:
                    f.write(json.dumps(lines, indent=2, ensure_ascii=False))
                else:
                    for line in lines:
                        f.write(line)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'usage: {argv[0]} TEAM-DIRECTORY RESULT-DIRECTORY')
        sys.exit(1)
    generate_results(sys.argv[1], sys.argv[2], as_json=True)
