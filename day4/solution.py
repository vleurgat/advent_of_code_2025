
class Solution:

    def __init__(self):
        self.grid = []
        self.removed = {}


    def read_file(self, filename: str):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                self.grid.append(line.strip())


    def inbounds(self, x, y) -> bool:
        return x >= 0 and x < len(self.grid[0]) and y >= 0 and y < len(self.grid)


    def was_removed(self, x, y) -> bool:
        if x in self.removed:
           return y in self.removed[x]
        return False


    def observed_to_removed(self, observed):
        for x in observed:
            if not x in self.removed:
                self.removed[x] = []
            for y in observed[x]:
                if not y in self.removed[x]:
                    self.removed[x].append(y)


    def count_adjacent(self, x, y) -> int:
        count = 0
        count += 1 if self.inbounds(x, y+1) and self.grid[y+1][x] == '@' and not self.was_removed(x, y+1) else 0
        count += 1 if self.inbounds(x, y-1) and self.grid[y-1][x] == '@' and not self.was_removed(x, y-1) else 0
        count += 1 if self.inbounds(x+1, y) and self.grid[y][x+1] == '@' and not self.was_removed(x+1, y) else 0
        count += 1 if self.inbounds(x-1, y) and self.grid[y][x-1] == '@' and not self.was_removed(x-1, y) else 0
        count += 1 if self.inbounds(x+1, y+1) and self.grid[y+1][x+1] == '@' and not self.was_removed(x+1, y+1) else 0
        count += 1 if self.inbounds(x-1, y-1) and self.grid[y-1][x-1] == '@' and not self.was_removed(x-1, y-1) else 0
        count += 1 if self.inbounds(x+1, y-1) and self.grid[y-1][x+1] == '@' and not self.was_removed(x+1, y-1) else 0
        count += 1 if self.inbounds(x-1, y+1) and self.grid[y+1][x-1] == '@' and not self.was_removed(x-1, y+1) else 0
        return count


    def walk(self) -> int:
        count = 0
        observed = {}
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                c = self.grid[y][x]
                if c == '@' and not self.was_removed(x, y):
                    adj = self.count_adjacent(x, y)
                    #print(f"@ [{x},{y}] c={c} adj={adj}")
                    if adj < 4:
                        #print("  c is @ and adj < 4")
                        if not x in observed:
                            observed[x] = []
                        if not y in observed[x]:
                            observed[x].append(y)
                            count += 1
                            #print(f"    and not observed before - count is now {count}")
        self.observed_to_removed(observed)
        return count

 
    def solve(self, filename):
        self.read_file(filename)
        #print(f"grid is: {self.grid}")
        loop_count = 0
        removed = 0
        total = 0
        while loop_count == 0 or removed != 0:
            loop_count += 1
            removed = self.walk()
            print(f"{loop_count}: removed {removed}")
            total += removed
        print(f"total is {total}")


if __name__ == "__main__":
    filename = "input.txt"

    solution = Solution()
    solution.solve(filename)
