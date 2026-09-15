from copy import deepcopy
from time import perf_counter
import tracemalloc

# ------------------------------------------------------------
# 問題
# ------------------------------------------------------------

board = [
    [0,8,0,2,0,0,4,0,0],
    [5,7,0,0,0,0,1,0,0],
    [0,0,2,3,0,0,0,0,0],

    [8,2,0,0,9,0,0,0,5],
    [0,0,0,7,1,5,0,0,0],
    [7,0,0,0,2,0,0,4,1],

    [0,0,0,0,0,6,7,0,0],
    [0,0,3,0,0,0,0,1,8],
    [0,0,7,0,0,9,0,5,0],
]



# ------------------------------------------------------------
# 統計
# ------------------------------------------------------------

class Stats:

    def __init__(self):
        self.nodes = 0          # 探索ノード数
        self.backtracks = 0     # 戻った回数


stats = Stats()


# ------------------------------------------------------------
# 候補計算
# ------------------------------------------------------------

def candidates(board, r, c):

    if board[r][c] != 0:
        return set()

    cand = set(range(1,10))

    # 行
    cand -= set(board[r])

    # 列
    cand -= {board[i][c] for i in range(9)}

    # ブロック
    br = (r//3)*3
    bc = (c//3)*3

    for i in range(br, br+3):
        for j in range(bc, bc+3):
            cand.discard(board[i][j])

    return cand



# ------------------------------------------------------------
# 制約伝播
# ------------------------------------------------------------

def constraint_propagation(board):

    while True:

        changed = False


        # Naked Single
        for r in range(9):
            for c in range(9):

                if board[r][c] != 0:
                    continue

                cand = candidates(board,r,c)

                if len(cand) == 0:
                    return False

                if len(cand) == 1:
                    board[r][c] = cand.pop()
                    changed = True


        # Hidden Single（行）
        for r in range(9):

            for num in range(1,10):

                pos = []

                for c in range(9):

                    if board[r][c] == 0 and num in candidates(board,r,c):
                        pos.append(c)

                if len(pos) == 1:
                    board[r][pos[0]] = num
                    changed = True



        # Hidden Single（列）
        for c in range(9):

            for num in range(1,10):

                pos = []

                for r in range(9):

                    if board[r][c] == 0 and num in candidates(board,r,c):
                        pos.append(r)

                if len(pos) == 1:
                    board[pos[0]][c] = num
                    changed = True



        # Hidden Single（ブロック）
        for br in range(0,9,3):

            for bc in range(0,9,3):

                for num in range(1,10):

                    pos = []

                    for r in range(br,br+3):
                        for c in range(bc,bc+3):

                            if board[r][c] == 0 and num in candidates(board,r,c):
                                pos.append((r,c))

                    if len(pos) == 1:
                        r,c = pos[0]
                        board[r][c] = num
                        changed = True


        if not changed:
            break


    return True



# ------------------------------------------------------------
# 候補最少マス(MRV)
# ------------------------------------------------------------

def find_best_cell(board):

    best = None
    best_candidate = None


    for r in range(9):
        for c in range(9):

            if board[r][c] != 0:
                continue

            cand = candidates(board,r,c)

            if len(cand) == 0:
                return None,None


            if best is None or len(cand) < len(best_candidate):

                best = (r,c)
                best_candidate = cand


    return best,best_candidate



# ------------------------------------------------------------
# 解く（制約伝播 + MRV + バックトラッキング）
# ------------------------------------------------------------

def solve(board):

    stats.nodes += 1


    # 制約伝播
    if not constraint_propagation(board):
        return False


    # 完成判定
    if all(board[r][c] != 0 for r in range(9) for c in range(9)):
        return True



    pos,cand = find_best_cell(board)


    if pos is None:
        return False


    r,c = pos


    # 候補を試す
    for x in cand:

        new_board = deepcopy(board)

        new_board[r][c] = x


        if solve(new_board):

            for i in range(9):
                board[i] = new_board[i]

            return True


        # 失敗して戻る
        stats.backtracks += 1



    return False



# ------------------------------------------------------------
# 実行
# ------------------------------------------------------------

tracemalloc.start()

start = perf_counter()

ok = solve(board)

elapsed = perf_counter() - start


current, peak = tracemalloc.get_traced_memory()

tracemalloc.stop()



print("=== 実行結果 ===")
print("解が見つかったか :", ok)
print(f"実行時間           : {elapsed:.6f} 秒")
print(f"探索ノード数       : {stats.nodes}")
print(f"バックトラック回数 : {stats.backtracks}")
print(f"最大メモリ使用量   : {peak / 1024:.2f} KB")