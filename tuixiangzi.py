# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 01:31:19 2021

@author: wyx
"""

def solve(grid, pos, targets):
    # 0-空地
    # 1-箱子
    # 2-悬崖
    # state: (((1,1,1), (2,2,2), (3,3,3)), (x, y))
    def done(state, targets):
        for target in targets:
            if state[target[0]][target[1]] != 1:
                return False
        return True
    
    def get_state(grid, pos):
        def dfs(grid, i, j, idx):
            grid[i][j] = idx
            if i-1 >= 0 and grid[i-1][j] == 0:
                dfs(grid, i-1, j, idx)
            if j-1 >= 0 and grid[i][j-1] == 0:
                dfs(grid, i, j-1, idx)
            if i+1 < len(grid) and grid[i+1][j] == 0:
                dfs(grid, i+1, j, idx)
            if j+1 < len(grid[0]) and grid[i][j+1] == 0:
                dfs(grid, i, j+1, idx)
        idx = -1
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 0:
                    dfs(grid, i, j, idx)
                    idx -= 1
        return (tuple(map(tuple, grid)), grid[pos[0]][pos[1]])
    
    def get_actions(state):
        # 上下左右
        grid = state[0]
        pos = state[1]
        actions = []
        cnt = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    if i+1 < len(grid) and grid[i+1][j] == pos and i-1 >= 0 and grid[i-1][j] not in {1, 2}:
                        actions.append(cnt*4+0)
                    if i-1 >= 0 and grid[i-1][j] == pos and i+1 < len(grid) and grid[i+1][j] not in {1, 2}:
                        actions.append(cnt*4+1)
                    if j+1 < len(grid[0]) and grid[i][j+1] == pos and j-1 >= 0 and grid[i][j-1] not in {1, 2}:
                        actions.append(cnt*4+2)
                    if j-1 >= 0 and grid[i][j-1] == pos and j+1 < len(grid[0]) and grid[i][j+1] not in {1, 2}:
                        actions.append(cnt*4+3)
                    cnt += 1
        return actions
    
    def take_action(state, action):
        num, option = divmod(action, 4)
        grid = list(map(list, state[0]))
        pos = state[1]
        cnt = 0
        for i in range(len(state[0])):
            for j in range(len(state[0][0])):
                if grid[i][j] == 1:
                    if cnt == num:
                        grid[i][j] = 0
                        if option == 0:
                            grid[i-1][j] = 1
                        elif option == 1:
                            grid[i+1][j] = 1
                        elif option == 2:
                            grid[i][j-1] = 1
                        else:
                            grid[i][j+1] = 1
                        pos = (i, j)
                    cnt += 1
                elif grid[i][j] < 0:
                    grid[i][j] = 0
        return get_state(grid, pos)
        
    def helper(state, res, states):
        actions = get_actions(state)
        for action in actions:
            next_state = take_action(state, action)
            res.append(action)
            if done(next_state[0], targets):
                return True
            if next_state in states:
                res.pop()
            else:
                states.add(next_state)
                flag = helper(next_state, res, states)
                if flag:
                    return True
                else:
                    res.pop()
        return False
    
    state = get_state(grid, pos)
    states = {state}
    res = []
    helper(state, res, states)
    return res
m = int(input('请输入行数：'))
print('请输入地图：')
print('0-空地（包括目的地）\n1-箱子（包括目的地上的箱子）\n2-墙体\n同一行之间不用空格，换行时输入回车')
grid = []
for i in range(m):
    grid.append(list(map(int, input())))
pos = tuple(map(int, input('请输入角色坐标，左上角为00，其右边为01：')))
raw = list(map(int, input('请输入目的地坐标，多个目的地之间不用分隔，如0001表示左上角与其右边的格子均为目的地：')))
targets = []
for i in range(len(raw)//2):
    targets.append((raw[2*i], raw[2*i+1]))
res = solve(grid, pos, targets)
orders = []
dic = {
    0: '上',
    1: '下',
    2: '左',
    3: '右',
}
for order in res:
    div, mod = divmod(order, 4)
    orders.append(str(div)+dic[mod])
print('\n\n每步移动的指令为箱子的编号（当前地图中从上往下从左往右的箱子编号，从0开始数）与箱子移动的方向：\n')
print(orders)
