
class Solution:

    def __init__(self):
        self.pos = 50
        self.inputs = []
        self.at_zero = 0


    def read_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                lr = line[0]
                n = int(line[1:])
                self.inputs.append([lr, n])


    def rotate(self, n, d):
        rl = f'R{n}' if d == 1 else f'L{n}'
        #print(f"{rl}: pos is {self.pos}")

        new_pos = self.pos + (d * n)
        inc = int(abs(new_pos) / 100)
        if new_pos <= 0 and self.pos > 0:
            inc += 1

        self.at_zero += inc
        self.pos = new_pos % 100
        #print(f"after {rl}: pos is {self.pos} passing or at zero {inc} times")


    def solve(self, filename):
        self.read_file(filename)
        #print(f"inputs are: {self.inputs}")
        for input in self.inputs:
            if input[0] == 'R':
                self.rotate(input[1], 1)
            else:
                self.rotate(input[1], -1)
        print(f"was at zero {self.at_zero} times")


if __name__ == "__main__":
    filename = "input.txt"

    solution = Solution()
    solution.solve(filename)
