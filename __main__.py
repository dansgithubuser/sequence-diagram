import argparse
import textwrap

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('--output', '-o', default='sequence-diagram.txt')
args = parser.parse_args()

with open(args.input) as f: lines = f.readlines()

actors = set()
actions = []
for line in lines:
    who, what = line.split(':')
    who = who.split(' to ')
    what = what.strip()
    if len(who) > 2: raise Exception('invalid syntax')
    for i in who: actors.add(i)
    actions.append((who, what))

stride = min(max(max(len(i) for i in actors), max(len(i[1]) for i in actions)) + 4, 20)
actors = {v: i*stride for i, v in enumerate(sorted(list(actors)))}

with open(args.output, 'w') as f:
    for actor in actors:
        f.write('{{:{}}}'.format(stride).format(actor))
    f.write('\n\n')
    for who, what in actions:
        if len(who) == 1:
            who = who[0]
            for line in textwrap.wrap('['+what+']', width=stride):
                f.write(' '*actors[who])
                f.write(line)
                f.write('\n')
        elif len(who) == 2:
            fro, to = who
            if fro < to:
                lines = textwrap.wrap(what, width=stride)
                for i, line in enumerate(lines):
                    f.write(' '*actors[fro])
                    f.write(line)
                    if i != len(lines) - 1: f.write('\n')
                f.write('-'*(actors[to]-actors[fro]-1-len(lines[-1])))
                f.write('>')
                f.write('\n')
            else:
                lines = textwrap.wrap(what, width=stride)
                for i, line in enumerate(lines):
                    if i == len(lines) - 1:
                        f.write(' '*(actors[to]+1))
                        f.write('<')
                        f.write('-'*(actors[fro]-actors[to]-2))
                    else:
                        f.write(' '*actors[fro])
                    f.write(line)
                    f.write('\n')
        f.write('\n')
