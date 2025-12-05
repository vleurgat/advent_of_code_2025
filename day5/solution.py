
class Solution:

    def __init__(self):
        self.fresh_ranges = []
        self.ingredients = []


    def read_file(self, filename: str):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if '-' in line:
                    ids = line.split('-')
                    self.fresh_ranges.append([int(ids[0]), int(ids[1])])
                elif len(line) > 0:
                    self.ingredients.append(int(line))

 
    def solve(self, filename):
        self.read_file(filename)
        print(f"ranges are {self.fresh_ranges}")
        print(f"ingredients are {self.ingredients}")
        fresh_ingredients = []
        for ingredient in self.ingredients:
            for fresh_range in self.fresh_ranges:
                if ingredient >= fresh_range[0] and ingredient <= fresh_range[1]:
                    fresh_ingredients.append(ingredient)
                    break
        print(f"fresh ingredients are {fresh_ingredients}")
        print(f"number of fresh ingredients is {len(fresh_ingredients)}")


if __name__ == "__main__":
    filename = "input.txt"

    solution = Solution()
    solution.solve(filename)
