import search

class GardenerProblem(search.Problem):
    
    def __init__(self):
        self.N = 0
        self.M = 0
        self.garden_map = []
        self.flower_list = []  
        self.W0 = 0
        self.start = (0,0)

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
    
    def check_solution(self, plan, verbose = False):
        time = 0
        x, y = self.start
        water_level = self.W0
         
        moves = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
        is_watered = set()
        
        for action in plan:
           
            if action in moves:
                dx, dy = moves[action]
                x, y = x + dx, y + dy
                #print (f"({x}, {y}) at step {time}")
                if not (0 <= x < self.N and 0 <= y < self.M):
                    if verbose:
                        print(f"Invalid move to ({x}, {y}) - out of bounds.")
                    return False
                
                if self.garden_map[x][y] == -1: 
                    if verbose:
                        print(f"Invalid move to ({x}, {y}) - obstacle encountered.")
                    return False
                
                if (x, y) == (0, 0):
                    water_level = self.W0

            elif action == "W":
                cell = self.garden_map[x][y]

                if cell <= 0: 
                    if verbose: print(f"No plant at ({x},{y}) step {time}")
                    return False

                if (x, y) in is_watered:
                    if verbose: print(f"Plant already watered at ({x},{y})")
                    return False

                wk, dk = self.flower_list[cell-1] 
                if water_level < wk:
                    if verbose: print(f"Not enough water at step {time}")
                    return False

                if time > dk:
                    if verbose: print(f"Deadline missed for plant at ({x},{y}) at step {time}")
                    return False

                water_level -= wk
                is_watered.add((x, y))

            else:
                if verbose: print(f"Invalid action '{action}' at step {time}")
                return False
            time += 1

        # verificar se todas as plantas ja foram regadas
        all_plants = {(i, j) for i in range(self.N) for j in range(self.M)
                      if self.garden_map[i][j] > 0}
        if is_watered != all_plants:
            if verbose:
                missing = all_plants - is_watered
                print(f"Not all plants watered, missing: {missing}")
            return False
        return True
        


#testes
#problem = GardenerProblem()

#with open("ex8.dat") as fh:
   # problem.load(fh)

#with open("ex8.plan") as fh:
    #plan = fh.read().strip()  # se o plano for uma única linha


#print(problem.N, problem.M, problem.W0)
#print(problem.garden_map)
#print(problem.flower_list)
#print(problem.check_solution(plan, verbose=True))
