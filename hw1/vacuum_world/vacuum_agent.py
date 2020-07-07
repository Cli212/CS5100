import argparse
#
import random
import re

def print_grid(grid,x,y,wlines):
    for row in range(weight):
        if row == x:
            l = grid[row].copy()
            l.insert(y,'[')
            l.insert(y+2,']')
            print(' '.join([str(i) for i in l]))
            wlines.append(' '.join([str(i) for i in l]))
        else:
            print(' '.join([str(i) for i in grid[row]]))
            wlines.append(' '.join([str(i) for i in grid[row]]))
    return wlines

def reflex(grid,x,y,moves,weight,height):
    ops = ['L', 'R', 'U', 'D']
    performance = 0
    index = 0
    wlines = []
    while moves:
        if grid[x][y]>0:
            performance+=grid[x][y]
            op = 'S'
            grid[x][y] = 0
        else:
            op = random.sample(ops,1)[0]
            if op == 'L':
                if y==0:
                    pass
                else:
                    y-=1
            elif op == 'R':
                if y==height-1:
                    pass
                else:
                    y+=1
            elif op == 'U':
                if x==0:
                    pass
                else:
                    x-=1
            elif op == 'D':
                if x==weight-1:
                    pass
                else:
                    x+=1
        print(f'{op} {performance}')
        wlines.append(f'{op} {performance}')
        moves -= 1
        index += 1
        if index%5 == 0:
            wlines = print_grid(grid, x, y, wlines)
    with open('output_partA1.txt', 'w') as f:
        for i in wlines:
            f.write(i + '\n')

def reflex_greedy(grid,x,y,moves,weight,height):
    ops = ['L', 'R', 'U', 'D']
    performance = 0
    index = 0
    wlines = []
    while moves:
        if grid[x][y] > 0:
            performance += grid[x][y]
            op = 'S'
            grid[x][y] = 0
        else:
            steps = []
            for op in ops:
                x1 = x
                y1 = y
                if op == 'L':
                    if y1 == 0:
                        continue
                    else:
                        y1 -= 1
                elif op == 'R':
                    if y1 == height - 1:
                        continue
                    else:
                        y1 += 1
                elif op == 'U':
                    if x1 == 0:
                        continue
                    else:
                        x1 -= 1
                elif op == 'D':
                    if x1 == weight - 1:
                        continue
                    else:
                        x1 += 1
                if steps != []:
                    if grid[steps[0][1]][steps[0][2]] < grid[x1][y1]:
                        while steps != []:
                            steps.pop()
                    elif grid[steps[0][1]][steps[0][2]] == grid[x1][y1]:
                        pass
                    else:
                        continue
                steps.append((op,x1,y1))
            step = random.sample(steps,1)[0]
            op = step[0]
            x = step[1]
            y = step[2]

        print(f'{op} {performance}')
        wlines.append(f'{op} {performance}')
        moves -= 1
        index += 1
        if index % 5 == 0:
            wlines = print_grid(grid, x, y, wlines)
    with open('output_partB1.txt', 'w') as f:
        for i in wlines:
            f.write(i + '\n')


def model_reflex(grid,x,y,moves,weight,height):
    ops = ['L', 'R', 'U', 'D']
    performance = 0
    index = 0
    wlines = []
    memory = [[False for i in range(height)] for j in range(weight)]
    while moves:
        if grid[x][y] > 0:
            performance += grid[x][y]
            op = 'S'
            grid[x][y] = 0
            memory[x][y] = True
        else:
            steps = []
            for op in ops:
                x1 = x
                y1 = y
                if op == 'L':
                    if y1 == 0:
                        continue
                    else:
                        y1 -= 1
                        if memory[x1][y1]:
                            continue
                elif op == 'R':
                    if y1 == height - 1:
                        continue
                    else:
                        y1 += 1
                        if memory[x1][y1]:
                            continue
                elif op == 'U':
                    if x1 == 0:
                        continue
                    else:
                        x1 -= 1
                        if memory[x1][y1]:
                            continue
                elif op == 'D':
                    if x1 == weight - 1:
                        continue
                    else:
                        x1 += 1
                        if memory[x1][y1]:
                            continue
                if steps != []:
                    if grid[steps[0][1]][steps[0][2]] < grid[x1][y1]:
                        while steps != []:
                            steps.pop()
                    elif grid[steps[0][1]][steps[0][2]] == grid[x1][y1]:
                        pass
                    else:
                        continue
                steps.append((op, x1, y1))
            step = random.sample(steps, 1)[0]
            op = step[0]
            x = step[1]
            y = step[2]

        print(f'{op} {performance}')
        wlines.append(f'{op} {performance}')
        moves -= 1
        index += 1
        if index % 5 == 0:
            wlines = print_grid(grid, x, y,wlines)
    with open('output_partC1.txt','w') as f:
        for i in wlines:
            f.write(i+'\n')

if __name__ == '__main__':
    with open('environ.txt','r') as f:
        lines = f.readlines()
    grid = []
    for line in lines:
        line = re.sub('\\s+',' ',line).strip().lstrip()
        if line.split(':')[0] == 'GRID':
            weight = int(line.split(':')[1].lstrip().split(' ')[0])
            height = int(line.split(':')[1].lstrip().split(' ')[1])
        elif line.split(':')[0] == 'INITIAL':
            init_x = int(line.split(':')[1].lstrip().split(' ')[0])-1
            init_y = int(line.split(':')[1].lstrip().split(' ')[1])-1
        elif line.split(':')[0] == 'MOVES':
            moves = int(line.split(':')[1])
        elif line.split(':')[0] == 'DIRT':
            continue
        else:
            grid.append([float(i) for i in line.lstrip().split(' ')])
    assert len(grid) == weight and len(grid[0]) == height
    parser = argparse.ArgumentParser(description="geography parser")
    parser.add_argument('-q','--ques',default=1)
    args = parser.parse_args()
    if args.ques == '1':
        reflex(grid,init_x,init_y,moves,weight,height)
    elif args.ques == '2':
        reflex_greedy(grid,init_x,init_y,moves,weight,height)
    else:
        model_reflex(grid,init_x,init_y,moves,weight,height)
