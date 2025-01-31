from queue import PriorityQueue

class TaquinBoard:
    def __init__(self, board):
        self.board = board
        self.size = int(len(board) ** 0.5)
        self.empty_pos = self.board.index(0)

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(self.board))

    def __lt__(self, other):
        return self.board < other.board

    def neighbors(self):
        neighbors = []
        row, col = divmod(self.empty_pos, self.size)
        moves = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        for new_row, new_col in moves:
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                new_pos = new_row * self.size + new_col
                new_board = self.board[:]
                new_board[self.empty_pos], new_board[new_pos] = new_board[new_pos], new_board[self.empty_pos]
                neighbors.append(TaquinBoard(new_board))

        return neighbors

    def __repr__(self):
        size = self.size
        return "\n".join(
            [" ".join(map(str, self.board[i:i + size])) for i in range(0, len(self.board), size)]
        )

def dijkstra_solver(start_board):
    pq = PriorityQueue()
    pq.put((0, start_board))

    distances = {start_board: 0}
    previous_nodes = {start_board: None}

    goal_board = list(range(1, start_board.size ** 2)) + [0]

    while not pq.empty():
        current_distance, current_board = pq.get()

        if current_board.board == goal_board:
            return reconstruct_path(previous_nodes, current_board)

        for neighbor in current_board.neighbors():
            new_distance = current_distance + 1

            if neighbor not in distances or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_board
                pq.put((new_distance, neighbor))

    return None


def reconstruct_path(previous_nodes, current_board):
    path = []
    while current_board:
        path.append(current_board)
        current_board = previous_nodes[current_board]
    return path[::-1]


if __name__ == "__main__":
    start_board = TaquinBoard([1, 2, 3, 4, 5, 6, 7, 8, 0])  # Solved board
    shuffled_board = TaquinBoard([1, 2, 3, 4, 5, 6, 0, 7, 8])

    solution = dijkstra_solver(shuffled_board)

    if solution:
        print("Solution found in {} moves:\n".format(len(solution) - 1))
        for step in solution:
            print(step)
            print("---")
    else:
        print("No solution found.")
