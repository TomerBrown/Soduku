from random import Random
import random
import numpy as np
import copy


class Soduku:

    #Fields
    # board : board need to be solved - updates over time
    # need_to_solve_points : a list of coordinates (i,j,possibles) that still need to be solved.
    #possibles is a list of all possible values for that point
    def __init__(self, board,soloution=None,original=None):
        self.board = board
        self.need_to_solve_points = []
        self.solved =0
        self.soloution = soloution
        self.original = original
        for i in range (9):
            for j in range (9):
                if (self.board[i][j]==0):
                    self.need_to_solve_points.append((i,j))

    #checks if the insert does not violate propeties and inserts
    def insert (self,i,j,num):
        if (self.is_legit(i,j,num)):
            self.need_to_solve_points.remove((i,j))
            self.board[i][j]= num
            self.solved +=1
            print(self.solved, "out of",self.number_to_solve())

    #check if num in postion (i,j) does not violate row coloumn or square
    def is_legit(self,i,j,num):
        if num<1 or num >9: return False
        if (i,j) not in self.need_to_solve_points: return False
        if self.board[i][j]!=0: return False
        row = self.all_in_row(i)
        line = self.all_in_line(j)
        square = self.all_in_square(i,j)
        return (num not in row) and (num not in line) and (num not in square)

    #how many more left to solve
    def number_to_solve (self):
        return len (self.need_to_solve_points)

    #returns a set of all number in row
    def all_in_row (self,i):
        return set([self.board[i][j] for j in range (9)])

    #returns a set of all numbers in line
    def all_in_line(self, j):
        return set([self.board[i][j] for i in range(9)])

    # return a 3x3 square that contains (i,j)
    def square3x3 (self,i,j):
        square = [[0,0,0],[0,0,0],[0,0,0]]
        left = i-(i%3)
        up = j - (j%3)
        for l in range (3):
            for m in range (3):
                square [l][m] = self.board[left+l][up+m]
        return square

    # return a set of all numbers in square
    def all_in_square (self,i,j):
        s = set([])
        square = self.square3x3(i,j)
        for line in square:
            for num in line:
                s.add(num)
        return s

    def get_possibles (self,i,j):
        row = self.all_in_row(i)
        line = self.all_in_line(j)
        square = self.all_in_square(i,j)
        all = set([i for i in range (1,10)])
        return all - (square.union(row.union(line)))


    def unique_line (self,i,j):
        blank_line = [(i,x) for x in range(9) if x!=j and self.board[i][x]==0]
        point_possibles = self.get_possibles(i,j);
        all_other_possible = set([])
        for (x,y) in blank_line:
            all_other_possible = all_other_possible.union(self.get_possibles(x,y))
        point_possibles = point_possibles-all_other_possible
        if len(point_possibles)==1:
            self.insert(i,j,list(point_possibles)[0])

    def unique_row (self,i,j):
        blank_line = [(x,j) for x in range(9) if x!=i and self.board[x][j]==0]
        point_possibles = self.get_possibles(i,j);
        all_other_possible = set([])
        for (x,y) in blank_line:
            all_other_possible = all_other_possible.union(self.get_possibles(x,y))
        point_possibles = point_possibles-all_other_possible
        if len(point_possibles)==1:
            self.insert(i,j,list(point_possibles)[0])

    def unique_square(self, i, j):
        l = i-i%3
        u= j-j%3
        blank_line = []
        for x in range (l,l+3):
            for y in range (u,u+3):
                if not(x==i and y==j or self.board[x][y]!=0):
                    blank_line.append((x,y))
        point_possibles = self.get_possibles(i, j)
        all_other_possible = set([])
        for (x, y) in blank_line:
            all_other_possible = all_other_possible.union(self.get_possibles(x, y))
        point_possibles = point_possibles - all_other_possible
        if len(point_possibles) == 1:
            self.insert(i, j, list(point_possibles)[0])

    def unique_all (self,i,j):
        self.unique_row(i, j)
        self.unique_line(i,j)
        self.unique_square(i,j)

####################################################################################
    ## The method that solves the puzzle
    def solve(self):
        #if for two rounds no soloution should quit.
        #c is a counter for that
        c=0
        c2=0
        while (self.number_to_solve()>0):
            c += 1
            c2+=1
            #temp is used to see if something changed
            for (i,j) in self.need_to_solve_points:
                possibles = self.get_possibles(i,j)
                if (len(possibles)==1):
                    self.insert(i,j,list(possibles)[0])
                self.unique_all(i, j)
            if (c>=100):
                try:
                    self.insert(i,j,random.choice(list(possibles)))
                    tempboard = copy.deepcopy(self.board)
                    tempsolve = copy.deepcopy(self.need_to_solve_points)
                    c=0
                except:
                    c=0
                    self.board = tempboard
                    self.need_to_solve_points= tempsolve
            if c2>10000:
                return





        if (self.check_if_correct()):
            print ("Solved Correctly")
        else:
            print ("Mistake Found")
        for line in self.board:
            print (line)
##################################################################################
    def display (self):
        c1=0
        c2=0
        for line in self.board:
            for num in line:
                c1+=1
                print (num,end =" ")
                if c1==3:
                    c1=0
                    print ("|",end=" ")
            print("")

    def check_if_correct(self):
        for i in range(9):
            for j in range(9):
                line = self.all_in_line(i)
                row = self.all_in_row(j)
                square = self.all_in_square(i,j)
                if (len(line)!=9) or (len(row)!=9) or len(square)!=9: return False
            return True






    @staticmethod
    def generate(num_to_delete):
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
        print ("-"*100)
        print("-" * 100)
        for i in range (9):
            for j in range (9):
                lst.append((i,j))
        random.shuffle(lst)

        temp_board = copy.deepcopy(board)

        for i in range (num_to_delete):
            tup = lst[i]
            x = tup[0]
            y = tup[1]
            board[x][y]=0

        return Soduku(board,temp_board,copy.deepcopy(board))



def test():


    if (True):
        for i in range (100):
            soduku = Soduku.generate(46)
            print("-"*100)
            print ("*** test num",i,"***")
            soduku.display()
            print("-"*100)
            soduku.solve()




