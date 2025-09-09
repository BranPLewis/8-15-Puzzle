import eight_puzzle_boards
import fifteen_puzzle_boards
import heapq, argparse

eight_GS = [
    [1,2,3],
    [4,5,6],
    [7,8,0]
]
fifteen_GS = [
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
    [13,14,15,0]
]

def find_blank(state):
    size = len(state)
    for r in range(size):
        for c in range(size):
            if state[r][c] == 0:
                return r, c

def actions(state):
    size = len(state)
    moves = []
    blank_pos = find_blank(state)
    row, col = blank_pos
    if row > 0:
        moves.append('UP')
    if row < size-1:
        moves.append('DOWN')
    if col > 0:
        moves.append('LEFT')
    if col < size-1:
        moves.append('RIGHT')
    return moves

def transition(state,action):
    blank_pos = find_blank(state)
    row, col = blank_pos
    new_state = [list(r) for r in state]  # Deep copy of the state
    if action == 'UP':
        new_state[row][col], new_state[row-1][col] = new_state[row-1][col], new_state[row][col]
    elif action == 'DOWN':
        new_state[row][col], new_state[row+1][col] = new_state[row+1][col], new_state[row][col]
    elif action == 'LEFT':
        new_state[row][col], new_state[row][col-1] = new_state[row][col-1], new_state[row][col]
    elif action == 'RIGHT':
        new_state[row][col], new_state[row][col+1] = new_state[row][col+1], new_state[row][col]
    return new_state

def StepCost(state, action, next_state):
    return 1

def heuristic(goal_state,state,h_type):
    size = len(state)
    distance = 0
    if(h_type == "misplaced"):
        for r in range(size-1):
            for c in range(size-1):
                if state[r][c] != 0 and state[r][c] != goal_state[r][c]:
                    distance += 1
    elif h_type == "manhattan" or h_type == "weighted_manhattan": # Calculate Manhattan for both
        size = len(state)
        for r in range(size):
            for c in range(size):
                if state[r][c] != 0:
                    target_r = (state[r][c] - 1) // size
                    target_c = (state[r][c] - 1) % size
                    distance += abs(r - target_r) + abs(c - target_c)
        if h_type == "weighted_manhattan":
            return distance * 1.5
    elif(h_type == "zero"):
        return 0
    return distance

def goal(goal_state,state):
    return state == goal_state

def a_star_search(initial_state,goal_state,h_type):
    initial_state_tuple = tuple(map(tuple, initial_state))
    g_score_initial = 0
    h_score_initial = heuristic(goal_state, initial_state, h_type)
    f_score_initial = g_score_initial + h_score_initial

    frontier = [(f_score_initial, g_score_initial, initial_state_tuple, [])]
    explored = {initial_state_tuple: 0}
    
    nodes_generated = 1
    nodes_expanded = 0
    max_frontier_size = 1
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))

        _, g, current_state_tuple, path = heapq.heappop(frontier)

        current_state = [list(row) for row in current_state_tuple]
        if goal(goal_state,current_state):
            return path, g, nodes_expanded, nodes_generated, max_frontier_size
        nodes_expanded += 1
        for action in actions(current_state):
            child_state = transition(current_state, action)
            child_state_tuple = tuple(map(tuple, child_state))
            nodes_generated += 1
            new_g = g + StepCost(current_state, action, child_state)

            if child_state_tuple not in explored or new_g < explored[child_state_tuple]:
                explored[child_state_tuple] = new_g
                h = heuristic(goal_state,child_state, h_type)
                heapq.heappush(frontier, (new_g + h, new_g, child_state_tuple, path + [action]))
        
    return None, -1, nodes_expanded, nodes_generated, max_frontier_size

# if __name__ == '__main__':
#     for ht in ["manhattan","misplaced","zero","weighted_manhattan"]:
#         path, cost, expanded, generated, max_frontier = a_star_search(ht)
#         print(f"Heuristic: {ht}")
#         if path:
#             print(f"  Solution Path: {path}")
#             print(f"  Solution Cost: {cost}")
#             print(f"  Solution Depth: {len(path)}")
#             print(f"  Nodes Expanded: {expanded}")
#             print(f"  Nodes Generated: {generated}")
#             print(f"  Max Frontier Size: {max_frontier}")
#         else:
#             print("  No solution found.")
#         print("-" * 20)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Solve the N-Puzzle with A* search.")
    parser.add_argument("domain", type=str, choices=["puzzle"], default="puzzle", help="The problem domain to solve (e.g., 'puzzle').")
    parser.add_argument("-H", "--heuristic", type=str, choices=["misplaced", "manhattan","weighted_manhattan", "zero"], default="manhattan", help="The heuristic function to use.")
    parser.add_argument("-n", "--boards", type=int, default=3, help="The number of boards to solve from the predefined list.")
    parser.add_argument("-s", "--size", type=str, default="8", choices=["8","15"], help="The size of the puzzle board you want it to work on; 15 puzzle or 8 puzzle")
    args = parser.parse_args()
    # 2. Validate the domain
    if args.domain != "puzzle":
        print(f"Error: Unknown domain '{args.domain}'. This program only solves 'puzzle'.")
        exit()
    # 3. Run the solver on the requested number of boards
    if args.size == "8":
        num_boards_to_solve = min(args.boards, len(eight_puzzle_boards.puzzle_boards))
    elif args.size == "15":
        num_boards_to_solve = min(args.boards, len(fifteen_puzzle_boards.puzzle_boards))
    print(f"Running A* search on {num_boards_to_solve} board(s) with '{args.heuristic}' heuristic...")
    print("="*40)
    for i in range(num_boards_to_solve):
        print(f"\nSolving Board #{i+1}:")
        # Set the global IS to the current board from the list
        if args.size == "8":
            IS = eight_puzzle_boards.puzzle_boards[i]
            GS = eight_GS
        elif args.size == "15":
            IS = fifteen_puzzle_boards.puzzle_boards[i]
            GS = fifteen_GS
        path, cost, expanded, generated, max_frontier = a_star_search(IS,GS,args.heuristic)
        print(f"  Initial State: {IS}")
        if path is not None:
            print(f"  Solution Found!")
            print(f"    - Path: {path}")
            print(f"    - Cost/Depth: {cost}")
            print(f"    - Nodes Expanded: {expanded}")
            print(f"    - Nodes Generated: {generated}")
            print(f"    - Max Frontier Size: {max_frontier}")
        else:
            print("  No solution was found.")
        print("-" * 40)
