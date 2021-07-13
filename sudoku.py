# Sudoku → japanisches Akronym (griech. akros, onyma = Spitze, Namen)
# (= dos(denial-of-service)-attack on the brain ..)

# 9x9 grid with 9 3x3 subgrids, each subgrid, row, and column contains the numbers 1..9 once (+ unique solution)

from collections import deque

legal_entries = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]


class Sudoku:
    """
    # list of 81 entries from top-left to bottom-right (-1 → empty)
    """
    def __init__(self, entries):
        self.entries = entries[:]
        self.original_entries = entries[:]

    def __repr__(self):
        rows = ["sudoku:\n"]
        for row in range(9):
            current_row = []
            for column in range(9):
                current_row.append(str(self.entries[row * 9 + column]))
                if current_row[-1][0] != "-":
                    current_row[-1] = " " + current_row[-1]
            rows.append(" ".join(current_row) + "\n")
        return "".join(rows)

    def reset(self):
        self.entries = self.original_entries[:]

    def no_duplicates(self, indices):
        # True if all entries (not -1) pointed to by indices are different
        entries = [self.entries[index] for index in indices]
        for entry in range(1, 9 + 1):
            if entries.count(entry) > 1:
                return False
        return True

    def no_errors(self):
        # no illegal entries
        if not (len(self.entries) == 81 and all(entry in legal_entries for entry in self.entries)):
            return False
        # all subgrids correct
        for subgrid in range(9):
            indices = get_indices_from_subgrid(subgrid)
            if not self.no_duplicates(indices):
                return False
        # all rows correct
        for row in range(9):
            indices = get_indices_from_row(row)
            if not self.no_duplicates(indices):
                return False
        # all columns correct
        for column in range(9):
            indices = get_indices_from_column(column)
            if not self.no_duplicates(indices):
                return False
        return True

    def possible_entries_for_index(self, index):
        if self.entries[index] != -1:
            return [self.entries[index]]
        impossible_entries = set()
        subgrid = get_subgrid_from_index(index)
        row = get_row_from_index(index)
        column = get_column_from_index(index)
        for i in get_indices_from_subgrid(subgrid):
            impossible_entries.add(self.entries[i])
        for i in get_indices_from_row(row):
            impossible_entries.add(self.entries[i])
        for i in get_indices_from_column(column):
            impossible_entries.add(self.entries[i])
        possible_entries = []
        for entry in range(1, 9 + 1):
            if entry not in impossible_entries:
                possible_entries.append(entry)
        return possible_entries

    def solve_next_entry(self, quiet=False):
        # return 1 for new_entry, 0 for no_new_entry, -1 for error
        possible_entries_for_indices = []
        # index level
        for index in range(81):
            if self.entries[index] == -1:
                possible_entries = self.possible_entries_for_index(index)
                if len(possible_entries) == 1:  # success
                    if not quiet:
                        row = get_row_from_index(index)
                        column = get_column_from_index(index)
                        print(f"New entry at row {row}, column {column}: {possible_entries[0]} [index level]")
                    self.entries[index] = possible_entries[0]
                    return 1
                possible_entries_for_indices.append(possible_entries)
            else:
                possible_entries_for_indices.append([self.entries[index]])
        for index in range(81):
            if not len(possible_entries_for_indices[index]):  # error check (empty)
                if not quiet:
                    row = get_row_from_index(index)
                    column = get_column_from_index(index)
                    print(f"Error at row {row}, column {column}: no possible entries")
                return -1
        # subgrid level
        for subgrid in range(9):
            indices = get_indices_from_subgrid(subgrid)
            subgrid_entries = set()
            for index in indices:
                subgrid_entries.add(self.entries[index])
            missing_subgrid_entries = []
            for entry in range(1, 9 + 1):
                if entry not in subgrid_entries:
                    missing_subgrid_entries.append(entry)
            for missing_entry in missing_subgrid_entries:
                count = 0
                pos = -1
                for index in indices:
                    if missing_entry in possible_entries_for_indices[index]:
                        count += 1
                        pos = index
                if count == 1:  # success
                    if not quiet:
                        row = get_row_from_index(pos)
                        column = get_column_from_index(pos)
                        print(f"New entry at row {row}, column {column}: {missing_entry} [subgrid level]")
                    self.entries[pos] = missing_entry
                    return 1
                elif count == 0:  # error check
                    if not quiet:
                        print(f"Error at subgrid {subgrid}: no place for {missing_entry}")
                    return -1
        # row level
        for row in range(9):
            indices = get_indices_from_row(row)
            row_entries = set()
            for index in indices:
                row_entries.add(self.entries[index])
            missing_row_entries = []
            for entry in range(1, 9 + 1):
                if entry not in row_entries:
                    missing_row_entries.append(entry)
            for missing_entry in missing_row_entries:
                count = 0
                pos = -1
                for index in indices:
                    if missing_entry in possible_entries_for_indices[index]:
                        count += 1
                        pos = index
                if count == 1:  # success
                    if not quiet:
                        column = get_column_from_index(pos)
                        print(f"New entry at row {row}, column {column}: {missing_entry} [row level]")
                    self.entries[pos] = missing_entry
                    return 1
                elif count == 0:  # error check
                    if not quiet:
                        print(f"Error at row {row}: no place for {missing_entry}")
                    return -1
        # column level
        for column in range(9):
            indices = get_indices_from_column(column)
            column_entries = set()
            for index in indices:
                column_entries.add(self.entries[index])
            missing_column_entries = []
            for entry in range(1, 9 + 1):
                if entry not in column_entries:
                    missing_column_entries.append(entry)
            for missing_entry in missing_column_entries:
                count = 0
                pos = -1
                for index in indices:
                    if missing_entry in possible_entries_for_indices[index]:
                        count += 1
                        pos = index
                if count == 1:  # success
                    if not quiet:
                        row = get_row_from_index(pos)
                        print(f"New entry at row {row}, column {column}: {missing_entry} [column level]")
                    self.entries[pos] = missing_entry
                    return 1
                elif count == 0:  # error check
                    if not quiet:
                        print(f"Error at column {column}: no place for {missing_entry}")
                    return -1
        if not quiet:
            print("No new entry.")
        return 0

    def solve(self):
        dq = deque()
        dq.append(self.entries[:])
        while len(dq):
            """
            print(f"dq: len = {len(dq)}")
            for dq_entry in dq:
                print_entries(dq_entry)
            """
            dq_entries = dq.pop()
            self.entries = dq_entries
            while True:
                flag = self.solve_next_entry(quiet=True)
                if flag == 1:  # new_entry
                    # print("\nFLAG = 1\n")
                    continue
                elif flag == 0:  # no new entry (→ dfs)
                    # terminated?
                    if all(entry in legal_entries[1:] for entry in self.entries):
                        dq.clear()
                        # print("\nDone.\n")
                        break
                    else:
                        for index in range(81):
                            if self.entries[index] == -1:
                                possible_entries = self.possible_entries_for_index(index)
                                for entry in possible_entries:
                                    self.entries[index] = entry
                                    dq.append(self.entries[:])  # [:] !
                                # print(f"\nFLAG = 0, entries added → len(dq) = {len(dq)}\n")
                                break
                else:  # flag = -1, error (← dfs)
                    # print("\nFLAG = -1\n")
                    break
        assert self.no_errors()
        if all(entry in legal_entries[1:] for entry in self.entries):
            print("\nSudoku solved.", end="\n\n")
            print(self)
        else:
            print("\nSudoku not solved. (why?)", end="\n\n")
            print(self)


