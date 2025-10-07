import search

#gaurdar estados
state = []


class GardenerProblem(search.Problem):
    
    def __init__(self):
        self.N = 0
        self.M = 0
        self.garden_map = []
        self.flower_list = []  
        self.W0 = 0
        self.start = (0,0)
        self.state_num = 0


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
            
            self.initial = (0, 0, self.W0, 0, frozenset())

    def actions(self, state):
        x, y, water, time, watered = state
        possible_moves = []

        if y != 0 and self.garden_map[y-1][x] > -1:
            possible_moves.append("U")
        if y < (self.N - 1) and self.garden_map[y+1][x] > -1:
            possible_moves.append("D")
        if x != 0 and self.garden_map[y][x-1] > -1:
            possible_moves.append("L")
        if x < (self.M - 1) and self.garden_map[y][x+1] > -1:
            possible_moves.append("R")

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
        plants = {(j, i)
                for i in range(self.N)
                for j in range(self.M)
                if self.garden_map[i][j] > 0}
        return plants.issubset(watered)
        
    def path_cost(self,c,state1,action,state2):
       
        return c+1
    
    def solve(self):
        node = search.breadth_first_graph_search(self)
        if node:
            return "".join(node.solution())
        return None

#testes
'''
problem = GardenerProblem()

with open("ex3.dat") as fh:
    problem.load(fh)

# start at the initial state
state.append({"prev_state_num": None,"state_num":0, "x": 0, "y": 0, "water": problem.W0, "time": 0, "is_watered": set()})
print("Initial state:", state[0])

# get possible actions
acts = problem.actions(state[0])
print("Available actions at start:", acts)

state.append(problem.result(state[0],"D"))
state.append(problem.result(state[1],"D"))
state.append(problem.result(state[2],"W"))
state.append(problem.result(state[3],"R"))
state.append(problem.result(state[4],"R"))
state.append(problem.result(state[5],"W"))
state.append(problem.result(state[6],"U"))
state.append(problem.result(state[7],"W"))
state.append(problem.result(state[8],"U"))
state.append(problem.result(state[9],"W"))

print("Final state:", state[10])

print("Veridict:",problem.goaltest(state[10]))
'''

'''
    # apply the first action (if any)
if acts:
    first_action = acts[0]
    new_state = problem.result(state[0], first_action)
    print(f"\nAfter action {first_action}:")
    print("New state:", new_state)

     # check possible actions from the new state
    next_acts = problem.actions(new_state)
    print("Available actions from new state:", next_acts)

    # apply a watering action if available
    if "D" in next_acts:
        watered_state = problem.result(new_state, "D")
        print("\nAfter watering:")
        print("Watered state:", watered_state)
        print("Plants watered:", watered_state["is_watered"])
'''

#print(problem.N, problem.M, problem.W0)
#print(problem.garden_map[0][0])
#print(problem.flower_list)
#print(problem.check_solution(plan, verbose=True))