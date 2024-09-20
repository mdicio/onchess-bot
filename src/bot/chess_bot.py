from bot.web_interface import WebInterface
from bot.chess_engine import ChessEngine
import time


class ChessBot:
    def __init__(
        self,
        web_interface: WebInterface,
        chess_engine: ChessEngine,
    ):
        self.web_interface = web_interface
        self.chess_engine = chess_engine
        self.previous_move_count = 0

    def detect_end_of_game(self):
        """
        Detects if the game has ended due to checkmate, stalemate, or time over.

        Returns:
        - True if the game has ended, otherwise False.
        - A string indicating the reason for the game end ('checkmate', 'stalemate', 'timeover', or None if not ended).
        """

        # 1. Check for checkmate using the chess engine
        if self.chess_engine.is_checkmate():
            print("Checkmate detected!")
            return True, "checkmate"

        # 2. Check for stalemate using the chess engine
        if self.chess_engine.board.is_stalemate():
            print("Stalemate detected!")
            return True, "stalemate"

        # 3. Check for time over from the web interface (assuming timeover detection logic)
        if self.web_interface.detect_is_time_over():
            print("Timeover detected!")
            return True, "timeover"

        # If none of the above conditions are met, the game is still ongoing
        return False, None

    def play_game(self, playing_as="white", mode="auto", timeout=10, loop_speed=0.1):
        """
        Play a game against the computer by interacting with the web-based chessboard.
        """
        previous_move = "asd"  # previous move not exist at start, just needs to be set to something random
        game_move_count = 0  # Track the number of moves in the move history
        self.playing_as = playing_as
        if not self.web_interface.browser_is_running:
            self.web_interface.start_browser()
        if not mode == "debug":
            self.web_interface.navigate_to_lichess()
            self.web_interface.navigate_to_computer_play()
            self.web_interface.select_computer_level()
            self.web_interface.select_color()

        self.chess_engine.setup_board()
        self.chess_engine.setup_engine()

        # Handle initial computer move when playing as Black
        if self.playing_as == "black":
            computer_move = self.web_interface.wait_for_computer_move(
                previous_move,
                game_move_count,
                timeout=timeout,
                playing_as=playing_as,
                loop_speed=loop_speed,
            )
            print("Detected computer's initial move:", computer_move)
            self.chess_engine.update_board_with_move(
                computer_move
            )  # Push the move to the board
            self.chess_engine.set_fen_position()  # Update engine's FEN position
            print(
                "Evaluation after computer's move:", self.chess_engine.get_evaluation()
            )

        # Main game loop
        while not self.chess_engine.is_game_over():
            # Get the best move from the engine
            self.chess_engine.set_fen_position()  # Update engine with the current position
            best_move = self.chess_engine.get_best_move()
            print(f"Best move: {best_move}")

            # Translate the best move to web-based interaction (start and end squares)
            start_square, end_square = self.chess_engine.translate_move_to_web(
                best_move
            )
            print(f"Performing move: {start_square} to {end_square}")

            # Perform the move on the web interface
            self.web_interface.drag_and_drop_by_square(start_square, end_square)
            if self.chess_engine.is_promotion(best_move):
                self.web_interface.handle_pawn_promotion(best_move)

            # Push the move to the chess engine and update board
            self.chess_engine.update_board_with_move(best_move)
            game_move_count += 1

            if self.chess_engine.is_checkmate():
                print("Checkmate! My bot reigns over the chess galaxies!")
                break

            computer_move = self.web_interface.wait_for_computer_move(
                previous_move,
                game_move_count,
                loop_speed=loop_speed,
                playing_as=self.playing_as,
                timeout=timeout,
            )
            print(f"Detected computer's move: {computer_move}")

            # Push the move to the engine and update the board
            self.chess_engine.update_board_with_move(computer_move)
            if self.chess_engine.is_checkmate():
                print("Checkmate! My bot got bamboozled!")
                break

            # Update move count
            game_move_count += 1
            print(
                "Evaluation after computer's move:", self.chess_engine.get_evaluation()
            )

            # Check if game over
            game_over, reason = self.detect_end_of_game()
            if game_over:
                print("Game Over", reason)
                break

        # Send quit command to the engine
        self.chess_engine.send_quit_command()
