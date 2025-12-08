
class Solution:

    def __init__(self):
        self.grid = []
        self.start_x = 0
        self.start_y = 0
        self.cache = {}


    def read_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                self.grid.append(line.strip())


    def find_start(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                c = self.grid[y][x]
                if c == 'S':
                    self.start_x = x
                    self.start_y = y + 1
                    print(f"starting pos is [{x},{y}]")
                    return


    def walk(self, x, y) -> int:
        if (x, y) in self.cache:
            return self.cache[(x, y)]
        
        c = self.grid[y][x]
        ret = 0
        if y == (len(self.grid) - 1):
            ret = 1
        elif c == '.':
            ret = self.walk(x, y+1)
        elif c == '^':
            ret = self.walk(x-1, y) + self.walk(x+1, y)

        self.cache[(x, y)] = ret
        return ret
    

    def solve(self, filename):
        self.read_file(filename)
        self.find_start()
        total = self.walk(self.start_x, self.start_y)
        print(f"total is {total}")


if __name__ == "__main__":
    solution = Solution()
    solution.solve('input.txt')
