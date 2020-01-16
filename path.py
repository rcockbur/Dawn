class Path:
    id_index = 0

    def new_id():
        Path.id_index += 1
        return Path.id_index - 1

    def __init__(self, points):
        self.id = Path.new_id()
        self.points = list()
        for point in points:
            self.points.append(point)

    def size(self):
        return len(self.points)

    def append(self, point):
        self.points.append(point)

    def pop(self):
        return self.points.pop(0)