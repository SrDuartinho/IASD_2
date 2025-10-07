from solution import GardenerProblem

# Load problem from .dat file
problem = GardenerProblem()
with open("ex8.dat") as fh:
    problem.load(fh)

# Solve the problem
solution_plan = problem.solve()

# Print your computed plan
print("Computed plan:", solution_plan)

# If there's a .plan file, compare results
try:
    with open("ex8.plan") as f:
        expected_plan = f.readline().strip()
        print("Expected plan:", expected_plan)

        if solution_plan == expected_plan:
            print("✅ Solution matches the expected plan!")
        else:
            print("❌ Solution differs from expected plan.")
except FileNotFoundError:
    print("(No ex3.plan file found — skipping comparison)")
