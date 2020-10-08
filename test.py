mark_map = [[0 for x in range(self.size[0])] y in range(self.size[1])]
for y in range(self.size[1]):
    for x in range(self.size[0]):
        if (x, y) in contur['dots'] and mark == -1:
            mark = 1
        if self.color(x, y) != contur['color'] and mark == 1:
            mark = -1
        if little_map[y][x] == 0:
            little_map[y][x] = mark
