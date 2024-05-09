from z3 import Int, sat, Solver, Or, If, And


class NoSolution(Exception):
    pass


class TooManySolutions(Exception):
    pass


def value_constraint(solver: Solver, board):
    for row in board:
        for cell in row:
            solver.add(0 <= cell)
            solver.add(cell <= 1)


def row_constraint(solver: Solver, board):
    for row in board:
        solver.add(2 == sum(row))


def column_constraint(solver: Solver, board):
    for col in zip(*board, strict=True):
        solver.add(2 == sum(col))


def region_constraint(solver: Solver, board, regions: list[list[tuple[int, int]]]):
    for region in regions:
        solver.add(2 == sum([board[y][x] for x, y in region]))


def adjacent_constraint(solver: Solver, board):
    for i, row in enumerate(board):
        for j in range(len(row)):
            solver.add(
                If(
                    row[j] == 1,
                    And(
                        *[
                            board[i + x][j + y] == 0
                            for x in [-1, 0, 1]
                            for y in [-1, 0, 1]
                            if (x != 0 or y != 0)
                            and 0 <= i + x
                            and i + x < len(board)
                            and 0 <= j + y
                            and j + y < len(row)
                        ]
                    ),
                    True,
                )
            )


def alt_adjacent_constraint(solver: Solver, board):
    for i, row in enumerate(board):
        for j in range(len(row)):
            solver.add(
                sum(
                    [
                        board[i + x][j + y]
                        for x in [0, 1]
                        for y in [0, 1]
                        if i + x < len(board) and j + y < len(row)
                    ]
                )
                <= 1
            )


def solve(regions: list[list[tuple[int, int]]]):
    solver = Solver()
    board = [[Int(f"x_{i}_{j}") for i in range(9)] for j in range(9)]
    value_constraint(solver, board)
    row_constraint(solver, board)
    column_constraint(solver, board)
    region_constraint(solver, board, regions)
    alt_adjacent_constraint(solver, board)
    if sat == solver.check():
        model = solver.model()
        solution = [[model.evaluate(board[i][j]) for i in range(9)] for j in range(9)]
        # TODO Ensure uniqueness
        return solution
    else:
        raise NoSolution()
