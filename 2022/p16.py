"""
AOC 2022 -- Jour 16
S. Hoarau
"""

import re
from puzzle import Puzzle

INF = float('inf')

STATES = 'CLOSED', 'OPENED'

class Valve:

    def __init__(self, pid, flow_rate, neighbors_pid):
        self.id = pid
        self.rate = flow_rate
        self.neighbors = neighbors_pid

    def __repr__(self):
        return f'Valve({self.id}, {self.rate}, {self.neighbors})'



class Configuration:

    def __init__(self, with_elephant=False):
        self.valves = None
        self.total_time = 26 if with_elephant else 30
        self.remaining_time = self.total_time 
        self.opened = {}
        self.position = 'AA'
        self.with_elephant = with_elephant
        if with_elephant:
            self.position_two = 'AA'

    def __repr__(self):
        valve_id = self.position
        s = f'My position: {valve_id}-{STATES[valve_id in self.opened]} '
        if self.with_elephant and self.position_two != self.position:
            s += f'Elephant: {self.position_two}-{STATES[self.position_two in self.opened]} '
        for pid in self.valves:
            s += f'{pid}-{STATES[pid in self.opened]} '
        s += f'Score: {self.release()}'
        return s

    def __eq__(self, cfg):
        return self.remaining_time == cfg.remaining_time and self.position == cfg.position and self.opened == cfg.opened and\
            (not self.with_elephant or self.position_two == cfg.position_two)

    def copy(self):
        cfg = Configuration()
        cfg.valves = self.valves
        cfg.remaining_time = self.remaining_time
        cfg.opened = self.opened.copy()
        cfg.position = self.position
        cfg.with_elephant = self.with_elephant
        if cfg.with_elephant:
            cfg.position_two = self.position_two
        return cfg

    def final(self):
        return self.remaining_time == 0

    def release(self):
        return sum(self.opened.values())

    def score(self):
        return self.release() / (self.total_time - self.remaining_time + 1)

    def goto(self, pid, elephant=False):
        if elephant:
            self.position_two = pid
        else:
            self.position = pid
            self.remaining_time -= 1

    def open(self, elephant=False):
        if elephant:
            self.opened[self.position_two] = (self.remaining_time - 1) * self.valves[self.position_two].rate
        else:
            self.remaining_time -= 1
            self.opened[self.position] = self.remaining_time * self.valves[self.position].rate

    def neighbors(self):
        cfgs = []
        if self.with_elephant:
            if self.position_two not in self.opened:
                cfg = self.copy()
                cfg.open(elephant=True)
                cfgs.append(cfg)
            for pid in self.valves[self.position_two].neighbors:
                cfg = self.copy()
                cfg.goto(pid, elephant=True)
                cfgs.append(cfg)

            new_cfgs = []
            for cfg in cfgs:
                if self.position not in self.opened:
                    cfg_bis = cfg.copy()
                    cfg_bis.open()
                    new_cfgs.append(cfg_bis)
                for pid in self.valves[self.position].neighbors:
                    cfg_bis = cfg.copy()
                    cfg_bis.goto(pid)
                    new_cfgs.append(cfg_bis)
            return new_cfgs
        else:
            if self.position not in self.opened:
                cfg = self.copy()
                cfg.open()
                cfgs.append(cfg)
            for pid in self.valves[self.position].neighbors:
                cfg = self.copy()
                cfg.goto(pid)
                cfgs.append(cfg_bis)
            return cfgs



class P16(Puzzle):

    REGEX1 = re.compile(r'[A-Z]{2}')
    REGEX2 = re.compile(r'\d+')

    def __init__(self, part):
        Puzzle.__init__(self, 16, part)
        self.initial = None
        self.valves = {}

    def aff(self):
        for valve in self.valves.values():
            print(valve)

    def beam_search(self, n):
        releases = set()
        generation = [self.initial]
        while len(generation) > 0:
            next_gen = []
            for cfg in generation:
                if cfg.final():
                    releases.add(cfg.release())
                else:
                    next_gen.extend(new_cfg for new_cfg in cfg.neighbors() if new_cfg not in next_gen)
                    next_gen.sort(key=Configuration.score, reverse=True)
            generation = [next_gen[i] for i in range(min(n, len(next_gen)))]
        self.solution = max(releases)

    def load_datas(self, filename):
        with open(filename) as datas:
            for data in datas.readlines():
                node, *neighbors = P16.REGEX1.findall(data)
                flow_rate = P16.REGEX2.findall(data)
                self.valves[node] = Valve(node, int(flow_rate[0]), neighbors)
            self.initial = Configuration(self.part!=0)
            self.initial.valves = self.valves

    def reset(self):
        self.valves = {}

    def solve(self, filename, *args):
        self.reset()
        self.load_datas(filename)
        self.beam_search(4096)

# -- MAIN

# p_one = P16(0)
# p_one.test()
# print(p_one)
# p_one.validate()
# print(p_one)

p_two = P16(1)
# p_two.test()
# print(p_two)
p_two.validate()
print(p_two)

