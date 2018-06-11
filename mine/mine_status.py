import numpy as np

class mine_status:

    def __init__(self, diff, level, dtype=np.int8):
        self.diff = diff
        self.level = level
        self.status = np.zeros(np.append(diff[level, 0:2]+2, 2), dtype)
        self.mines = list()

    def change_bomb_status(self, pos, stat):
        self.status[pos[0], pos[1], 0] = stat

    def change_flip_status(self, pos, stat):
        self.status[pos[0], pos[1], 1] = stat

    def get_bomb_status(self, pos):
        return self.status[pos[0], pos[1], 0]

    def get_flip_status(self, pos):
        return self.status[pos[0], pos[1], 1]

    def generate_bomb(self):
        mine_cnt = 0
        while True:
            x = np.random.randint(self.diff[self.level, 0])
            y = np.random.randint(self.diff[self.level, 1])
            if (x, y) not in self.mines:
                mines.append((x, y))
                change_bomb_status((x, y), -1)
                mine_cnt += 1
            if mine_cnt == self.diff[self.level, 2]:
                break
    def stat_cnt(mat, ind, value):
        cnt = 0
        for i in range(0,3):
            for j in range(0,3):
                if mat[i, j, ind]==value:
                    cnt += 1
        return cnt
            
    def cal_mine(self):
        for i in range(0, self.diff[self.level, 0]):
            for j in range(0, self.diff[self.level, 1]):
                if not get_bomb_status((i+1, j+1)) == -1:
                    mat = self.status[i:i+3, j:j+3, 0:1]
                    cnt = stat_cnt(mat, 0, -1)
                    change_bomb_status([i+1, j+1], cnt)

    def recur_none(self, pos):
        self.status[pos[0]-1:pos[0]+2, pos[1]-1:pos[1]+2, 1] = 1
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i ==0 and j == 0) and \
                   self.status[pos[0]+i,pos[1]+j, 0] == 0 and \
                   pos[0]+i>=1 and pos[0]+i<diff[level, 0]+1 and \
                   pos[1]+j>=1 and pos[1]+j<diff[level, 1]+1 and \
                   not check_rec((m_i+i, m_j+j)) == 0:
                        recur_none((m_i+i, m_j+j))

    def check_rec(self, pos):
        cnt = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.status[pos[0]+i, pos[1]+j, 1]==0:
                    cnt += 1
        return cnt

    def reset(self):
        self.status.fill(0)
        self.mines.clear()






