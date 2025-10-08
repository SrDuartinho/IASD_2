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
            
            self.initial = (0, 0, self.W0, 0, frozenset())

    def actions(self, state):
        x, y, water, time, watered = state
        possible_moves = []

        if x < (self.M - 1) and self.garden_map[y][x+1] > -1:
            possible_moves.append("R")
        if y != 0 and self.garden_map[y-1][x] > -1:
            possible_moves.append("U")
        if x != 0 and self.garden_map[y][x-1] > -1:
            possible_moves.append("L")     
        if y < (self.N - 1) and self.garden_map[y+1][x] > -1:
            possible_moves.append("D")
        
    
        cell = self.garden_map[y][x]
        if cell > 0 and (x, y) not in watered:
            wk, dk = self.flower_list[cell-1]
            if water >= wk and time <= dk:
                possible_moves.append("W")

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
        
    def path_cost(self,c,state1,action,state2):
       
        return c+1
    
    def solve(self):
        node = search.breadth_first_graph_search(self)
        if node:
            return "".join(node.solution())
        return None