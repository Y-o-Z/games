# Vier Gewinnt (the first player can always win (with perfect play))
# (..)

# 6x7 grid, the goal is to connect four disc (h, v, d)

# . → ?, o → disc

import random
import sys
import time

RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

color = {0: RESET, 1: RED, 2: BLUE}


class VierGewinnt:
    def __init__(self):
        self.entries = ["." for _ in range(42)]
        self.colors = [0 for _ in range(42)]

    def __repr__(self):
        rows = ["vier gewinnt:\n"]
        for row in range(6):
            current_row = []
            for column in range(7):
                current_row.append(f"{color[self.colors[row * 7 + column]]}{self.entries[row * 7 + column]}{RESET}")
            rows.append("  ".join(current_row) + "\n")
        return "".join(rows)

    def reset(self):
        self.entries = ["." for _ in range(42)]
        self.colors = [-1 for _ in range(42)]

    def column_space(self, column):
        space = 0
        for row in range(6):
            if self.entries[row * 7 + column] == ".":
                space += 1
        return space

    def play_column(self, column, player=1):  # 1, 2
        if not isinstance(column, int) and 0 <= column <= 6:
            return -1
        row = self.column_space(column) - 1
        if row < 0:  # no space
            return 0
        else:
            self.entries[row * 7 + column] = "o"
            self.colors[row * 7 + column] = player
            return 1

    def play_column_automatically(self):
        valid_columns = []
        for column in range(7):
            if self.column_space(column) != 0:
                valid_columns.append(column)
        column = valid_columns[random.randint(0, len(valid_columns)) - 1]
        self.play_column(column, player=2)

    def colors_at_indices_equal(self, indices):
        return self.colors[indices[0]] == self.colors[indices[1]] == self.colors[indices[2]] \
               == self.colors[indices[3]]

    def game_over(self):  # (double counting (doesn't matter))
        p1_count = 0
        p2_count = 0
        for index in range(42):
            for direction in range(8):
                indices = get_eight_direction_indices(index, direction)
                if indices:  # not empty
                    if all([self.entries[i] == "o" for i in indices]) and self.colors_at_indices_equal(indices):
                        if self.colors[index] == 1:
                            p1_count += 1
                        else:  # 2
                            p2_count += 1
        if p1_count > 1 and p2_count > 1:
            return 0  # draw
        elif p1_count > 1:
            return 1
        elif p2_count > 1:
            return 2
        else:
            if all([self.entries[index] == "o" for index in range(42)]):
                return 0
            else:
                return -1  # not over


def get_eight_direction_indices(index, direction=0):  # 0 is straight up, then clockwise
    indices = [index]
    for _ in range(1, 4):
        if direction == 0:
            indices.append(indices[-1] - 7)
        if direction == 1:
            indices.append(indices[-1] - 7 + 1)
        if direction == 2:
            indices.append(indices[-1] + 1)
        if direction == 3:
            indices.append(indices[-1] + 7 + 1)
        if direction == 4:
            indices.append(indices[-1] + 7)
        if direction == 5:
            indices.append(indices[-1] + 7 - 1)
        if direction == 6:
            indices.append(indices[-1] - 1)
        if direction == 7:
            indices.append(indices[-1] - 7 - 1)
    if all([0 <= index <= 41 for index in indices]):
        return indices
    else:
        return []


if __name__ == "__main__":
    print("#" * 28, "# Welcome to Vier Gewinnt! #", "#" * 28, sep="\n", end="\n\n")
    try:
        mode = int(input("Press 2 to play against the computer, 1 to play against yourself. "))  # 1 → else
    except:
        sys.exit("Bad input.")
    v_g = VierGewinnt()
    switch = True
    if mode == 2:
        print("So you wish to loose against the computer...")
    else:
        print("So you wish to loose against yourself...")
    time.sleep(1)
    print("-" * 30, v_g, "-" * 30, sep="\n")
    time.sleep(1)
    while v_g.game_over() == -1:
        if mode == 2:
            if switch:
                v_g.play_column_automatically()
                print("-" * 30, v_g, "-" * 30, sep="\n")
                if v_g.game_over() == 2:
                    print("You loose!!!")
                    break
                elif v_g.game_over() == 0:
                    print("We both loose!!!")
                    break
                switch = not switch
            else:
                c = int(input("What column would you like to play? (0..6)  "))
                while True:
                    flag = v_g.play_column(c, player=1)
                    if flag == 1:
                        break
                    else:
                        c = int(input("Bad input. What column would you like to play? (0..6)  "))
                print("-" * 30, v_g, "-" * 30, sep="\n")
                if v_g.game_over() == 1:
                    print("Victory!!!")
                    break
                elif v_g.game_over() == 0:
                    print("We both win!!!")
                    break
                switch = not switch
        else:  # 1
            c = int(input("What column would you like to play? (0..6)  "))
            while True:
                flag = v_g.play_column(c, player=int(switch) + 1)
                if flag == 1:
                    break
                else:
                    c = int(input("Bad input. What column would you like to play? (0..6)  "))
            print("-" * 30, v_g, "-" * 30, sep="\n")
            if v_g.game_over() == 2 or v_g.game_over() == 1:
                print("Victory!!! / You loose!!!")
                break
            switch = not switch
