
class Solution:

    def __init__(self):
        self.problems = []


    def read_file0(self, filename: str):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                i = 0
                for col in line.split():
                    if len(self.problems) <= i:
                        self.problems.append([col])
                    else:
                        self.problems[i].append(col)
                    i += 1


    def read_file(self, filename: str):
        with open(filename) as f:
            lines = f.readlines()
            last_line = lines[len(lines)-1]
            cols = []
            for i in range(len(last_line)):
                if last_line[i] != ' ' and last_line[i] != '\n':
                    cols.append(i)

            for line in lines:
                for i in range(len(cols)):
                    word = ""
                    if i < (len(cols)-1):
                        word = line[cols[i]:cols[i+1]-1]
                    else:
                        word = line[cols[i]:len(line)-1]
                    if len(self.problems) <= i:
                        self.problems.append([word])
                    else:
                        self.problems[i].append(word)


    def calculate0(self):
        total = 0
        for problem in self.problems:
            j = len(problem) - 1
            if problem[j] == '*':
                res = 1
                for i in range(len(problem) - 1):
                    res *= int(problem[i])
            elif problem[j] == '+':
                res = 0
                for i in range(len(problem) - 1):
                    res += int(problem[i])
            else:  
                raise Exception(f"unexpected problem, unknown operator: {problem}")
            total += res
        return total


    def operation(self, op, nums):
        res = 0
        if '+' in op:
            res = 0
            for num in nums:
                res += int(num.strip())
        elif '*' in op:
            res = 1
            for num in nums:
                res *= int(num.strip())
        else:  
            raise Exception(f"unexpected problem, unknown operator: {op}")
        #print(f"result of {op} on {nums} is {res}")
        return res


    def calculate(self):
        total = 0
        for problem in self.problems:
            #print(f"got problem {problem}")
            cols = []
            for row in problem:
                if '*' in row or '+' in row:
                    #print(f"perform operation {row} on {cols}")
                    total += self.operation(row, cols)
                    break
                #print(f"for row {row}:")
                i = 0
                for col_i in range(len(row)-1, -1, -1):
                    c = row[col_i]
                    if len(cols) <= i:
                        cols.append(c)
                    else:
                        cols[i] += c
                    i += 1
                #print(f"cols is now {cols}")
        return total


    def solve(self, filename):
        self.read_file(filename)
        #print(f"problems are {self.problems}")
        total = self.calculate()
        print(f"total is {total}")


if __name__ == "__main__":
    filename = "input.txt"

    solution = Solution()
    solution.solve(filename)
