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
            self.flower_list = flower_list
            
            #obtain the full plant list
            self.plants = {(j,i) for i in range(self.N) for j in range(self.M) if self.garden_map[i][j]>0}

            #create the initial state
            self.initial = (0,0,self.W0,0,frozenset())


    def actions(self, state):
        possible_moves = []

        # movement
        if state["y"] != 0 and self.garden_map[state["y"]-1][state["x"]] > -1:
            possible_moves.append("U")
        if state["y"] < (self.N - 1) and self.garden_map[state["y"]+1][state["x"]] > -1:
            possible_moves.append("D")
        if state["x"] != 0 and self.garden_map[state["y"]][state["x"]-1] > -1:
            possible_moves.append("L")
        if state["x"] < (self.M - 1) and self.garden_map[state["y"]][state["x"]+1] > -1:
            possible_moves.append("R")

        # watering
        cell = self.garden_map[state["y"]][state["x"]]
        if cell > 0 and (state["x"], state["y"]) not in state["is_watered"]:
            wk, dk = self.flower_list[cell-1]
            if state["water"] >= wk and state["time"] <= dk:
                possible_moves.append("W")

        return possible_moves


    def result(self, state, action):
        """Return new state dict after applying action"""

        #New_state_identification
        self.state_num += 1

        new_state = {
            "x": state["x"],
            "y": state["y"],
            "water": state["water"],
            "time": state["time"] + 1,
            "is_watered": set(state["is_watered"]),
            "state_num" : self.state_num,
            "prev_state_num": state["state_num"],
        }

        if action == "U":
            new_state["y"] -= 1
        elif action == "D":
            new_state["y"] += 1
        elif action == "L":
            new_state["x"] -= 1
        elif action == "R":
            new_state["x"] += 1
        elif action == "W":
            cell = self.garden_map[state["y"]][state["x"]]
            wk, _ = self.flower_list[cell-1]
            new_state["water"] -= wk
            new_state["is_watered"].add((state["x"], state["y"]))

        # refill water if back at start
        if (new_state["x"], new_state["y"]) == (0, 0):
            new_state["water"] = self.W0

        return new_state
    
    def path_cost(self,c,state1,action,state2):
       
        return c+1
    
    def goal_test(self,state):
        
        return self.plants.issubset(state["is_watered"])
    
    def solve(self):
        
        solution_found = search.uniform_cost_search(self)

        if solution_found is None: 
            print("No solution found")
            return None
        

        solution = solution_found.solution()
        print("solution:",solution)
        return solution
            
#testes
problem = GardenerProblem()

with open("ex0.dat") as fh:
    problem.load(fh)

solution = problem.solve()
