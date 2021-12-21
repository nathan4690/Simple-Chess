import chess
import pygame
from os.path import dirname
from typing import Iterable

pygame.init()
infoObject = pygame.display.Info()
RESOURCESPATH = (dirname(__file__)) + "/Resources/"
SCREENWIDTH = 60*8
SCREENHEIGHT = 60*8
IMAGESNAME = ["wK","wQ","wR","wB","wN","wP","bk","bq","br","bb","bn","bp"]
images = []
for i in IMAGESNAME:
        images.append(pygame.image.load(RESOURCESPATH +i+".png"))
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
defaultFont = pygame.font.SysFont("Calibri",int(100/1500*SCREENWIDTH))
chessboard = chess.Board()
pygame.display.set_caption("Chess")

class Cover:
    def __init__(self,master,color,top=0,left=0,width=SCREENWIDTH,height=SCREENHEIGHT) -> None:
        self.master = master
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.left,self.top,self.width,self.height)

    def draw(self,):
        shape_surf = pygame.Surface(pygame.Rect(self.rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, self.color, shape_surf.get_rect())
        self.master.blit(shape_surf, self.rect)

class PygameText():
    def __init__(self,master,font=defaultFont) -> None:
        self.master = master
        self.font = font

    def draw(self,text: str,pos=None,color=(255,0,0)):
        cnt = len(text.splitlines())
        for line in text.splitlines():
            img = self.font.render(line,True,color)
            pos = [SCREENWIDTH/2-img.get_width()/2,SCREENHEIGHT/2 - (img.get_height()/2)]
            pos = list(pos)
            if cnt >= 1:
                pos[1] -= ((img.get_height())+20/2)*(cnt-1)
            self.master.blit(img,pos)
            print(cnt,pos)
            cnt -= 1

def flipy(r,c):
    # c = (8 - c)
    r = 8-r-1
    return chess.square(c,r)

def drawBoard(selected: Iterable[int] = None , mrange: Iterable[Iterable[int]] = None):
    colors = [pygame.Color("white"),pygame.Color("grey")]
    for r in range(8):
        for c in range(8):
            pygame.draw.rect(screen,colors[(r+c)%2],pygame.Rect(c*60,r*60,60,60))
    if selected:
        r,c = selected
        pygame.draw.rect(screen, pygame.Color(110, 155, 255), pygame.Rect(c*60,r*60,60,60))
    if mrange:
        for r,c in mrange:
            pygame.draw.rect(screen, pygame.Color(255, 214, 110), pygame.Rect(c*60,r*60,60,60))

def drawPieces(board: chess.Board):
    mboard = board.transform(chess.flip_vertical)
    # print(mboard.piece_map().items())
    for sq, piece in list(mboard.piece_map().items()):
        ssym = chess.square_name(sq)
        r,c = [chess.FILE_NAMES.index(ssym[0]),int(ssym[1])-1]
        psym = piece.symbol()
        psym = ("w" if psym.isupper() else "b") + psym
        # print(psym,r,c)
        screen.blit(images[IMAGESNAME.index(psym)],(r*60,c*60))
    # print(type(sq), type(piece))

# print(chess.square_name(flipy(1,2)))
done = False
click = True
selected = []
availmoves = []
mrange = []
txt = PygameText(screen)
cvr = Cover(screen,(0,0,0,200))
while not done:
    # print(chessboard)
    drawBoard(selected,mrange)
    drawPieces(chessboard)
    if chessboard.is_game_over():
        cvr.draw()
        res = chessboard.outcome().result()
        reas = chessboard.outcome().termination.name
        if res == "1-0":
            txt.draw(f"White wins-{reas}")
        elif res == "0-1":
            txt.draw(f"Black wins-{reas}")
        else:
            txt.draw(f"Draw-{reas}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and not chessboard.is_game_over():
            aselected = (pygame.mouse.get_pos()[1] // 60,pygame.mouse.get_pos()[0] // 60,)
            if click:
                availmoves = []
                mrange = []
                squ = flipy(*aselected)
                print(chess.square_name(squ))
                piec = chessboard.piece_at(squ)
                print(piec)
                selected = aselected[:]
                for move in chessboard.generate_legal_moves():
                    # print(move.from_square, squ)
                    if move.from_square == squ:
                        ssym = chess.square_name(move.to_square)
                        r,c = [chess.FILE_NAMES.index(ssym[0]),8-int(ssym[1])]
                        mrange.append((c,r))
                        availmoves.append(move)
                click = not click
            else:
                print(aselected,mrange)
                if tuple(aselected) in mrange:
                    chessboard.push(availmoves[mrange.index(aselected)])
                print(chessboard.is_game_over())
                click = not click
                selected = []
                availmoves = []
                mrange = []

    pygame.display.flip()