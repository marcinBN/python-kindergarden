#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os

square_dict = {}


square_map =[[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8]]


sudoku1 = """
           400 000 000
           005 000 300
           000 060 107
           
           000 075 000
           000 030 060
           960 000 040
           
           000 009 000
           000 000 000
           007 008 001
           """
sudoku = """
           060 104 050
           008 305 600
           200 000 001
           
           800 407 006
           006 000 300
           700 901 004
           
           500 000 002
           007 206 900
           040 508 070
           """
def print_sudoku(sudoku):
    assert len(sudoku) == 81
    pretty = ''
    pos = 0
    while pos < 81:
        pretty += sudoku[pos]
        if pos%3 == 2:
            if pos%27 == 26:
                pretty += '\n----+-----+----\n'
            else:
                if pos%9 == 8:
                    pretty += '\n'
                else:
                    pretty += ' | '
        pos += 1
    print(pretty)

def grid_sudoku(sudoku):
    assert len(sudoku) == 81
    grid = []
    pos = 0
    row = []
    while pos < 81:
        row.append(int(sudoku[pos]))
        if pos%9 == 8:
            grid.append(row)
            row = []
        pos += 1
    return grid

def pretty_grid(grid):
    os.system('clear')
    for row in grid:
        print(row)

def find_unassigned_location(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)
    return False

def noconflict_row(grid, row, guess):
    if guess not in grid[row]:
        return True
    else:
        return False

def noconflict_col(grid, col, guess):
    if guess not in [row[col] for row in grid]:
        return True
    else:
        return False

def noconflict_square(grid, row, col, guess):
    groups = group_grip(grid)
    group = calc_group(row, col)
    if guess not in groups[group]:
        return True
    else:
        return False

def noconflicts(grid, row, col, guess):
    if (noconflict_row(grid, row, guess) and
        noconflict_col(grid, col, guess) and
        noconflict_square(grid, row, col, guess)):
        return True
    else:
        return False

def calc_group(row, col):
    return square_map[row // 3][col // 3]

def group_grip(grip):
    d = {}
    for row in range(9):
        for col in range(9):
            d.setdefault(calc_group(row, col), []).append(grip[row][col])
    return d


def npos(row, col):
    if col == 8:
        row += 1
        col = 0
    else:
        col += 1
    return (row, col)

def SolveSudoku(grid):
    if not find_unassigned_location(grid):
        pretty_grid(grid)
        print('hura')
        return True
    else:
        row, col = find_unassigned_location(grid)
    
    for guess in range(1, 10):
        if noconflicts(grid, row, col, guess):
            grid[row][col] = guess
            if SolveSudoku(grid):
                return True
            grid[row][col] = 0

    return False


sudoku1 = ''.join(sudoku1.split())
grid = grid_sudoku(sudoku1)
row = 0
col = 4
guess = 9
SolveSudoku(grid)
