import os, random

class Piece:
    top = 0
    bottom = 0
    left = 0
    right = 0
    orientation = 0
    id = 0

    def __init__(self, top, bottom, left, right, id = 0, orientation = 0):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.id = id
        self.orientation = orientation

    def move_orientation(self):
        top = self.top
        self.top = self.left
        self.left = self.bottom
        self.bottom = self.right
        self.right = top
        self.orientation += 1
        if self.orientation == 4:
            self.orientation = 0


class Board:
    board = []
    resultPath = './result/'
    nextFile = 1
    pieces = {}
    border_pieces = {}
    best_result_x = 0
    best_result_y = 0

    def __init__(self):
        self.load_pieces()

        for i in range(16):
            self.board.append(['x' for _ in range(16)])
        self.board[8][7] = self.pieces[139]
        del self.pieces[139]

        if not os.path.exists(self.resultPath):
            os.mkdir(self.resultPath)

        dirs = os.listdir(self.resultPath)
        if len(dirs) == 0:
            self.resultPath += '1'
        else:
            index = 1
            for dir_name in dirs:
                if int(dir_name) > index:
                    index = int(dir_name)
            self.resultPath += str(index + 1)
        os.mkdir(self.resultPath)

    def load_pieces(self):
        with open('./assets/pieces.txt', 'r') as file:
            line = file.readline()
            counter = 1
            while line:
                pieces = line.split(' ')
                if pieces[0] == 'x' or pieces[1] == 'x' or pieces[2] == 'x' or pieces[3][:-1] == 'x':
                    self.border_pieces[counter] = Piece(int(pieces[0]), int(pieces[1]), int(pieces[2]), int(pieces[3][:-1]), counter)
                else:
                    self.pieces[counter] = Piece(int(pieces[0]), int(pieces[1]), int(pieces[2]), int(pieces[3][:-1]), counter)
                line = file.readline()
                counter += 1

    def export(self):
        counter = 0
        with open(self.resultPath + '/' + str(self.nextFile) + '.txt', 'w') as file:
            for line in self.board:
                result = ''
                for row in line:
                    if row == 'x':
                        result += 'X-'
                    else:
                        result += str(row.id - 1) + '(' + str(row.orientation) + ')' + '-'
                if counter < 15:
                    file.write(result[:-1] + '\n')
                else:
                    file.write(result[:-1])
                counter += 1
        self.nextFile += 1

    def fill_randomly(self):
        orientation = [0, 1, 2, 3]
        for line in range(16):
            for row in range(16):
                if self.board[line][row] == 'x':
                    piece_id = random.choice(list(self.pieces))
                    piece = self.pieces.pop(piece_id)
                    for i in range(random.choice(orientation)):
                        piece.move_orientation()
                    self.board[line][row] = piece

    def get_needed_side(self, x, y):
        if y == 0:
            top = 0
        else:
            piece = self.board[y - 1][x]
            if piece == 'x':
                top = 'x'
            else:
                top = piece.bottom

        try :
            piece = self.board[y + 1][x]
            if piece == 'x':
                bottom = 'x'
            else:
                bottom = piece.top
        except IndexError:
            bottom = 0

        if x == 0:
            left = 0
        else:
            piece = self.board[y][x - 1]
            if piece == 'x':
                left = 'x'
            else:
                left = piece.right

        try:
            piece = self.board[y][x + 1]
            if piece == 'x':
                right = 'x'
            else:
                right = piece.left
        except IndexError:
            right = 0

        return {
            'top': top,
            'bottom': bottom,
            'left': left,
            'right': right,
        }

    def is_best_result_tmp(self, x, y):
        if y > self.best_result_y:
            return True
        if y == self.best_result_y and x > self.best_result_x:
            return True
        return False

    def is_best_result(self, x, y):
        if y < self.best_result_y:
            return False
        if x < self.best_result_x:
            return False
        return True


    def try_win_two_million(self, x, y):
        next_x = x + 1
        next_y = y
        if next_x == 16:
            next_x = 0
            next_y = y + 1
            if next_y == 16:
                print("You win 2 million")
                self.export()
                exit()
        if not self.board[y][x] == 'x':
            self.try_win_two_million(next_x, next_y)
            return
        needed = self.get_needed_side(x, y)
        if needed == 0 or needed == 0 or needed == 0 or needed == 0:
            border = True
            pieces = self.border_pieces
        else:
            border = False
            pieces = self.pieces
        for piece_id in pieces:
            for _ in range(4):
                piece = pieces[piece_id]
                if piece.top == needed['top'] or (needed['top'] == 'x' and not piece.top == 0):
                    if piece.bottom == needed['bottom'] or (needed['bottom'] == 'x' and not piece.bottom == 0):
                        if piece.left == needed['left'] or (needed['left'] == 'x' and not piece.left == 0):
                            if piece.right == needed['right'] or (needed['right'] == 'x' and not piece.right == 0):
                                self.board[y][x] = piece
                                if border:
                                    del self.border_pieces[piece_id]
                                else:
                                    del self.pieces[piece.id]
                                if self.is_best_result(x, y):
                                    self.export()
                                    self.best_result_x = x
                                    self.best_result_y = y
                                self.try_win_two_million(next_x, next_y)
                                if border:
                                    self.border_pieces[piece.id] = piece
                                else:
                                    self.pieces[piece.id] = piece

                                self.board[y][x] = 'x'
                piece.move_orientation()







a = Board()
a.try_win_two_million(0, 0)
# print(a.get_needed_side(0, 0))
# a.fillRandomly()
# a.export()
