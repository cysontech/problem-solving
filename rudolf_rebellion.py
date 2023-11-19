# 코드트리 루돌프의 반란
# 선언
p_dict = {} # 산타정보
dx = [-1, -1, 0, 1, 1, 1, 0, -1] # 상 우 하 좌
dy = [0, 1, 1, 1, 0, -1, -1, -1]
n, m, p, c, dd = map(int, input().split())
rx, ry = map(lambda x:(int(x)-1), input().split()) # 루돌프 초기 위치
board = [[0]*n for _ in range(n)]
for i in range(1, p+1):
    pn, sx, sy = map(lambda x:(int(x)-1), input().split())
    p_dict[pn+1] = [sx, sy, 0, 0, 0, 0]
    board[sx][sy] = pn+1
board[rx][ry] = -1

# 함수
def get_dst(x1, y1, x2, y2):
    return (x1-x2) ** 2 + (y1-y2) ** 2

def rudolf_move():
    global board, p_dict, p, rx, ry
    min_dst = 1e9
    min_d = 0
    cand = []
    for i in range(1, p+1):
        p_elem = p_dict[i]
        px, py, out = p_elem[0], p_elem[1], p_elem[3]
        if not out:
            p_dst = get_dst(rx, ry, px, py)
            cand.append([p_dst, px, py, i])
    cand.sort(key=lambda x:(x[0], -x[1], -x[2]))
    target_p = cand[0][3] # 충돌 대상
    target_x, target_y = cand[0][1], cand[0][2]
    cand_l = []
    for i in range(8):
        nx = rx+dx[i]
        ny = ry+dy[i]
        n_dst = get_dst(nx, ny, target_x, target_y)
        cand_l.append([n_dst, nx, ny, i])
    cand_l.sort(key=lambda x:(x[0], -x[1], -x[2]))
    min_d = cand_l[0][3]
    board[rx][ry] = 0
    rx, ry = rx + dx[min_d], ry + dy[min_d]

    if board[rx][ry] > 0:
        p_dict[target_p][2] = 1
        rudolf_collision(rx, ry, target_p, min_d)
    board[rx][ry] = -1

def rudolf_collision(x, y, p_num, dir):# 루돌프의 충돌
    global p_dict, c, board
    p_dict[p_num][4] += c # 점수 얻음
    p_dict[p_num][0] += dx[dir]*c
    p_dict[p_num][1] += dy[dir]*c
    nx, ny = p_dict[p_num][0], p_dict[p_num][1]
    if 0<=nx<n and 0<=ny<n:
        nnx, nny = nx, ny
        if board[nx][ny] > 0:
            # 상호작용
            c_p = board[nx][ny]
            while c_p != 0:
                n_p = c_p # 현재 이동할 산타
                nnx += dx[dir] # 산타가 이동할 좌표
                nny += dy[dir]
                if 0<=nnx<n and 0<=nny<n: # 산타가 이동할 좌표가 보드 내인경우
                    c_p = board[nnx][nny] # 그 칸에 있는 사람(or x)
                    board[nnx][nny] = n_p # 밀어내고 이동
                    p_dict[n_p][0], p_dict[n_p][1] = nnx, nny
                else: # 보드 밖인경우
                    p_dict[n_p][3] = 1 # 탈락처리
                    break
        board[nx][ny] = p_num
    else: # 밖으로 나감
        p_dict[p_num][3] = 1

def santa_move():
    global p_dict, board, rx, ry, n

    for i in range(1, p+1):
        if p_dict[i][2] > 0 or p_dict[i][3] > 0:
            continue
        p_elem = p_dict[i]
        x, y = p_elem[0] ,p_elem[1]
        min_dst = 1e9
        min_d = 0
        flag = 0
        a_dst = get_dst(x, y, rx, ry)
        for d in range(0, 8, 2):
            nx = x + dx[d]
            ny = y + dy[d]
            if (not (0<=nx<n and 0<=ny<n)) or board[nx][ny] > 0:
                continue
            flag = 1
            c_dst = get_dst(rx, ry, nx, ny)
            if c_dst < min_dst:
                min_d = d
                min_dst = c_dst
        if flag == 1: # 움직일 수 있어도 루돌프로부터 가까워질 수 없으면 움직이지 않음
            if min_dst >= a_dst:
                flag = 0
        if flag == 0:
            continue
        else:
            board[x][y] = 0
            nx = x + dx[min_d]
            ny = y + dy[min_d]
            p_dict[i][0], p_dict[i][1] = nx, ny
            if board[nx][ny] == -1:
                p_dict[i][2] = 1
                santa_collision(nx, ny, i, min_d)
            else:
                board[nx][ny] = i

def santa_collision(x, y, p_num, dir):# 산타의 충돌
    global p_dict, dd, board
    dir = (dir+4)%8
    p_dict[p_num][4] += dd # 점수 얻음
    p_dict[p_num][0] += dx[dir]*dd
    p_dict[p_num][1] += dy[dir]*dd
    nx, ny = p_dict[p_num][0], p_dict[p_num][1]
    if 0<=nx<n and 0<=ny<n:
        nnx, nny = nx, ny
        if board[nx][ny] > 0:
            # 상호작용
            c_p = board[nx][ny]
            while c_p != 0:
                n_p = c_p # 현재 이동할 산타
                nnx += dx[dir] # 산타가 이동할 좌표
                nny += dy[dir]
                if 0<=nnx<n and 0<=nny<n: # 산타가 이동할 좌표가 보드 내인경우
                    c_p = board[nnx][nny] # 그 칸에 있는 사람(or x)
                    board[nnx][nny] = n_p # 밀어내고 이동
                    p_dict[n_p][0], p_dict[n_p][1] = nnx, nny
                else: # 보드 밖인경우
                    p_dict[n_p][3] = 1 # 탈락처리
                    break
        board[nx][ny] = p_num
    else: # 밖으로 나감
        p_dict[p_num][3] = 1

def p_check():
    global board, n, p_dict
    flag = 0
    for x in range(n):
        for y in range(n):
            if board[x][y] > 0:
                flag = 1
                p_dict[board[x][y]][4] += 1
    if flag == 0:
        return False
    else:
        return True

# 실행
for i in range(m):
    for j in range(1, p+1):
        if p_dict[j][2] == 2:
            p_dict[j][2] = 0
        if p_dict[j][2] == 1:
            p_dict[j][2] += 1
    rudolf_move()
    santa_move()
    if not p_check():
        break

for i in range(1, p+1):
    print(p_dict[i][4], end = ' ')

