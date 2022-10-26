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

class Layer:
    def __init__(self):
        self.text_segments = []
        self.lines = None

    def write(self, text):
        self.text_segments.append(text)
        self.lines = None

    def linify(self):
        text = ''.join(self.text_segments)
        self.lines = text.splitlines()

    def overlay(self, foreground):
        if not self.lines: self.linify()
        if not foreground.lines: foreground.linify()
        new_lines = []
        for b, f in zip(self.lines, foreground.lines):
            segments = []
            for b_c, f_c in zip(b, f):
                if f_c == ' ':
                    segments.append(b_c)
                else:
                    segments.append(f_c)
            if len(b) > len(f):
                longer = b
                shorter = f
            else:
                longer = f
                shorter = b
            segments.append(longer[len(shorter):])
            new_lines.append(''.join(segments))
        self.lines = new_lines

    def to_file(self, path):
        if not self.lines: self.linify()
        with open(path, 'w') as file:
            for line in self.lines:
                file.write(line)
                file.write('\n')

    def print(self):
        if not self.lines: self.linify()
        for line in self.lines:
            print(line)

f = Layer()
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
            if len(lines[-1]) > stride - 3:
                f.write('\n')
                f.write(' '*(actors[fro]))
                lines[-1] = ' '*(stride//2)
                f.write(lines[-1])
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
f.linify()

b = Layer()
for _ in range(len(f.lines)):
    for _ in actors:
        b.write('.')
        b.write(' '*(stride-1))
    b.write('\n')

b.overlay(f)
b.to_file(args.output)
