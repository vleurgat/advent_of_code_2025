
class Solution:

    def __init__(self):
        self.banks = []
        self.batteries = 0


    def read_file(self, filename: str):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                self.banks.append(list(map(int, line.strip())))


    def find_largest(self, bank: list) -> int:
        l = len(bank)
        digits = []
        start = 0
        #print(f"\nfind largest for bank {bank}")
        for i in range(self.batteries):
            end = l - (self.batteries - 1 - i)
            sorted = bank[start:end]
            sorted.sort(reverse=True)
            #print(f"loop {i} start is {start} end is {end}, so sorted is {sorted}")
            digit = sorted[0]
            digits.append(digit)
            start = bank.index(digit, start) + 1
            #print(f"item {i} is {digit} and next start is {start}")
        res = int("".join(list(map(str, digits))))
        #print(f"result is {res}")
        return res

 
    def solve(self, filename):
        self.read_file(filename)
        #print(f"banks are: {self.banks}")
        total = 0
        for bank in self.banks:
            total += self.find_largest(bank)
        print(f"total is {total}")


if __name__ == "__main__":
    filename = "input.txt"

    solution = Solution()
    solution.batteries = 12
    solution.solve(filename)
