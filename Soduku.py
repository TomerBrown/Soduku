from random import Random
import random
import numpy as np
class Soduku:
    def __init__(self,board):
       assert_dimentions(board)
       self.board = board
       self.need_to_be_solved = count_zeros(board)

    @staticmethod
    def get_smaller_square(arr, i, j):
        nums = set();
        left = i - (i % 3)
        upper = j - (j % 3)
        smaller_cube = [[0,0,0],[0,0,0],[0,0,0]]
        for m in range (0,3):
            for n in range(0,3):
                nums.add(arr[left + m][upper + n])
        return nums

    @staticmethod
    def get_nums_in_row(arr,i,j):
        nums = set();
        for x in range(0,9):
           t = arr[x][j]
           nums.add(t)
        return nums

    @staticmethod
    def get_nums_in_line(arr,i,j):
        nums = set();
        for x in range(0,9):
           t = arr[i][x]
           nums.add(t)
        return nums

    @staticmethod
    def possible_numbers (arr,i,j):
        rows = Soduku.get_nums_in_row(arr,i,j)
        lines = Soduku.get_nums_in_line(arr,i,j)
        rl = rows.union(lines)
        sq = Soduku.get_smaller_square(arr,i,j)
        both = rl.union(sq)
        lst = [True,True,True,True,True,True,True,True,True,True]
        for num in both:
            lst [num]= False
        return [i for i in range(0,10) if lst[i]]


    def solve(self):
        while (self.need_to_be_solved>0):
            for i in range (0,9):
                for j in range (0,9):
                    num = self.board[i][j]
                    if (num==0):
                        possible = self.possible_numbers(self.board,i,j)
                        if (len(possible)==1):
                            self.board[i][j] = possible[0]
                            self.need_to_be_solved -=1
        for line in self.board:
            print (line)

    @staticmethod
    def generate():
        base = 3
        side = base * base

        # pattern for a baseline valid solution
        def pattern(r, c): return (base * (r % base) + r // base + c) % side

        # randomize rows, columns and numbers (of valid base pattern)
        from random import sample
        def shuffle(s): return sample(s, len(s))

        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))

        # produce board using randomized baseline pattern
        board = [[nums[pattern(r, c)] for c in cols] for r in rows]
        lst = []
        for i in range (9):
            for j in range (9):
                lst.append((i,j))
        random.shuffle(lst)
        for i in range (37):
            tup = lst[i]
            x = tup[0]
            y = tup[1]
            board[x][y]=0


        return Soduku(board)








def assert_dimentions(array):
    bol1 = len(array) ==9
    bol2 = True
    for row in array:
        if (len(row) != 9):
            bol2 = False
    assert bol1 and bol2

def count_zeros (array):
    count = 0
    for line in array:
        for number in line:
            if number ==0:
                count +=1
    return count




def test():
    line1 = [0,3,0,0,0,0,0,0,0]
    line2 = [0,4,0,0,5,0,0,1,0]
    line3 = [0,2,0,6,1,3,5,0,4]
    line4 = [0,0,6,8,0,2,0,0,5]
    line5 = [0,1,8,7,0,0,3,0,0]
    line6 = [7,0,3,1,0,6,2,0,8]
    line7 = [1,0,0,4,0,9,7,0,6]
    line8 = [9,0,0,3,7,8,4,0,1]
    line9 = [0,0,0,0,6,1,9,0,0]

    board = [line1,line2,line3,line4,line5,line6,line7,line8,line9]
    for line in board:
        print (line)
    soduku = Soduku(board)
    print ("-"*100)
    soduku.solve()
    print("-" * 100)
    soduku = Soduku.generate()
    for line in soduku.board:
        print(line)
    print("-" * 100)
    soduku.solve()




test()