def get_subgrid_from_index(index):
    # top-left to bottom-right, 0-based
    row = get_row_from_index(index)
    column = get_column_from_index(index)
    if row < 3:
        if column < 3:
            return 0
        elif column < 6:
            return 1
        else:
            return 2
    elif row < 6:
        if column < 3:
            return 3
        elif column < 6:
            return 4
        else:
            return 5
    else:
        if column < 3:
            return 6
        elif column < 6:
            return 7
        else:
            return 8


def get_row_from_index(index):
    # 0-based
    if index < 9:
        return 0
    elif index < 18:
        return 1
    elif index < 27:
        return 2
    elif index < 36:
        return 3
    elif index < 45:
        return 4
    elif index < 54:
        return 5
    elif index < 63:
        return 6
    elif index < 72:
        return 7
    else:
        return 8


def get_column_from_index(index):
    # 0-based
    return index % 9


def get_indices_from_subgrid(subgrid):
    # 0-based
    x = subgrid % 3
    if subgrid < 3:
        y = 0
    elif subgrid < 6:
        y = 1
    else:
        y = 2
    indices = []
    for row in range(3 * y, 3 * y + 3):
        for column in range(3 * x, 3 * x + 3):
            indices.append(row * 9 + column)
    return indices


def get_indices_from_row(row):
    # 0-based
    return list(range(row * 9, row * 9 + 9))


def get_indices_from_column(column):
    # 0-based
    return list(range(column, column + 8 * 9 + 1, 9))


def print_entries(entries):
    # quick & dirty
    print("-" * 10)
    for row in range(9):
        print(*entries[row * 9: row * 9 + 9])
    print("-" * 10)


if __name__ == "__main__":
    print("Enter the sudoku row by row (top to bottom, -1 → empty):", end="\n\n")
    sudoku_entries = []
    for r in range(9):
        r_entries = input(f"Enter the row {r} entries as a comma separated tuple:\n")
        sudoku_entries.extend(list(map(int, r_entries.split(","))))
    sudoku = Sudoku(sudoku_entries)
    print("\nPlease verify your starting entries:")
    print(sudoku)
    while True:
        answer = input("Do you want to make a correction? ('yes')\n")
        if answer.lower() in ["yes", '"yes"', '"yes"', "y"]:
            correction = input("Enter the row, column, and corrected entry as a comma separated tuple: (0-based)\n")
            correction = list(map(int, correction.split(",")))
            sudoku.entries[(correction[0]) * 9 + (correction[1])] = correction[2]
            print("\n", sudoku, sep="")
        else:
            if not sudoku.no_errors():
                print("\nPlease verify your entries again:")
                print(sudoku)
            else:
                break
    sudoku.solve()
