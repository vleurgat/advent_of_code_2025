class Solution1:

    def __init__(self):
        self.shapes = []
        self.regions = []
        self.presents = []
        self.negative_cache = []


    def read_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            shape = []
            for line in lines:
                line = line.strip()
                if 'x' in line:
                    # process region
                    ls = line.split(':')
                    self.regions.append(list(map(int, ls[0].strip().split('x'))))
                    self.presents.append(list(map(int, ls[1].strip().split())))
                elif '#' in line or '.' in line:
                    shape.append(line)
                elif shape:
                    shapes = []
                    shapes.append(shape)
                    shapes.append(self.rot90(shape))
                    shapes.append(self.rot180(shape))
                    shapes.append(self.rot270(shape))
                    self.shapes.append(shapes)
                    shape = []


    def inbounds(self, x, y, grid) -> bool:
        return x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)


    def print_shape(self, shape, extra=""):
        if extra:
            print(f"{extra}:")
        for row in shape:
            print(f"  {row}")
        print("")


    def rot90(self, grid) -> list:
        new_grid = []
        for x in range(len(grid[0])):
            row = ""
            for y in range(len(grid)):
                row += grid[y][x]
            new_grid.append(row[::-1])
        return new_grid


    def rot180(self, grid) -> list:
        new_grid = []
        for y in range(len(grid)):
            new_grid.append(grid[y][::-1])
        return new_grid


    def rot270(self, grid) -> list:
        new_grid = []
        for x in range(len(grid[0])):
            row = ""
            for y in range(len(grid)):
                row += grid[y][x]
            new_grid.append(row[::-1])
        return new_grid[::-1]


    def free_in_grid(self, grid) -> int:
        free_space = 0
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == '.':
                    free_space += 1
        return free_space


    def max_shape_dims(self, shape_id):
        shape = self.shapes[shape_id][0]
        min_x = -1
        max_x = 0
        min_y = -1
        max_y = 0
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x] == '#':
                    if min_x == -1 or x < min_x:
                        min_x = x
                    if x > max_x:
                        max_x = x
            if min_y == -1 or y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
        width = (max_x - min_x) + 1
        height = (max_y - min_y) + 1
        return width, height



    # def has_space(self, grid, shapes):
    #     free_space = self.free_in_grid(grid)
    #     shape_space = 0
    #     for shape in shapes:
    #         for y in range(len(shape)):
    #             for x in range(len(shape[y])):
    #                 if shape[y][x] == '#':
    #                     shape_space += 1
    #     ret = free_space >= shape_space
    #     if not ret:
    #         print(f"no space for shapes [{shapes}] in {grid} ({free_space} < {shape_space})")
    #     return ret 


    def fits(self, x, y, grid, shape_id, orient):
        grid = grid.copy()
        shape = self.shapes[shape_id][orient]
        for j in range(len(shape)):
            for i in range(len(shape[j])):
                sc = shape[j][i]
                if sc == '#':
                    if not self.inbounds(x+i, y+j, grid):
                        return None
                    gc = grid[y+j][x+i]
                    if gc == '#':
                        return None
                    sl = list(grid[y+j])
                    sl[x+i] = '#'
                    grid[y+j] = "".join(sl)
        #print(f"fits works for shape {shape} in grid {grid} starting [{x},{y}]")
        return grid


    def do_fit(self, depth, grid, shape_ids, attempted_str) -> bool:
        if len(shape_ids) == 0:
            print(f"TRUE for {attempted_str} @ depth {depth}")
            return True, attempted_str
        if attempted_str in self.negative_cache:
            print(f"{attempted_str} is in negative cache")
            return False, attempted_str
        shape_ids = shape_ids.copy()
        shape_id = shape_ids.pop()
        attempted_str = attempted_str + f"+{shape_id}"
        #print(f"shape_ids are {shape_ids} and shape_id is {shape_id}")
        #input(f"{depth}: fit {shape_id} grid_free={self.free_in_grid(grid)} len(shape_ids)={len(shape_ids)}")
        attempted_strs = []
        for i in range(4):
            for y in range(len(grid)):
                for x in range(len(grid[y])):
                    #print(f"x = {x} and y = {y}")
                    new_grid = self.fits(x, y, grid, shape_id, i)
                    if new_grid:
                        #print(f"x = {x} and y = {y}: got fit for shape{i}: recurse {depth}")
                        att_s = self.do_fit(depth+1, new_grid, shape_ids, attempted_str)
                        if not att_s:
                            return ""
        print(f"FALSE for {attempted_str} @ depth {depth} remaining shapes {len(shape_ids)}")
        self.negative_cache.append(attempted_str)
        return False, attempted_str


    def fit0(self, region, presents) -> bool:
        grid = []
        for _ in range(region[1]):
            grid.append('.' * region[0])
        print(f"starting grid is {grid}")

        present_shape_ids = []
        for pi in range(len(presents)):
            if presents[pi] > 0:
                print(f"adding {presents[pi]} shapes of index {pi}")
                for _ in range(presents[pi]):
                    present_shape_ids.append(pi)
        for present_shape_id in present_shape_ids:
            print(f"try to fit present shape with id {present_shape_id} to region {region}")

        return self.do_fit(0, grid, present_shape_ids, "")


    def fit(self, region, presents) -> bool:
        present_shape_ids = []
        for pi in range(len(presents)):
            if presents[pi] > 0:
                print(f"adding {presents[pi]} shapes of index {pi}")
                for _ in range(presents[pi]):
                    present_shape_ids.append(pi)

        if self.is_definitely_possible(region, present_shape_ids):
            return True
        if self.is_definitely_impossible(region, present_shape_ids):
            return False
        raise Exception(f"got unknown for region {region} and presents {presents}")


    def is_definitely_possible(self, region, present_shape_ids) -> bool:
        presents_area = len(present_shape_ids) * 9
        grid_area = region[0] * region[1]
        return presents_area <= grid_area


    def area_of_shape(self, shape_id):
        shape_area = 0
        shape = self.shapes[shape_id][0]
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x] == '#':
                    shape_area += 1
        return shape_area


    def is_definitely_impossible(self, region, present_shape_ids) -> bool:
        grid_area = region[0] * region[1]
        present_area = 0
        for present_shape_id in present_shape_ids:
            present_area += self.area_of_shape(present_shape_id)
        return present_area > grid_area


    def solve(self, filename):
        self.read_file(filename)
        # print("shapes are:")
        # for shape in self.shapes:
        #     self.print_shape(shape, "0")
        #     self.print_shape(self.rot90(shape), "90")
        #     self.print_shape(self.rot180(shape), "180")
        #     self.print_shape(self.rot270(shape), "270")
        # print(f"regions are: {self.regions}")
        # print(f"presents are: {self.presents}")

        total = 0
        for i in range(len(self.regions)):
            ret = self.fit(self.regions[i], self.presents[i])
            print(f"result for {i} is {ret}")
            if ret:
                total += 1
        print(f"total is {total}")


if __name__ == "__main__":
    solution = Solution1()
    solution.solve('input.txt')
