from shapely import Polygon

class Solution:

    def __init__(self):
        self.points = []
        self.polygon = None


    def read_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                x, y = map(int, line.strip().split(','))
                self.points.append((x,y))
        self.polygon = Polygon(self.points)


    def find_biggest_rectangle0(self):
        max_area = -1
        for p in self.points:
            (x1, y1) = p
            for q in self.points:
                (x2, y2) = q
                if q == p or x2 == x1 or y2 == y1:
                    continue
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                if area > max_area:
                    max_area = area
        return max_area


    def find_biggest_rectangle(self):
        max_area = -1
        for p in self.points:
            (x1, y1) = p
            for q in self.points:
                (x2, y2) = q
                if q == p or x2 == x1 or y2 == y1:
                    continue
                c1 = (x2, y1)
                c2 = (x1, y2)
                if self.polygon.covers(Polygon([p, c1, q, c2])):
                    area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                    if area > max_area:
                        max_area = area
        return max_area


    def solve(self, filename):
        self.read_file(filename)
        #print(f"points are {self.points}")
        #print(f"polygon is {self.polygon}")
        max_area = self.find_biggest_rectangle()
        print(f"area of biggest rectangle is {max_area}")


if __name__ == "__main__":
    solution = Solution()
    solution.solve('input.txt')
