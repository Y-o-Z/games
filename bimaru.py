# Bi-mar-u → Marke der Rätsel Agentur Schweiz (→ schiffli versänke)

# 8x8 grid, position all ships (o,o,o,o,<>,<>,<>,<=>,<=>,<==>) such that each ship has no immediate neighbour

# . → ?, o → single ship, m → middle section of ship, l → corner pointing left, r → corner pointing right,
# u → corner pointing up, d → corner pointing down, x → water

from collections import deque

legal_entries = [".", "o", "m", "l", "r", "u", "d", "x"]

# example_entries = (".," * 15 + "o," + ".," * 12 + "m," + ".," * 34 + ".").split(",")
# example_numbers = [2, 3, 2, 3, 3, 2, 2, 1, 5, 0, 3, 0, 4, 1, 2, 3]  # "subtract" existing ships before entry


class Bimaru:
    """
    # list of 64 entries from top-left to bottom-right
    # list of 16 numbers from top-left (columns (0..7)) to bottom-right (rows (0..7)) → (remaining space [!])
    """
    def __init__(self, entries, numbers):
        self.entries = entries[:]
        self.original_entries = entries[:]
        """
        for index in range(64):  # decrement numbers if entries[index] not in [".", "x"]
            if entries[index] in ["o", "m", "l", "r", "u", "d"]:
                row = get_row_from_index(index)
                column = get_column_from_index(index)
                numbers[column] -= 1
                numbers[8 + row] -= 1
        """
        self.numbers = numbers[:]
        self.original_numbers = numbers[:]

    def __repr__(self):
        rows = ["bimaru:\n", "  ".join([str(n) for n in self.numbers[:8]]) + "\n"]
        for row in range(8):
            current_row = []
            for column in range(8):
                current_row.append(str(self.entries[row * 8 + column]))
            current_row.append(str(self.numbers[8 + row]))
            rows.append("  ".join(current_row) + "\n")
        return "".join(rows)

    def reset(self):
        self.entries = self.original_entries[:]
        self.numbers = self.original_numbers[:]

    def find_single_ships(self):
        single_ships = []
        for index in range(64):
            if self.entries[index] == "o":
                single_ships.append(index)
        return single_ships

    def find_double_ships_and_unfinished_single_ships(self):
        double_ships = []
        unfinished_single_ships = []
        directions_double_ships = []
        directions_unfinished_single_ships = []
        for index in range(64):
            if self.entries[index] == "l":
                if self.entries[index + 1] == "r":
                    double_ships.append(index)
                    directions_double_ships.append("x")
                elif self.entries[index + 1] == ".":
                    unfinished_single_ships.append(index)
                    directions_unfinished_single_ships.append("x")
            elif self.entries[index] == "u":
                if self.entries[index + 8] == "d":
                    double_ships.append(index)
                    directions_double_ships.append("y")
                elif self.entries[index + 8] == ".":
                    unfinished_single_ships.append(index)
                    directions_unfinished_single_ships.append("y")
        return double_ships, directions_double_ships, unfinished_single_ships, directions_unfinished_single_ships

    """
    def find_single_middle_ships(self):
        single_middle_ships = []
        for index in range(64):
            if self.entries[index] == "m":
                single_middle_ships.append(index)
        return single_middle_ships
    """

    def find_triple_ships_and_unfinished_double_ships(self):
        triple_ships = []
        unfinished_double_ships = []
        directions_triple_ships = []
        directions_unfinished_double_ships = []
        for index in range(64):
            if self.entries[index] == "l":
                if self.entries[index + 1] == "m" and self.entries[index + 2] == "r":
                    triple_ships.append(index)
                    directions_triple_ships.append("x")
                elif self.entries[index + 1] == "m" and self.entries[index + 2] == ".":
                    unfinished_double_ships.append(index)
                    directions_unfinished_double_ships.append("x")
            elif self.entries[index] == "u":
                if self.entries[index + 8] == "m" and self.entries[index + 16] == "d":
                    triple_ships.append(index)
                    directions_triple_ships.append("y")
                elif self.entries[index + 8] == "m" and self.entries[index + 16] == ".":
                    unfinished_double_ships.append(index)
                    directions_unfinished_double_ships.append("y")
        return triple_ships, directions_triple_ships, unfinished_double_ships, directions_unfinished_double_ships

    """
    def find_double_middle_ships(self):
        double_middle_ships = []
        directions_double_middle_ships = []
        for index in range(64):
            if self.entries[index] == "m":
                if get_row_from_index(index) == get_row_from_index(index + 1) and self.entries[index + 1] == "m":
                    double_middle_ships.append(index)
                    directions_double_middle_ships.append("x")
                elif get_row_from_index(index + 8) < 8 and self.entries[index + 8] == "m":
                    double_middle_ships.append(index)
                    directions_double_middle_ships.append("y")
        return double_middle_ships, directions_double_middle_ships
    """

    def find_quadruple_ships(self):
        quadruple_ships = []
        directions_quadruple_ships = []
        for index in range(64):
            if self.entries[index] == "l":
                if self.entries[index + 1] == "m" and self.entries[index + 2] == "m":
                    quadruple_ships.append(index)
                    directions_quadruple_ships.append("x")
            elif self.entries[index] == "u":
                if self.entries[index + 8] == "m" and self.entries[index + 2] == "m":
                    quadruple_ships.append(index)
                    directions_quadruple_ships.append("y")
        return quadruple_ships, directions_quadruple_ships

    def no_errors(self, done=False):
        for n in self.numbers:
            if n < 0:
                return False
        single_ships = self.find_single_ships()
        double_ships, double_directions, unfinished_single_ships, unfinished_single_directions = \
            self.find_double_ships_and_unfinished_single_ships()
        triple_ships, triple_directions, unfinished_double_ships, unfinished_double_directions = \
            self.find_triple_ships_and_unfinished_double_ships()
        quadruple_ships, quadruple_directions = self.find_quadruple_ships()
        if b_ne(len(single_ships), 4, done) or b_ne(len(double_ships), 3, done) or b_ne(len(triple_ships), 2, done) or \
                b_ne(len(quadruple_ships), 1, done):
            return False
        for single_ship in single_ships:
            surrounding_indices = get_indices_surrounding_ship(single_ship, 1)
            for index in surrounding_indices:
                if self.entries[index] not in [".", "x"]:
                    return False
        for double_ship, direction in \
                zip(double_ships + unfinished_single_ships, double_directions + unfinished_single_directions):
            surrounding_indices = get_indices_surrounding_ship(double_ship, 2, direction)
            for index in surrounding_indices:
                if self.entries[index] not in [".", "x"]:
                    return False
        for triple_ship, direction in \
                zip(triple_ships + unfinished_double_ships, triple_directions + unfinished_double_directions):
            surrounding_indices = get_indices_surrounding_ship(triple_ship, 3, direction)
            for index in surrounding_indices:
                if self.entries[index] not in [".", "x"]:
                    return False
        for quadruple_ship, direction in zip(quadruple_ships, quadruple_directions):
            surrounding_indices = get_indices_surrounding_ship(quadruple_ship, 4, direction)
            for index in surrounding_indices:
                if self.entries[index] not in [".", "x"]:
                    return False
        return True

    def possible_indices_for_ship(self, length, direction="x"):  # both directions
        indices = []
        loop_through_indices = []
        if direction == "x":
            for index in range(64):
                if index % 8 + (length - 1) < 8:
                    loop_through_indices.append(index)
        else:  # "y"
            for index in range(64):
                if get_row_from_index(index) + (length - 1) < 8:
                    loop_through_indices.append(index)
        for index in loop_through_indices:
            s_row = [length] * length if direction == "x" else [1] * length
            s_column = [1] * length if direction == "x" else [length] * length
            ship_indices = get_ship_indices(index, length, direction)
            for k, i in enumerate(ship_indices):
                if self.entries[i] != ".":
                    if direction == "x":
                        s_row = list(map(lambda x: x - 1, s_row))
                        s_column[k] -= 1
                    else:
                        s_row[k] -= 1
                        s_column = list(map(lambda x: x - 1, s_column))
            if all([self.numbers[get_column_from_index(i)] >= s_column[k] and
                    self.numbers[8 + get_row_from_index(i)] >= s_row[k] for k, i in enumerate(ship_indices)]):
                legal_ship_indices = get_legal_ship_indices(length, direction)
                surrounding_indices = get_indices_surrounding_ship(index, length, direction)
                if all([self.entries[i] in legal_ship_indices[k] for k, i in enumerate(ship_indices)]) and \
                        not (self.entries[ship_indices[0]] == "l" and self.entries[ship_indices[-1]] == "r") and \
                        not (self.entries[ship_indices[0]] == "u" and self.entries[ship_indices[-1]] == "d") and \
                        all([self.entries[i] in [".", "x"] for i in surrounding_indices]):
                    indices.append(index)
        return indices

    def place_ship(self, index, length, direction="x"):
        ship_indices = get_ship_indices(index, length, direction)
        if length == 1:
            row = get_row_from_index(index)
            column = get_column_from_index(index)
            self.entries[index] = "o"
            self.numbers[column] -= 1
            self.numbers[8 + row] -= 1
        else:
            for k, index in enumerate(ship_indices):
                if self.entries[index] == ".":
                    row = get_row_from_index(index)
                    column = get_column_from_index(index)
                    if k == 0:
                        self.entries[index] = "l" if direction == "x" else "u"
                    elif k == length - 1:
                        self.entries[index] = "r" if direction == "x" else "d"
                    else:
                        self.entries[index] = "m"
                    self.numbers[column] -= 1
                    self.numbers[8 + row] -= 1

    def solve(self):
        dq = deque()
        dq.append((self.entries, self.numbers))
        while len(dq):
            dq_entries, dq_numbers = dq.pop()
            self.entries, self.numbers = dq_entries, dq_numbers

            """
            print("#" * 30)
            print(self)
            for q in dq:
                print("-" * 30)
                print(Bimaru(q[0], q[1]))
            print("#" * 30)
            """

            if self.no_errors():  # else skip
                len_next_ship = -1
                ships, directions = self.find_quadruple_ships()  # <==> first
                if len(ships) < 1:
                    len_next_ship = 4
                else:
                    ships, ships_u, directions, directions_u = self.find_triple_ships_and_unfinished_double_ships()
                    if len(ships) < 2:
                        len_next_ship = 3
                    else:
                        ships, ships_u, directions, directions_u = self.find_double_ships_and_unfinished_single_ships()
                        if len(ships) < 3:
                            len_next_ship = 2
                        else:
                            ships = self.find_single_ships()
                            if len(ships) < 4:
                                len_next_ship = 1

                if len_next_ship == -1:  # done
                    dq.clear()
                    break

                indices_x = self.possible_indices_for_ship(len_next_ship, direction="x")
                indices_y = self.possible_indices_for_ship(len_next_ship, direction="y")

                for index in indices_x:
                    copy_bimaru = Bimaru(self.entries[:], self.numbers[:])
                    copy_bimaru.place_ship(index, len_next_ship, direction="x")
                    dq.append((copy_bimaru.entries, copy_bimaru.numbers))
                for index in indices_y:
                    copy_bimaru = Bimaru(self.entries[:], self.numbers[:])
                    copy_bimaru.place_ship(index, len_next_ship, direction="y")
                    dq.append((copy_bimaru.entries, copy_bimaru.numbers))

        # assert self.no_errors(done=True)
        print("\nBimaru solved.", end="\n\n")
        print(self)


