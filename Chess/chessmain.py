'''Current game state and user input'''
import pygame as p
from Chess import chesseng

WIDTH = HEIGHT = 512
DIMENSION = 8  # dimension pf chess
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 12  # for animations later on
IMAGES = {}
'''
Initialize a global dictionary of images 
'''


def load_Images():
    pieces = {'wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ'}
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chesseng.Gamestate()
    load_Images()
    running = True
    sq_selected = ()
    playerClicks = []  # keep track of player clicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sq_selected == (row, col):
                    sq_selected = ()
                    playerClicks = []  # if already selected, then clear
                else:
                    sq_selected = (row, col)
                    playerClicks.append(sq_selected)  # append for first and second clicks

                if len(playerClicks) == 2:
                    Move = chesseng.move(playerClicks[0], playerClicks[1], gs.board, gs.whiteToMove, gs)
                    # if(gs.is_checkmate()):
                    #     print("Game over!Checkmate")
                    #     running=False
                    # checkmate = chesseng.checkmate(gs, Move)
                    # if checkmate.is_checkmate(gs.board):
                    #     print("Checkmate! Game Over.")
                    #     running = False
                    # print(Move.is_in_check(gs.board))
                    print(gs.moveLog)
                    # print(gs.is_checkmate())

                    if Move.isValid(gs.board):

                        gs.moveLog.append(Move)


                        # print(Move.checkmate(gs.board))

                        # gs.generate_possible_moves()


                        gs.makeMove(Move)
                        if(gs.is_checkmate()):
                            print("Its Checkmate!")
                            running=False
                        if(gs.is_stalemate()):
                            print("Its Stalemate!")
                            running=False

                        # if(gs.is_checkmate()):
                        #     print("Checkmate")
                        #     running=False
                        # elif(gs.is_stalemate()):
                        #     print("Stalemate")
                        #     running=False
                        # else:
                        #     pass






                        # print(gs.is_checkmate())
                        # print(gs.moveLog)


                        # print(checkmate.is_checkmate(gs.board))

                    else:
                        sq_selected = ()
                        playerClicks = []

                    sq_selected = ()
                    playerClicks = []

        drawGameState(screen, gs)

        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("brown")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c];
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# def isValid(StartSq,EndSq,piece):
#     if piece=="wp":
#         if()


if __name__ == "__main__":
    main()
