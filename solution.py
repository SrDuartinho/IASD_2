import search


class GardenerProblem(search.Problem):
    
    def __init__(self):
        self.N = 0
        self.M = 0
        self.garden_map = []
        self.flower_list = []  
        self.W0 = 0
        self.start = (0,0)
        self.state_num = 0
        self.initial = None
        self.plants = None
        self.all_obstacles = None

    def load(self, fh):
        file_lines = [
            line.strip()
            for line in fh
            if line.strip() and not line.strip().startswith("#")
        ]

        if len(file_lines) == 1:
            self.solution = file_lines[0].strip()
            return
        else:
            self.N, self.M, self.W0 = map(int, file_lines[0].split())

            garden_map = []
            file_line_marker = 1
            for i in range(self.N):
                garden_map.append(list(map(int, file_lines[file_line_marker].split())))
                file_line_marker += 1

            flower_list = []
            while file_line_marker < len(file_lines):
                if file_lines[file_line_marker] != "":
                    water_needs, deadline = map(int, file_lines[file_line_marker].split())
                    flower_list.append((water_needs, deadline)) 
                file_line_marker += 1

            self.garden_map = garden_map

            #definicao do state inicial 
            self.state = garden_map

            self.flower_list = flower_list

            self.plants = {(j, i)
                for i in range(self.N)
                for j in range(self.M)
                if self.garden_map[i][j] > 0}

            self.all_obstacles = {(j, i)
                for i in range(self.N)
                for j in range(self.M)
                if self.garden_map[i][j] != 0}

            for i in range(self.N):
                for j in range(self.M):

                    if self.garden_map[i][j] <= 0:
                        if not any(i == y or j == x for (x, y) in self.all_obstacles):
                            cells_around = []
                            for dy in [-1, 0, 1]:
                                for dx in [-1, 0, 1]:
                                    if dx == 0 and dy == 0:
                                        continue
                                    ny, nx = i + dy, j + dx
                                    if 0 <= ny < self.N and 0 <= nx < self.M:
                                        cells_around.append(self.garden_map[ny][nx])

                            if all(v <= 0 for v in cells_around):
                                self.garden_map[i][j] = -1
            
            self.initial = (0, 0, self.W0, 0, frozenset())


    def actions(self, state):
        x, y, water, time, watered = state
        possible_moves = []
        
        for (px, py) in self.plants - watered:
            _, dk = self.flower_list[self.garden_map[py][px] - 1]
            if time > dk:
                return []
            
        cell = self.garden_map[y][x]
        if cell > 0 and (x, y) not in watered:
            wk, dk = self.flower_list[cell-1]
            if water >= wk and time <= dk:
                possible_moves.append("W")

        if x < (self.M - 1) and self.garden_map[y][x+1] > -1:
            possible_moves.append("R")
        if y != 0 and self.garden_map[y-1][x] > -1:
            possible_moves.append("U")
        if x != 0 and self.garden_map[y][x-1] > -1:
            possible_moves.append("L")     
        if y < (self.N - 1) and self.garden_map[y+1][x] > -1:
            possible_moves.append("D")
        
        return possible_moves


    def result(self, state, action):
        x, y, water, time, watered = state
        new_time = time + 1
        new_watered = set(watered)

        if action == "U":
            y -= 1
        elif action == "D":
            y += 1
        elif action == "L":
            x -= 1
        elif action == "R":
            x += 1
        elif action == "W":
            cell = self.garden_map[y][x]
            wk, _ = self.flower_list[cell-1]
            water -= wk
            new_watered.add((x, y))

        if (x, y) == (0, 0):
            water = self.W0

        return (x, y, water, new_time, frozenset(new_watered))
    
    def goal_test(self,state):
        x, y, water, time, watered = state
        
        return self.plants.issubset(watered)
    
    def h(self, node):
        x, y, water, time, watered = node.state
        unwatered = self.plants - watered
        if not unwatered:
            return 0

        avg_dist = sum(abs(x - px) + abs(y - py) for (px, py) in unwatered) / len(unwatered)

        total_needed = sum(self.flower_list[self.garden_map[py][px] - 1][0] for (px, py) in unwatered)

        trips_needed = 0
        if water < total_needed:
            trips_needed = (total_needed - water + self.W0 - 1) // self.W0

        dist_to_base = abs(x - 0) + abs(y - 0)
        refill_cost = trips_needed * (dist_to_base + 2)

        urgent_flowers = [
            (dk - time)
            for (px, py) in unwatered
            for (_, dk) in [self.flower_list[self.garden_map[py][px] - 1]]
            if dk - time < 20
        ]
        urgency_penalty = sum(1 + (20 - u) / 10 for u in urgent_flowers)

        spread_penalty = 0
        if len(unwatered) > 1:
            cx = sum(px for (px, _) in unwatered) / len(unwatered)
            cy = sum(py for (_, py) in unwatered) / len(unwatered)
            spread_penalty = sum(abs(px - cx) + abs(py - cy) for (px, py) in unwatered) / len(unwatered)

        time_penalty = 0.05 * time

        return ( avg_dist * 1.2 + refill_cost * 1.5 + urgency_penalty * 2.0
            + spread_penalty * 0.5 + len(unwatered) * 1.0 + time_penalty)
        
    def path_cost(self,c,state1,action,state2):
       
        return c+1
    
    def solve(self):
        node = search.astar_search(self, self.h)
        if node:
            return "".join(node.solution())
        return None
