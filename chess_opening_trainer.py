import os  # Filepaths will be platform-independent (I like both macOS + Windows)
import pygame
import pygame.gfxdraw
import chess
import chess.svg
import chess.engine

pygame.init()

# Set up the window
width = height = 512
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("GFC's Chess Opening Trainer")

# Load board and piece images
chess_board_img_path = os.path.join('chess_image_assets', 'board.png')
board_img = pygame.image.load(chess_board_img_path)

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
window.blit(board_surface, (0, 0))
pygame.display.update()


running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

# # Initialize a chess engine
# engine = chess.engine.SimpleEngine.popen_uci('stockfish')

# engine.quit()

# # Get the best move from the engine
# result = engine.play(board, chess.engine.Limit(time=2.0))
# best_move = result.move