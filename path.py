print("running path.py")

class Path:
    id_index = 0

    def new_id():
        Path.id_index += 1
        return Path.id_index - 1

    def __init__(self):
        self.id = Path.new_id()
        self.points = list()

    def size(self):
        return len(self.points)

    def append(self, point):
        self.points.append(point)

    def clear(self):
        self.points.clear()

    def pop(self):
        return self.points.pop(0)

    def get(self, n):
        return self.points[n]

    def print(self):
        r = "Path: "
        for point in self.points:
            r = r + "(" + str(point[0]) + "," + str(point[1]) + ")"
        print(r)

    def reverse(self):
        self.points = self.points[::-1]
        return self