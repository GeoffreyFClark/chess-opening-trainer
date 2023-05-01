import os
import pygame
import pygame.gfxdraw
import chess
import chess.svg
import chess.engine

# # Initialize a chess engine
# engine = chess.engine.SimpleEngine.popen_uci('stockfish')

# engine.quit()

# # Get the best move from the engine
# result = engine.play(board, chess.engine.Limit(time=2.0))
# best_move = result.move

pygame.init()

# Set up the window
width, height = 812, 512
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("GFC's Chess Opening Trainer")

# Load board 
chess_board_img_path = os.path.join('chess_image_assets', 'board.png')
board_img = pygame.image.load(chess_board_img_path)

# Load pieces
piece_imgs = {}
for color in ['w', 'b']:
    for piece in ['p', 'n', 'b', 'r', 'q', 'k']:
        key = f'{color}{piece}'
        chess_piece_img_path = os.path.join('chess_image_assets', f'{key}.png')
        piece_imgs[key] = pygame.image.load(chess_piece_img_path)
        


# Draw the initial board state
board = chess.Board()
board_surface = pygame.Surface((width, height))
board_surface.blit(board_img, (0, 0))
# for square in chess.SQUARES:
#     if board.piece_at(square) is not None:
#         piece_key = board.piece_at(square).symbol().lower()
#         if board.piece_at(square).color == chess.BLACK:
#             piece_key = 'b' + piece_key
#         elif board.piece_at(square).color == chess.WHITE:
#             piece_key = 'w' + piece_key
#         piece_img = piece_imgs[piece_key]
#         x, y = chess.square_file(square) * 64, (7 - chess.square_rank(square)) * 64
#         board_surface.blit(piece_img, (x, y))
# window.blit(board_surface, (0, 0))
# pygame.display.update()

def redraw_board_surface():
    # Clear the board surface
    board_surface.fill((0, 0, 0, 0))
    # Draw the chessboard image
    board_surface.blit(board_img, (0, 0))
    # Draw the pieces based on the current state of the chess.Board object
    for square in chess.SQUARES:
        if board.piece_at(square) is not None:
            piece_key = board.piece_at(square).symbol().lower()
            if board.piece_at(square).color == chess.BLACK:
                piece_key = 'b' + piece_key
            elif board.piece_at(square).color == chess.WHITE:
                piece_key = 'w' + piece_key
            piece_img = piece_imgs[piece_key]
            x, y = chess.square_file(square) * 64, (7 - chess.square_rank(square)) * 64
            board_surface.blit(piece_img, (x, y))

redraw_board_surface()
window.blit(board_surface, (0, 0))
pygame.display.update()

selected_piece = None
selected_piece_pos = None
start_square = None

running = True
while running:
    pygame.event.poll()
    # Main event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position and calculate the selected square
            mouse_x, mouse_y = event.pos
            file, rank = mouse_x // 64, 7 - mouse_y // 64
            start_square = chess.square(file, rank)
            # Check if there is a piece on the selected square
            piece = board.piece_at(start_square)
            if piece is not None:
                selected_piece = piece.symbol().lower()
                selected_piece_pos = (mouse_x, mouse_y)
                # Remove the piece from the board temporarily
                board.remove_piece_at(start_square)
        elif event.type == pygame.MOUSEMOTION:
            # Update the position of the selected piece
            if selected_piece is not None:
                selected_piece_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            # Drop the piece and update the chess board
            if selected_piece is not None and start_square is not None:
                mouse_x, mouse_y = event.pos
                file, rank = mouse_x // 64, 7 - mouse_y // 64
                end_square = chess.square(file, rank)
                move = chess.Move(start_square, end_square)
                # Check if the move is legal
                if move in board.legal_moves:
                    # Apply the move to the board
                    board.push(move)
                else:
                    # If the move is illegal, return the piece to its original position
                    board.set_piece_at(start_square, chess.Piece.from_symbol(selected_piece))
                selected_piece = None
                selected_piece_pos = None
                start_square = None
                redraw_board_surface()

    # Redraw the board and pieces
    window.blit(board_surface, (0, 0))
    for square in chess.SQUARES:
        if board.piece_at(square) is not None:
            piece_key = board.piece_at(square).symbol().lower()
            if board.piece_at(square).color == chess.BLACK:
                piece_key = 'b' + piece_key
            elif board.piece_at(square).color == chess.WHITE:
                piece_key = 'w' + piece_key
            piece_img = piece_imgs[piece_key]
            x, y = chess.square_file(square) * 64, (7 - chess.square_rank(square)) * 64
            window.blit(piece_img, (x, y))
    # Draw the selected piece at the current position
    if selected_piece is not None:
        piece_key = selected_piece
        piece_img = piece_imgs[piece_key]
        window.blit(piece_img, (selected_piece_pos[0] - 32, selected_piece_pos[1] - 32))
    pygame.display.update()

pygame.quit()
