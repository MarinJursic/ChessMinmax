from ChessEngine import GameState
from math import inf
from copy import deepcopy
from numpy import flipud

global currentBoard

START_DEPTH = 3

PAWN = 100
BISHOP = 300
KNIGHT = 300
ROOK = 500
QUEEN = 900

white = {
    "wp": PAWN,
    "wB": BISHOP,
    "wN": KNIGHT,
    "wR": ROOK,
    "wQ": QUEEN,
}

black = {
    "bp": PAWN,
    "bB": BISHOP,
    "bN": KNIGHT,
    "bR": ROOK,
    "bQ": QUEEN,
}

PieceSquare = {
    "wp": [[0, 0, 0, 0, 0, 0, 0, 0],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [0, 0, 0, 0, 0, 0, 0, 0]],
    "wN": [[-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]],
    "wB": [[-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]],
    "wR": [[0,  0,  0,  0,  0,  0,  0,  0],
              [5, 10, 10, 10, 10, 10, 10,  5],
             [-5,  0,  0,  0,  0,  0,  0, -5],
             [-5,  0,  0,  0,  0,  0,  0, -5],
             [-5,  0,  0,  0,  0,  0,  0, -5],
             [-5,  0,  0,  0,  0,  0,  0, -5],
             [-5,  0,  0,  0,  0,  0,  0, -5],
             [0,  0,  0,  5,  5,  0,  0,  0]],
    "wQ": [[-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
             [-5,  0,  5,  5,  5,  5,  0, -5],
              [0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]],
    "wK": [[-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
             [20, 20,  0,  0,  0,  0, 20, 20],
             [20, 30, 10,  0,  0, 10, 30, 20]],
    "bp": [[0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
             [5,  5, 10, 25, 25, 10,  5,  5],
             [0,  0,  0, 20, 20,  0,  0,  0],
             [5, -5,-10,  0,  0,-10, -5,  5],
             [5, 10, 10,-20,-20, 10, 10,  5],
             [0,  0,  0,  0,  0,  0,  0,  0]],
    "bN": [[50,40,30,30,30,30,40,50],
            [40,20,  0,  0,  0,  0,20,40],
            [30,  0, -10, -15, -15, -10,  0,30],
            [30,  -5, -15, -20, -20, -15,  -5,30],
            [30,  0, -15, -20, -20, -15,  0,30],
            [30,  -5, -10, -15, -15, -10,  -5,30],
            [40,20,  0,  -5,  -5,  0,20,40],
            [50,40,30,30,30,30,40,50]],
    "bB": [[-20, -10, -10, -10, -10, -10, -10, -20],
            [-10, 5, 0, 0, 0, 0, 5, -10],
            [-10, 10, 10, 10, 10, 10, 10, -10],
            [-10, 0, 10, 10, 10, 10, 0, -10],
            [-10, 5, 5, 10, 10, 5, 5, -10],
            [-10, 0, 5, 10, 10, 5, 0, -10],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]],
    "bR": [[0, 0, 0, 5, 5, 0, 0, 0],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [5, 10, 10, 10, 10, 10, 10, 5],
            [0, 0, 0, 0, 0, 0, 0, 0]],
    "bQ": [[-20, -10, -10, -5, -5, -10, -10, -20],
            [-10, 0, 5, 0, 0, 0, 0, -10],
            [-10, 5, 5, 5, 5, 5, 0, -10],
            [0, 0, 5, 5, 5, 5, 0, -5],
            [-5, 0, 5, 5, 5, 5, 0, -5],
            [-10, 0, 5, 5, 5, 5, 0, -10],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-20, -10, -10, -5, -5, -10, -10, -20]],
    "bK": [[20, 30, 10, 0, 0, 10, 30, 20],
            [20, 20, 0, 0, 0, 0, 20, 20],
            [-10, -20, -20, -20, -20, -20, -20, -10],
            [-20, -30, -30, -40, -40, -30, -30, -20],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30]]
}

def minimax(gs, depth, AI,alpha,beta,First):

    global currentBoard

    if First:
        currentBoard = deepcopy(gs.getBoard())

    if AI:
        gs.whiteToMove = False
    else:
        gs.whiteToMove = True

    validMoves = gs.getValidMoves()

    if First:
        for move in validMoves:
            print(move.startRow, move.startCol, move.endRow, move.endCol, move.pieceMoved)
        First = False

    chessBoard = gs.getBoard()

    if AI:
        bestMove = [deepcopy(chessBoard), -inf]
    else:
        bestMove = [deepcopy(chessBoard), inf]

    if depth == 0 or len(validMoves) == 0:

        if gs.checkMate:
            if gs.whiteToMove:

                gs.checkMate = False
                print("Black checkmate")
                return chessBoard, inf
            else:
                gs.checkMate = False
                print("White checkmate")
                return chessBoard, -inf
        elif gs.staleMate:

            gs.staleMate = False
            print("stalemate")
            return chessBoard, 0

        else:
            score = deepcopy(evaluate(chessBoard)[0] - evaluate(chessBoard)[1])
            return chessBoard, score

    for move in validMoves:

        gs.makeMove(move)

        score = minimax(gs, depth - 1, 1 if AI == 0 else 0,alpha,beta,False)

        if depth == START_DEPTH:
            score = deepcopy(score)

        gs.undoMove()

        if AI:
            if score[1] > bestMove[1]:
                if score[0] != currentBoard:
                    bestMove = score

            if bestMove[1] >= beta:
                return bestMove

            if bestMove[1] > alpha:
                alpha = bestMove[1]

        else:
            if score[1] < bestMove[1]:
                if score[0] != currentBoard:
                    bestMove = score

            if bestMove[1] <= alpha:
                return bestMove

            if bestMove[1] < beta:
                beta = bestMove[1]

    return bestMove


def evaluate(board):
    blackScore = 0
    whiteScore = 0

    for row in range(8):
        for col in range(8):
            if board[row][col][0] == "w" and board[row][col] != "wK":
                whiteScore += white[board[row][col]]
                whiteScore += PieceSquare[board[row][col]][row][col]
            elif board[row][col][0] == "b" and board[row][col] != "bK":
                blackScore += black[board[row][col]]
                blackScore += PieceSquare[board[row][col]][row][col]

    return blackScore, whiteScore