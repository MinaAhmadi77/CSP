#!/usr/bin/python3

from timeit import default_timer as timer
from csp import backtracking_search, mrv, unordered_domain_values, forward_checking, mac, no_inference, BinaryPuzzle


class Test:

    def __init__(self):
        self.original_board = []
        self.expected_sum = 0
    def set_board(self, which):
        inputFile = "../puzzles/puzzle" + str(which) + ".txt"
        self.n = -1
        with open(inputFile, "r") as inputBoard:
            borad_data = inputBoard.readlines()
            self.n = int(borad_data[0].split(" ")[0].strip())
            self.original_board = [[0 for j in range(self.n)] for i in range(self.n)]
        for i in range(self.n):
            self.original_board[i] = borad_data[i+1].strip().split(" ")

    def start(self, inf):
        s = BinaryPuzzle(self.original_board, self.n, self.expected_sum)

        self.start_ = timer()
        a = backtracking_search(s, select_unassigned_variable=mrv, order_domain_values=unordered_domain_values,
                                inference=inf)
        self.end_ = timer()
        if a:
            self.bt = s.n_bt
            self.solve = True
            self.solution = a
        else:
            self.solve = False
            self.solution = None

        #     print("\nSolution found")
        #    # for i in range(9):
        #     #    print(" ")
        #      #   for j in range(9):
        #       #      name = i * 9 + j
        #        #     print(" " + str(a["CELL"+str(name)]) + " ", end='')
        # else:
        #     print("\nPlease check the binary initial board, solution not found!")

    def display(self):
        time = round(self.end - self.start, 5)
        print("Time: " + str(time) + " seconds")
        print("N. BT: " + str(self.bt))
    
    def display_solution(self):
        if self.solve:
            for item in self.solution.keys():
                item = int(item)
                i = item // self.n
                j = item % self.n
                self.original_board[i][j] = self.solution[str(item)]
            A = (self.original_board)
            print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in A]))
            print("***********************************************************************")
def main():
    time = []
    back_track = []
    n_test = 1
    inf = no_inference
    for i in range(n_test):
        t1 = Test()
        t1.set_board(i)
        x = int(t1.n //3)
        y = x*2 + 1
        for expected_sum in range (x , y+1):
            t1.expected_sum = expected_sum
            t1.start(inf)
            res = t1.solve
            print(res)
            if res:
                back_track.append(t1.bt)
                time.append(round(t1.end_ - t1.start_, 5))
                t1.display_solution()
                break
        print("----------------------------------------------------")
    #print(time)
    #print("\naverage time:" + str(sum(time) / len(time)))
    #print("average bt:" + str(sum(back_track) / len(back_track)))

#if __name__ == '__main__':
main()
