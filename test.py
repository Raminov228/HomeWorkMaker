class MAP():
    def __init__(self, color_map):
        self.color_map = color_map
        self.size = (len(a[0]), len(a))
        self._get_areas()
        self._get_conturs()

    def _is_dot_reg(self, x, y):
        for area in self.areas:
            if (x, y) in area[0]:
                return True
        return False

    def _is_dot_inside(self, x, y):
        return 0 <= x <= self.size[0] - 1 and 0 <= y <= self.size[1] - 1

    def _is_dot_nice(self, x, y, dots):
        return not (x, y) in dots and self._is_dot_inside(x, y)

    def get_area(self, x0, y0):
        color = self.color_map[y0][x0]
        dots = []
        self._fill_area(x0, y0, color, dots)
        return (sorted(dots), color)

    def _fill_area(self, x, y, color, dots):
        dots.append((x, y))
        for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if self._is_dot_nice(x + d[0], y + d[1], dots) and a[y + d[1]][x + d[0]] == color:
                self._fill_area(x + d[0], y + d[1], color, dots)

    def _get_areas(self):
        self.areas = []
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if not self._is_dot_reg(x, y):
                    self.areas.append(self.get_area(x, y))

    def _is_dot_inside(self, x, y):
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def _get_contur(self, area):
        contur = []
        for dot in area[0]:
            a = False
            for d in[(1, 0), (0, 1), (-1, 0), (0, -1)]:
                if not self._is_dot_inside(dot[0] + d[0], dot[1] + d[1]) or self.color_map[dot[1] + d[1]][dot[0] + d[0]] != area[1]:
                    a = True
            if a:
                contur.append(dot)
        return (contur, area[1])

    def _get_conturs(self):
        self.conturs = [self._get_contur(area) for area in self.areas]


a = [[0, 0, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 1],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 1, 0, 0, 0, 0],
     [0, 0, 1, 1, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 1, 0, 0],
     [0, 0, 0, 0, 1, 1, 0, 0]]

mp = MAP(a)
areas = mp.areas
print(areas)

for ar in areas:
    b = [[0 for i in range(8)] for j in range(8)]

    for dot in ar[0]:
        b[dot[1]][dot[0]] = 1

    for l in b:
        print(l)
    print()

print(len(areas))
print(mp.conturs[0])

b = [[0 for i in range(8)] for j in range(8)]

for dot in mp.conturs[0][0]:
    b[dot[1]][dot[0]] = 1


for l in b:
    print(l)