def get_ship_indices(index, length, direction="x"):  # index → top left
    if direction == "x":
        return list(range(index, index + length))
    else:
        return list(range(index, index + (length - 1) * 8 + 1, 8))


def get_legal_ship_indices(length, direction="x"):
    if length == 1:
        return [["."]]
    elif length == 2:
        if direction == "x":
            return [[".", "l"], [".", "r"]]
        else:
            return [[".", "u"], [".", "d"]]
    elif length == 3:
        if direction == "x":
            return [[".", "l"], [".", "m"], [".", "r"]]
        else:
            return [[".", "u"], [".", "m"], [".", "d"]]
    elif length == 4:
        if direction == "x":
            return [[".", "l"], [".", "m"], [".", "m"], [".", "r"]]
        else:
            return [[".", "u"], [".", "m"], [".", "m"], [".", "d"]]


def get_indices_surrounding_ship(index, length, direction="x"):  # index → top left
    index_row = get_row_from_index(index)
    index_column = get_column_from_index(index)
    ship_indices = get_ship_indices(index, length, direction)
    indices = []
    if length == 1:
        row_distance = 2
        column_distance = 2
    elif length == 2:
        if direction == "x":
            row_distance = 2
            column_distance = 3
        else:
            row_distance = 3
            column_distance = 2
    elif length == 3:
        if direction == "x":
            row_distance = 2
            column_distance = 4
        else:
            row_distance = 4
            column_distance = 2
    else:
        if direction == "x":
            row_distance = 2
            column_distance = 5
        else:
            row_distance = 5
            column_distance = 2
    for row in range(index_row - 1, index_row + row_distance):
        for column in range(index_column - 1, index_column + column_distance):
            if 0 <= row < 8 and 0 <= column < 8 and row * 8 + column not in ship_indices:
                indices.append(row * 8 + column)
    return indices


