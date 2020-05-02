MOVEMENTS = [[1,2],[-1,2],[1,-2],[-1,-2],[2,1],[-2,1],[2,-1],[-2,-1]]

def countMoves(board):
    sum = 0
    for i in board:
        for j in i:
            if j is None:
                j=0
            sum = sum + j
    return sum

def shortest_path(sx, sy, dx, dy, board):
    moves = [(sx, sy)]
    while moves:
        curr_x, curr_y = moves.pop(0)
        for i in MOVEMENTS:
          new_x, new_y = curr_x + i[0], curr_y + i[1]
          if ((sx-2 <= new_x <= sx+2 or sy-2 <= new_y <= sy+2) or (dx-2 <= new_x <= dx+2 or dy-2 <= new_y <= dy+2)) and (0 <= new_x <= 7 and 0 <= new_y <= 7):
              if board[new_x][new_y] is None:
                  board[new_x][new_y] = board[curr_x][curr_y] + 1
                  moves.append((new_x, new_y)) 
                #   print()
                #   print(moves)
                #   print(board)
                #   print()

def solution(src, dest):
    board = [[None for i in range(8)] for i in range(8)]
    start_x, start_y = int(src/8), src%8
    dest_x, dest_y = int(dest/8), dest%8
    board[start_x][start_y] = 0
    shortest_path(start_x, start_y, dest_x, dest_y, board)
    # print('total steps - ',countMoves(board))
    return board[dest_x][dest_y]

print(solution(0, 17))