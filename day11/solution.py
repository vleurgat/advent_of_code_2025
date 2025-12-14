from collections import deque


class Solution1:

    def __init__(self):
        self.devices = {}
        self.complete_paths = []


    def read_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                split = line.split(':')
                device = split[0]
                outputs = split[1].strip().split()
                self.devices[device] = outputs


    def walk(self):
        context = deque()
        path = []
        path.append('you')
        context.append(path)
        while len(context) > 0:
            path = context.popleft()
            current = path[len(path)-1]
            if current == 'out':
                self.complete_paths.append(path)
            else:
                for next in self.devices[current]:
                    next_path = path + [next]
                    context.append(next_path)


    def solve(self, filename):
        self.read_file(filename)
        self.walk()
        print(f"number of complete paths is {len(self.complete_paths)}")



class Solution2:

    def __init__(self):
        self.devices = {}
        self.cache = {}


    def read_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                split = line.split(':')
                device = split[0]
                outputs = split[1].strip().split()
                self.devices[device] = outputs


    def walk(self, node, seen_dac, seen_fft):
        if node == 'out':
            if seen_fft and seen_dac:
                return 1
            return 0

        if (node, seen_dac, seen_fft) in self.cache:
            return self.cache[(node, seen_dac, seen_fft)]

        is_dac = node == 'dac'
        is_fft = node == 'fft'

        ret = 0
        for next in self.devices[node]:
            ret += self.walk(next, seen_dac or is_dac, seen_fft or is_fft)

        self.cache[(node, seen_dac, seen_fft)] = ret
        return ret


    def solve(self, filename):
        self.read_file(filename)
        total = self.walk('svr', False, False)
        print(f"complete paths are {total}")


if __name__ == "__main__":
    solution = Solution1()
    solution.solve('input.txt')
