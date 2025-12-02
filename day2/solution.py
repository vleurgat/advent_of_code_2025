
class Solution:

    def __init__(self):
        self.ranges = []
        self.invalids = []


    def read_file(self, filename: str):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                _ranges = line.split(',')
                for _range in _ranges:
                    self.ranges.append(list(map(int, _range.split('-'))))


    def is_invalid0(self, n: int) -> bool:
        s = str(n)
        l = len(s)
        if l % 2 == 0:
            mid = int(l / 2)
            return s[0:mid] == s[mid:]
        return False


    def is_invalid(self, n: int) -> bool:
        s = str(n)
        len_s = len(s)
        len_match = 1
        for _ in range(int(len_s / 2)):
            mult = int(len_s / len_match)
            if s[0:len_match] * mult == s:
                return True
            len_match += 1
        return False
        

    def find_invalids_in_range(self, _range: list):
        #print(f"range to test is {_range}")
        for n in range(_range[0], _range[1]+1):
            if self.is_invalid(n):
                #print(f"found invalid {n}")
                self.invalids.append(n)
 

    def solve(self, filename):
        self.read_file(filename)
        print(f"ranges are: {self.ranges}")
        for _range in self.ranges:
            self.find_invalids_in_range(_range)
        print(f"total of invalid ids is: {sum(self.invalids)}")


    def _test(self):
        print(f"2222: {self.is_invalid(2222)}")
        print(f"22222: {self.is_invalid(22222)}")
        print(f"1: {self.is_invalid(1)}")
        print(f"404404: {self.is_invalid(404404)}")
        print(f"333: {self.is_invalid(333)}")
        print(f"404400: {self.is_invalid(404400)}")


if __name__ == "__main__":
    filename = "input.txt"

    solution = Solution()
    solution._test()
    solution.solve(filename)
