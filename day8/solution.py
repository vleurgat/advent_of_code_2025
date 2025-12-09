import math

class Solution:

    def __init__(self):
        self.boxes = []
        self.distances = {}
        self.circuits = []


    def read_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                x, y, z = map(int, line.strip().split(','))
                self.boxes.append((x,y,z))
        for box in self.boxes:
            self.circuits.append([box])


    def find_distances(self):
        for bk in self.boxes:
            #print(f"box key is {bk}")
            (x1, y1, z1) = bk
            #print(f"find distances for {bk}")
            for obk in self.boxes:
                if obk != bk:
                    (x2, y2, z2) = obk
                    d = math.sqrt((abs(x2 - x1) ** 2) + (abs(y2 - y1) ** 2) + (abs(z2 - z1) ** 2))
                    if not d in self.distances:
                        self.distances[d] = (bk, obk)
                    else:
                        if self.distances[d] != (bk, obk) and self.distances[d] != (obk, bk):
                            raise Exception("got multiple box pairs for distance {d}")


    def existing_circuit(self, b):
        for c in self.circuits:
            if b in c:
                return c
        return None


    def merge_circuits(self, c1: list, c2: list):
        if c1 == c2:
            #print("  do not merge c1 == c2")
            pass
        else:
            self.circuits.remove(c1)
            self.circuits.remove(c2)
            new_c = c1.copy()
            new_c.extend(c2)
            #print(f"  real merge of {c1} and {c2} to create {new_c}")
            self.circuits.append(new_c)


    def create_circuits0(self, num_pairs):
        d_keys = list(self.distances.keys())
        d_keys.sort()
        top_d_keys = d_keys[:num_pairs]

        for dk in top_d_keys:
            b1, b2 = self.distances[dk]
            #print(f"\ndistance {dk} between boxes: {b1} and {b2}")
            b1c = self.existing_circuit(b1)
            b2c = self.existing_circuit(b2)
            if b1c and b2c:
                #print(f"box {b1} is in {b1c}; and box {b2} is in {b2c} - merge those circuits")
                self.merge_circuits(b1c, b2c)
            elif b1c:
                #print(f"box {b1} is in {b1c}; and box {b2} is not in a circuit - add {b2} to the circuit")
                b1c.append(b2)
            elif b2c:
                #print(f"box {b2} is in {b2c}; and box {b1} is not in a circuit - add {b1} to the circuit")
                b2c.append(b1)
            else:
                #print(f"new circuit for boxes {b1} and {b2}")
                self.circuits.append([b1, b2])


    def create_circuits(self):
        d_keys = list(self.distances.keys())
        d_keys.sort()

        i = 0
        for dk in d_keys:
            b1, b2 = self.distances[dk]
            #print(f"\ndistance {dk} between boxes: {b1} and {b2}")
            b1c = self.existing_circuit(b1)
            b2c = self.existing_circuit(b2)
            if b1c and b2c:
                #print(f"  box {b1} is in {b1c}; and box {b2} is in {b2c} - merge those circuits")
                self.merge_circuits(b1c, b2c)
            elif b1c:
                #print(f"  box {b1} is in {b1c}; and box {b2} is not in a circuit - add {b2} to the circuit")
                b1c.append(b2)
            elif b2c:
                #print(f"  box {b2} is in {b2c}; and box {b1} is not in a circuit - add {b1} to the circuit")
                b2c.append(b1)
            else:
                #print(f"  new circuit for boxes {b1} and {b2}")
                self.circuits.append([b1, b2])
            if i > 5 and len(self.circuits) == 1:
                print(f"*** complete at i == {i} last boxes were {b1} and {b2}")
                res = b1[0] * b2[0]
                return res
            i += 1


    def size_circuits0(self):
        sizes = []
        for c in self.circuits:
            sizes.append(len(c))
        sizes.sort(reverse=True)
        total = sizes[0] * sizes[1] * sizes[2]
        print(f"total circuit size: {total}")


    def solve(self, filename, num_pairs):
        self.read_file(filename)
        self.find_distances()
        res = self.create_circuits()
        print(f"res (x1 * x2 of final box pair) is {res}")


if __name__ == "__main__":
    solution = Solution()
    solution.solve('input.txt', 1000)
    #solution.solve('test.txt', 10)