def get_row_from_index(index):
    return (index - index % 8) // 8


def get_column_from_index(index):
    return index % 8


def b_ne(x, y, done=False):  # bigger? / not equal?
    return x > y if not done else x != y


# b = Bimaru(example_entries, example_numbers)


if __name__ == "__main__":
    print("Enter the bimaru row by row (top to bottom, '.' → empty):", end="\n\n")
    bimaru_entries = []
    for r in range(8):
        r_entries = input(f"Enter the row {r} entries as a comma separated tuple:\n")
        bimaru_entries.extend(r_entries.split(","))
    # remaining space [!]
    bimaru_numbers = input("Enter the eight column and eight row numbers as a (length 16) comma separated tuple:\n")
    bimaru = Bimaru(bimaru_entries, bimaru_numbers)
    print("\nPlease verify your starting entries:")
    print(bimaru)
    while True:
        answer = input("Do you want to make a correction? ('yes')\n")
        if answer.lower() in ["yes", '"yes"', '"yes"', "y"]:
            correction = input("Enter the row, column, and corrected entry as a comma separated tuple: (0-based)\n")
            correction = correction.split(",")
            bimaru.entries[int(correction[0]) * 9 + int(correction[1])] = correction[2]
            print("\n", bimaru, sep="")
        else:
            if not bimaru.no_errors():
                print("\nPlease verify your entries again:")
                print(bimaru)
            else:
                break
    bimaru.solve()
