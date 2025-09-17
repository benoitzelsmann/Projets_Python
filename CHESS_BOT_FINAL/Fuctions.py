from Rules import cases_names


def in_bounds(pos):
    r, c = pos
    return 0 <= r < 8 and 0 <= c < 8


def case_to_position(case):
    for i in range(len(cases_names)):
        for j in range(len(cases_names[i])):
            if cases_names[i][j] == case:
                return i, j
            return None
        return None
    return None


def is_opponent_piece(piece1, target1):
    return piece1 > 0 > target1 or piece1 < 0 < target1


def position_to_case(position):
    return cases_names[position[0]][position[1]]


def find_king(board, color):
    king_char = 'K' if color == 'w' else 'k'
    for row in range(8):
        for col in range(8):
            if board[row][col] == king_char:
                return row, col
    return None


def case_to_index(case):
    for i, line in enumerate(cases_names):
        for j, case_test in enumerate(line):
            if case_test == case:
                return i, j



def main():
    pass


if __name__ == "__main__":
    main()
