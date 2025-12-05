
class Solution:

    def __init__(self):
        self.fresh_ranges = []
        self.ingredients = []


    def read_file(self, filename: str):
        str_ranges = []
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if '-' in line:
                    ids = line.split('-')
                    l = int(ids[0])
                    h = int(ids[1])
                    str_ranges.append(f"{l:020d}-{h:020d}")
                elif len(line) > 0:
                    self.ingredients.append(int(line))
        str_ranges.sort()
        for s in str_ranges:
            ids = s.split('-')
            l = int(ids[0])
            h = int(ids[1])
            self.add_or_merge(l, h)

 
    def add_or_merge(self, l: int, h: int) -> list:
        replaced = False
        for i in range(len(self.fresh_ranges)):
            fl = self.fresh_ranges[i][0]
            fh = self.fresh_ranges[i][1]
            if h < fl or l > fh:
                # no overlap
                pass
            elif l >= fl and l <= fh and h >= fl and h <= fh:
                # contained in entry - skip
                replaced = True
                break
            elif l <= fl and h >= fh:
                # complete overlap - replace
                self.fresh_ranges[i] = [l, h]
                replaced = True
                break
            elif l <= fl and h <= fh:
                # lower range overlaps - replace
                self.fresh_ranges[i] = [l, fh]
                replaced = True
                break
            elif l >= fl and h >= fh:
                # higer range overlaps - replace
                self.fresh_ranges[i] = [fl, h]
                replaced = True
                break
            else:
                raise Exception(f"unknown case: l={l} h={h} entry={self.fresh_ranges[i]}")
        if not replaced:
            self.fresh_ranges.append([l, h])


    def total_of_ranges(self) -> int:
        total = 0
        for r in self.fresh_ranges:
            total += (r[1] - r[0] + 1)
        return total


    def solve(self, filename):
        self.read_file(filename)
        #print(f"ranges are {self.fresh_ranges}")
        #print(f"ingredients are {self.ingredients}")
        fresh_ingredients = []
        for ingredient in self.ingredients:
            for fresh_range in self.fresh_ranges:
                if ingredient >= fresh_range[0] and ingredient <= fresh_range[1]:
                    fresh_ingredients.append(ingredient)
                    break
        #print(f"fresh ingredients are {fresh_ingredients}")
        print(f"number of fresh ingredients is {len(fresh_ingredients)}")
        print(f"total number of fresh ids in ranges: {self.total_of_ranges()}")


if __name__ == "__main__":
    filename = "input.txt"

    solution = Solution()
    solution.solve(filename)
