"""
Main Chess driver file
Responsible for handling user input and displaying current GameState
"""
import pygame as p
import ChessEngine
from Minimax import minimax
from math import inf

START_DEPTH = 3

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}

# Loading images

def LoadImages():

    pieces = ['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess_Files/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

# The Main Driver

def main():

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    gameOver = False
    LoadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    currentBoard = gs.getBoard()
    count = 0

    while running == True:

        if not gs.whiteToMove and not gameOver:

            Result = minimax(gs, START_DEPTH, 1,-inf,inf,True)
            start, end = findMove(currentBoard, Result[0])
            Move = ChessEngine.Move(start, end, gs.board)
            gs.makeMove(Move)
            moveMade = True
            animate = True
            currentBoard = gs.getBoard()
            gs.whiteToMove = True


        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row,col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                                currentBoard = gs.getBoard()
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen,gs,validMoves,sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen,'Black wins by checkmate')
            else:
                drawText(screen,'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen,'Stalemate')

        count += 1
        clock.tick(MAX_FPS)
        p.display.flip()

# Highlight square selected and moves for piece selected

def highlightSquares(screen,gs,validMoves,sqSelected):

    if sqSelected != ():
        r,c = sqSelected

        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):

            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE, r*SQ_SIZE))

            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol,SQ_SIZE*move.endRow))



# Responsible for graphics within a current game state.

def drawGameState(screen,gs,validMoves,sqSelected):
    drawBoard(screen)
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board)

# Draw squares on board
def drawBoard(screen):
    global colors
    colors = [p.Color("#eeeed2"), p.Color("#769656")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen,color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draw pieces on board

def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animateMove(move,screen,board,clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 3
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount+1):
        r,c = ((move.startRow + dR*frame/frameCount,move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen,board)
        color = colors[(move.endRow+move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured],endSquare)
        screen.blit(IMAGES[move.pieceMoved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen,text):
    font = p.font.SysFont('Helvitca',32,True,False)
    textObject = font.render(text,0,p.Color('Black'))
    textLocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2,HEIGHT/2-textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject = font.render(text,0,p.Color('Gray'))
    screen.blit(textObject,textLocation.move(2,2))

def findMove(currentBoard,board):

    piece = ""
    start = []
    end = []
    state = 0

    for row in range(8):
        for col in range(8):
            if currentBoard[row][col] != board[row][col]:
                if currentBoard[row][col] == "--":
                    piece = board[row][col]
                    end = [row,col]
                    state = 2
                elif currentBoard[row][col] != "--":
                    if board[row][col] != "--":
                        piece = board[row][col]
                        end = [row,col]
                        state = 2
                    elif board[row][col] == "--":
                        piece = currentBoard[row][col]
                        start = [row,col]
                        state = 1


    if state == 1:

        for row in range(8):
            for col in range(8):
                if board[row][col] == piece and board[row][col] != currentBoard[row][col]:
                    end = [row,col]
                    return start,end
    elif state == 2:

        if end[0] == 7 and piece == "bQ":
            start = [6,end[1]]
            return start,end

        for row in range(8):
            for col in range(8):
                if currentBoard[row][col] == piece and board[row][col] != currentBoard[row][col]:
                    start = [row,col]
                    return start,end


if __name__ == "__main__":
    main()



