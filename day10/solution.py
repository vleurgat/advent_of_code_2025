import random

class Solution:

    class Machine:

        def __init__(self):
            self.target_lights = []
            self.buttons = []
            self.target_joltage = []
            self.min_pushes = -1
            self.seqs = {}
            self.inc = 0


        def __str__(self) -> str:
            return f"\n****\ntarget={self.target_lights}\nbuttons={self.buttons}\njoltage={self.target_joltage}"
        

        def push(self, bi: int, lights: list):
            #print(f"  >> machine push {bi}; in_lights={lights}")
            if bi < 0 or bi >= len(self.buttons):
                raise Exception(f"cannot push button #{bi} for buttons={self.buttons}")
            button = self.buttons[bi]
            new_lights = lights.copy()
            for li in button:
                if li < 0 or li >= len(lights):
                    raise Exception(f"cannot modify light #{li} for lights={lights}")
                new_lights[li] = not new_lights[li]
            #print(f"  >> machine push {bi}; out_lights={new_lights}")
            return new_lights
        

        def pushj(self, bi: int, joltage: list):
            #print(f"  >> machine push {bi}; in_joltage={joltage}")
            if bi < 0 or bi >= len(self.buttons):
                raise Exception(f"cannot push button #{bi} for buttons={self.buttons}")
            button = self.buttons[bi]
            new_joltage = joltage.copy()
            for ji in button:
                if ji < 0 or ji >= len(joltage):
                    raise Exception(f"cannot modify joltage #{ji} for lights={joltage}")
                new_joltage[ji] += 1
            #print(f"  >> machine push {bi}; out_joltage={new_joltage}")
            return new_joltage
        

        def add_seq(self, seq: list):
            ss = self.seqs
            for s in seq:
                if not s in ss:
                    ss[s] = {}
                ss = ss[s]


        def is_existing_seq(self, seq: list):
            ss = self.seqs
            for s in seq:
                if not s in ss:
                    return False
                ss = ss[s]
            return True


        def is_over_joltage(self, joltage):
            for ji in range(len(joltage)):
                if joltage[ji] > self.target_joltage[ji]:
                    return True
            return False
        

        def starting_lights(self):
            return [False] * len(self.target_lights)
        

        def starting_joltage(self):
            return [0] * len(self.target_joltage)


    def __init__(self):
        self.machines = []
        self.max_num_pushes = 20


    def pushes(self, machine : Machine, lights: list, seq: list):
        num_pushes = len(seq)
        if machine.inc % 100000 == 0:
            print(f"loop#{machine.inc} pushes: lights={lights}; num={num_pushes}; seq={seq}")
        machine.inc += 1
        if lights == machine.target_lights:
            #print(f"  lights == target - return {num_pushes}")
            if machine.min_pushes == -1 or num_pushes < machine.min_pushes:
                machine.min_pushes = num_pushes
            print(f"found solution for num={num_pushes} and seq={seq}")
            return num_pushes
        if num_pushes >= self.max_num_pushes:
            #print(f"max: num={num_pushes} >= {self.max_num_pushes}; seq={seq}")
            #input("hit RETURN")
            return -1
        if num_pushes >= machine.min_pushes and machine.min_pushes != -1:
            #print(f"min: num={num_pushes} >= {machine.min_pushes}; seq={seq}")
            return -1
        min_num_pushes = -1
        for bi in range(len(machine.buttons)):
            if num_pushes > 1 and seq[num_pushes-1] == bi:
                # don't press the same button twice
                continue
            #print(f"  try pushing button {bi}")
            new_lights = machine.push(bi, lights)
            np = self.pushes(machine, new_lights, seq + [bi])
            if np != -1 and (np < min_num_pushes or min_num_pushes == -1):
                min_num_pushes = np
            #print(f"  min_num_pushes now {min_num_pushes}")
        #print(f"  after {bi} button pushes return {min_num_pushes}")
        #input("hit RETURN")
        return min_num_pushes


    def pushesj(self, machine : Machine, joltage: list, seq: list):
        num_pushes = len(seq)
        if machine.inc % 1000000 == 0:
            print(f"  pushes loop#{machine.inc} pushes: joltage={joltage}; num={num_pushes}; min={machine.min_pushes}; seq={seq}")
        machine.inc += 1
        if joltage == machine.target_joltage:
            #print(f"  joltage == target - return {num_pushes}")
            if machine.min_pushes == -1 or num_pushes < machine.min_pushes:
                machine.min_pushes = num_pushes
                #print(f"found new min solution for num={num_pushes} and seq={seq}")
            return num_pushes
        if machine.is_over_joltage(joltage):
            return -1
        if num_pushes >= self.max_num_pushes:
            #print(f"max: num={num_pushes} >= {self.max_num_pushes}; seq={seq}")
            #input("hit RETURN")
            return -1
        if num_pushes >= machine.min_pushes and machine.min_pushes != -1:
            #print(f"min: num={num_pushes} >= {machine.min_pushes}; seq={seq}")
            return -1
        min_num_pushes = -1
        for bi in range(len(machine.buttons)):
            #print(f"  try pushing button {bi}")
            new_joltage = machine.pushj(bi, joltage)
            np = self.pushesj(machine, new_joltage, seq + [bi])
            if np != -1 and (np < min_num_pushes or min_num_pushes == -1):
                min_num_pushes = np
            #print(f"  min_num_pushes now {min_num_pushes}")
        #print(f"  after {bi} button pushes return {min_num_pushes}")
        #input("hit RETURN")
        return min_num_pushes


    def read_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                machine = self.Machine()
                elements = line.strip().split()
                lights_str = elements[0]
                lights_str = lights_str[1:len(lights_str)-1]
                for light in lights_str:
                    if light == '#':
                        machine.target_lights.append(True)
                    else:
                        machine.target_lights.append(False)
                jolts_str = elements[len(elements)-1]
                machine.target_joltage = list(map(int, jolts_str[1:len(jolts_str)-1].split(',')))
                for button_str in elements[1:len(elements)-1]:
                    button_str = button_str[1:len(button_str)-1]
                    machine.buttons.append(list(map(int, button_str.split(','))))
                self.machines.append(machine)


    def solve(self, filename):
        self.read_file(filename)
        total = 0
        i = 1
        for machine in self.machines:
            min_pushes = self.pushesj(machine, machine.starting_joltage(), [])
            total += min_pushes
            print(f"{i} min pushes is {min_pushes} after {machine.inc} loops")
            i += 1
        print(f"total min pushes is {total}")


if __name__ == "__main__":
    solution = Solution()
    solution.solve('test2.txt')
