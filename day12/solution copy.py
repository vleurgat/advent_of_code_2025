class Solution1:

    def __init__(self):
        self.shapes = []
        self.regions = []
        self.presents = []


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
                    self.shapes.append(shape)
                    shape = []


    def inbounds(self, x, y, grid) -> bool:
        return x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)


    def print_shape(self, shape, extra=""):
        if extra:
            print(f"{extra}:")
        for row in shape:
            print(f"  {row}")
        print("")


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


    def rot90(self, grid) -> list:
        new_grid = []
        for x in range(len(grid[0])):
            row = ""
            for y in range(len(grid)):
                row += grid[y][x]
            new_grid.append(row[::-1])
        return new_grid


    def free_in_grid(self, grid) -> int:
        free_space = 0
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == '.':
                    free_space += 1
        return free_space


    def max_shape_dims(self, shape):
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


    def fits(self, x, y, grid, shape):
        grid = grid.copy()
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


    def do_fit(self, depth, grid, shapes_to_fit) -> bool:
        if len(shapes_to_fit) == 0:
            return True
        shapes_to_fit = shapes_to_fit.copy()
        shape = shapes_to_fit.pop()
        width, height = self.max_shape_dims(shape)
        #input(f"{depth}: fit {shape} ({width}x{height}) grid_free={self.free_in_grid(grid)} len(shapes_to_git)={len(shapes_to_fit)}")
        for y in range(1 + len(grid) - height):
            for x in range(1 + len(grid[y]) - width):
                c = grid[y][x]
                if c == '#':
                    continue
                #print(f"x = {x} and y = {y}")
                new_grid = self.fits(x, y, grid, shape)
                if new_grid:
                    #print(f"x = {x} and y = {y}: got fit for shape0: recurse {depth}")
                    if self.do_fit(depth+1, new_grid, shapes_to_fit):
                        return True
                new_grid = self.fits(x, y, grid, self.rot90(shape))
                if new_grid:
                    #print(f"x = {x} and y = {y}: got fit for shape90: recurse {depth}")
                    if self.do_fit(depth+1, new_grid, shapes_to_fit):
                        return True
                new_grid = self.fits(x, y, grid, self.rot180(shape))
                if new_grid:
                    #print(f"x = {x} and y = {y}: got fit for shape180: recurse {depth}")
                    if self.do_fit(depth+1, new_grid, shapes_to_fit):
                        return True
                new_grid = self.fits(x, y, grid, self.rot270(shape))
                if new_grid:
                    #print(f"x = {x} and y = {y}: got fit for shape270: recurse {depth}")
                    if self.do_fit(depth+1, new_grid, shapes_to_fit):
                        return True
        print(f"FALSE @ depth {depth} len(shapes_to_fit)={len(shapes_to_fit)}")
        return False


    def fit(self, region, presents) -> bool:
        grid = []
        for _ in range(region[1]):
            grid.append('.' * region[0])
        print(f"starting grid is {grid}")

        present_shapes = []
        for pi in range(len(presents)):
            if presents[pi] > 0:
                print(f"adding {presents[pi]} shapes of index {pi}")
                for _ in range(presents[pi]):
                    present_shapes.append(self.shapes[pi])
        for present_shape in present_shapes:
            print(f"try to fit present shape {present_shape} to region {region}")

        return self.do_fit(0, grid, present_shapes)


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

        i = 2
        ret = self.fit(self.regions[i], self.presents[i])
        print(f"result for {i} is {ret}")


if __name__ == "__main__":
    solution = Solution1()
    solution.solve('test.txt')
