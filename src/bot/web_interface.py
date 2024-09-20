from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import undetected_chromedriver as uc
import time
import re


class WebInterface:
    def __init__(self, timeout=10, driver_path="/usr/bin/google-chrome-beta"):
        self.timeout = timeout
        self.driver_path = driver_path
        self.browser_is_running = False

    def start_browser(self):
        uddir = "/Users/mdicio/Library/Application Support/Google/Chrome"
        profile = "Profile 1"

        if os.path.exists(f"{uddir}/{profile}"):
            print(1)

        u_options = uc.ChromeOptions()
        u_options.add_argument(f"user-data-dir={uddir}")
        u_options.add_argument(f"--profile-directory={profile}")

        self.browser = uc.Chrome(
            browser_executable_path=self.driver_path,
            options=u_options,
            use_subprocess=True,
        )
        self.browser_is_running = True
        time.sleep(1)

    def navigate_to_lichess(self, home_url="https://lichess.org/"):
        self.browser.get(home_url)
        time.sleep(1)

    def navigate_to_computer_play(self):
        # Code for navigating to the computer play page
        try:
            # Click the "Play with the computer" button by its visible text
            computer_button_xpath = (
                "//button[contains(text(), 'Play with the computer')]"
            )
            WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, computer_button_xpath))
            )
            computer_button = self.browser.find_element(By.XPATH, computer_button_xpath)
            ActionChains(self.browser).move_to_element(
                computer_button
            ).click().perform()

            print("Navigating to the 'Play with the computer' page.")
        except TimeoutException:
            print("Navigating to 'Play with the computer' page: took too much time!")
        except Exception as e:
            print(f"Error navigating to 'Play with the computer': {e}")

    def select_computer_level(self, level=1):
        try:
            # XPath for the desired level based on its value (e.g., level 1, 2, 3)
            level_xpath = f"//input[@id='sf_level_{level}']"

            # Wait until the level radio button is present
            WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, level_xpath))
            )

            # Use JavaScript to click on the element
            level_radio = self.browser.find_element(By.XPATH, level_xpath)
            self.browser.execute_script(
                "arguments[0].scrollIntoView(true);", level_radio
            )  # Scroll into view
            self.browser.execute_script(
                "arguments[0].click();", level_radio
            )  # Perform the click using JS

            print(f"Computer level {level} selected.")
        except TimeoutException:
            print(f"Selecting computer level {level} took too much time!")
        except Exception as e:
            print(f"Error selecting computer level {level}: {e}")

    def select_color(self, color="random"):
        try:
            # Map color choices to their respective class names
            color_classes = {
                "random": "color-submits__button random",  # assuming random class
                "white": "color-submits__button white",
                "black": "color-submits__button black",
            }

            if color not in color_classes:
                raise ValueError(
                    "Invalid color choice. Choose 'random', 'white', or 'black'."
                )

            # Get the class for the desired color
            color_class = color_classes[color]

            # XPath to locate the button with the specific class
            color_button_xpath = f"//button[contains(@class, '{color_class}')]"

            # Wait until the color button is present
            WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, color_button_xpath))
            )

            # Click the color button
            color_button = self.browser.find_element(By.XPATH, color_button_xpath)
            ActionChains(self.browser).move_to_element(color_button).click().perform()

            print(f"Color '{color}' selected.")
        except TimeoutException:
            print(f"Selecting color '{color}' took too much time!")
        except Exception as e:
            print(f"Error selecting color '{color}': {e}")

    def generate_square_pixel_mapping(self, playing_as="white"):
        """
        Generates a mapping of chess squares (e.g., 'a1', 'h8') to pixel coordinates
        (top-left and bottom-right corners) based on the board size.
        """
        try:
            # Wait until the chessboard element is present and visible
            chessboard = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "cg-board"))
            )

            # Get the size of the chessboard (bounding box)
            board_size = chessboard.size
            board_width = board_size["width"]
            board_height = board_size["height"]

            square_width = board_width / 8
            square_height = board_height / 8

            # Files and ranks in chess
            files = "abcdefgh"
            ranks = "12345678"  # Rank 1 at the bottom (for white at the bottom)

            if playing_as == "black":
                files = files[::-1]
                ranks = ranks[::-1]

            # Dictionary to store the pixel coordinates for each square
            square_pixel_mapping = {}

            # Generate the pixel coordinates for each square
            for rank_index, rank in enumerate(ranks):
                for file_index, file in enumerate(files):
                    # Calculate the pixel coordinates for the top-left corner of the square
                    top_left_x = file_index * square_width
                    top_left_y = (
                        7 - rank_index
                    ) * square_height  # Flip y-coordinate for ranks

                    # Calculate the pixel coordinates for the bottom-right corner of the square
                    bottom_right_x = top_left_x + square_width
                    bottom_right_y = top_left_y + square_height

                    # Store the pixel coordinates for this square
                    square_pixel_mapping[f"{file}{rank}"] = {
                        "top_left": (top_left_x, top_left_y),
                        "bottom_right": (bottom_right_x, bottom_right_y),
                    }

            return square_pixel_mapping

        except TimeoutException:
            print(f"Chessboard element not found within {self.timeout} seconds.")
            return None

    def find_square_for_pixel(self, x, y, square_pixel_mapping):
        """
        Finds the corresponding chess square for pixel coordinates (x, y).
        """
        for square, boundaries in square_pixel_mapping.items():
            top_left = boundaries["top_left"]
            bottom_right = boundaries["bottom_right"]

            # Extract pixel coordinates for the top-left and bottom-right corners
            top_left_x, top_left_y = top_left
            bottom_right_x, bottom_right_y = bottom_right

            # Check if the x, y coordinates fall within this square's pixel range
            if top_left_x <= x < bottom_right_x and top_left_y <= y < bottom_right_y:
                return square

        return None  # If no square found (this shouldn't happen on a valid board)

    def extract_piece_positions(self):
        """
        Extracts the piece positions from the chessboard (<cg-board>) by reading the
        transform: translate(x, y) values and the piece class.

        Parameters:
        - timeout: Maximum time to wait for the piece elements to be present.

        Returns:
        - piece_positions: A list of dictionaries with piece class and its (x, y) coordinates.
        """
        piece_positions = []

        try:
            # Wait for the piece elements on the chessboard
            pieces = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "cg-board piece"))
            )

            # Loop through each piece found on the board
            for piece in pieces:
                # Get the class name of the piece, e.g., 'white queen', 'black king'
                piece_class = piece.get_attribute("class")

                # Extract the transform: translate(x, y) values using a regular expression
                transform_style = piece.get_attribute("style")
                match = re.search(r"translate\((\d+)px, (\d+)px\)", transform_style)

                if match:
                    x = int(match.group(1))  # x-coordinate
                    y = int(match.group(2))  # y-coordinate

                    # Add the piece info to the list
                    piece_positions.append({"piece": piece_class, "x": x, "y": y})

        except (NoSuchElementException, TimeoutException):
            print(f"Piece elements not found within {self.timeout} seconds.")

        except Exception as e:
            print(f"An error occurred: {e}")

        return piece_positions

    def map_pieces_to_squares(self, playing_as="white"):
        """
        Maps pieces (based on their pixel positions) to chess squares.

        Parameters:
        - playing_as: Whether the player is playing as "white" or "black"
        """
        # Generate the mapping of all chess squares to pixel coordinates
        square_pixel_mapping = self.generate_square_pixel_mapping(playing_as)

        piece_square_mapping = {}

        # Find the piece positions from the chessboard (cg-board)
        piece_positions = self.extract_piece_positions()

        # Loop through each piece and find the corresponding square
        for piece in piece_positions:
            x = piece["x"]
            y = piece["y"]

            # Find the square for the piece's (x, y) coordinates
            square = self.find_square_for_pixel(x, y, square_pixel_mapping)

            if square:
                piece_square_mapping[square] = piece["piece"]

        return piece_square_mapping

    def find_piece_element_for_square(self, square, square_pixel_mapping):
        """
        Finds the piece element on the chessboard corresponding to a given square based on the pixel mapping.

        Parameters:
        - square: The chess square (e.g., 'd4') to look for a piece.
        - square_pixel_mapping: A dictionary mapping squares to their pixel boundaries.
        - timeout: Maximum time to wait for the piece elements to be present.

        Returns:
        - The piece WebElement found on the specified square, or None if no piece is found.
        """
        try:
            # Get the pixel boundaries for the specified square
            boundaries = square_pixel_mapping.get(square, {})
            print(boundaries)
            if not boundaries:
                return None

            top_left_x, top_left_y = boundaries["top_left"]
            bottom_right_x, bottom_right_y = boundaries["bottom_right"]

            # Wait for the pieces to be present on the board
            pieces = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "cg-board piece"))
            )

            # Loop through each piece to find the one matching the square's pixel boundaries
            for piece in pieces:
                transform_style = piece.get_attribute("style")
                match = re.search(r"translate\((\d+)px, (\d+)px\)", transform_style)

                if match:
                    x = int(match.group(1))
                    y = int(match.group(2))

                    # Check if the piece is within the boundaries of the square
                    if (
                        top_left_x <= x < bottom_right_x
                        and top_left_y <= y < bottom_right_y
                    ):
                        return piece

        except (NoSuchElementException, TimeoutException):
            print(
                f"Piece elements not found for square {square} within {self.timeout} seconds."
            )

        except Exception as e:
            print(f"An error occurred while finding the piece on square {square}: {e}")

        return None

    def drag_and_drop_by_square(self, start_square, end_square, playing_as="white"):
        try:
            # Generate the pixel mappings
            square_pixel_mapping = self.generate_square_pixel_mapping(playing_as)

            # Find the starting piece element
            start_piece = self.find_piece_element_for_square(
                start_square, square_pixel_mapping
            )
            if not start_piece:
                print(f"Error: No piece found at {start_square}.")
                return

            # Get pixel coordinates for the start and end squares
            start_pixel = square_pixel_mapping.get(start_square, {}).get("top_left")
            end_pixel = square_pixel_mapping.get(end_square, {}).get("top_left")

            if not start_pixel or not end_pixel:
                print("Error: Invalid square notation.")
                return

            # Create an ActionChains object
            actions = ActionChains(self.browser)

            # Perform the drag-and-drop action using the piece element
            actions.click_and_hold(start_piece).move_by_offset(
                end_pixel[0] - start_pixel[0], end_pixel[1] - start_pixel[1]
            ).release().perform()

            print(f"Dragged from {start_square} to {end_square}.")

        except Exception as e:
            print(f"Error in drag and drop by square: {e}")

    def handle_pawn_promotion(self, move_san):
        """
        Detects if the move is a pawn promotion (e.g., g8=Q), and selects the correct
        promotion piece in the UI by clicking the appropriate element.

        Parameters:
        - browser: The Selenium WebDriver instance.
        - move_san: The SAN string of the move, e.g., 'g8=Q' for a promotion to queen.
        """
        promotion_match = re.match(r"([a-h][18])=(Q|N|R|B)([+#]?)", move_san)

        if not promotion_match:
            print("No prmotion detected")
            return

        else:

            promotion_square, promotion_piece, check_or_mate = promotion_match.groups()
            print(
                f"Promotion to {promotion_piece} on {promotion_square} with {check_or_mate if check_or_mate else 'no check or checkmate'}"
            )

            # Wait until the promotion choice UI is visible (with the correct ID)
            try:
                promotion_choice_element = WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located((By.ID, "promotion-choice"))
                )
            except TimeoutException:
                print("Promotion choice element not found.")
                return

            # Define a mapping of piece notation to the expected CSS class
            piece_class_mapping = {
                "Q": "queen",
                "N": "knight",
                "R": "rook",
                "B": "bishop",
            }

            # Get the piece class to select (e.g., 'queen', 'knight', etc.)
            piece_class = piece_class_mapping.get(promotion_piece)

            if not piece_class:
                print(f"Invalid promotion piece: {promotion_piece}")
                return

            # Find the correct piece element to click within the promotion choice UI
            try:
                # The pieces are inside squares, so find the correct square
                promotion_squares = promotion_choice_element.find_elements(
                    By.CSS_SELECTOR, "square"
                )

                for square in promotion_squares:
                    piece = square.find_element(By.CSS_SELECTOR, "piece")
                    piece_class_attribute = piece.get_attribute("class")

                    if piece_class in piece_class_attribute:
                        # Found the correct promotion piece, now click on it
                        square.click()
                        print(f"Clicked on promotion piece: {piece_class}")
                        break
                else:
                    print(f"Could not find the promotion piece: {promotion_piece}")
            except NoSuchElementException:
                print(f"Error: Could not find elements for promotion selection.")

    def detect_last_table_move_and_count(self, playing_as="white"):
        """
        Detects the computer's move from the move table and ensures the move count has increased.

        Parameters:
        - board: The current board object to parse the move into UCI format.
        - previous_move_count: The total number of moves detected previously.
        - self.timeout: Maximum time (in seconds) to wait for the move table to appear.

        Returns:
        - computer_move: The computer's latest move in SAN format.
        - current_move_count: The updated move count.
        """
        try:
            # Wait until the move history table is present and visible
            move_table = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "l4x"))
            )

            # Find all move elements in the table (each move is in a <kwdb> tag)
            move_elements = move_table.find_elements(By.CSS_SELECTOR, "kwdb")

            # Get the total count of moves from all elements (both white and black)
            current_move_count = len(move_elements)

            # Get the last move element (latest move made)
            if playing_as == "white":

                last_move_element = move_elements[-1]
            else:
                last_move_element = move_elements[-2]

            computer_move = last_move_element.text.strip()  # Extract the move text

            # Return the detected move and the updated move count
            return computer_move, current_move_count

        except (NoSuchElementException, TimeoutException):
            print("Move history table or move element not found.")
            return None, None

    def detect_is_time_over(self):
        return False

    def wait_for_computer_move(
        self,
        previous_move,
        previous_move_count,
        playing_as="white",
        loop_speed=0.1,
        timeout=10,
    ):
        """
        Loops until a new computer move is detected, based on move count and the difference
        from the previous move. Stops after a specified timeout.

        Parameters:
        - previous_move: The last detected move (to avoid returning the same move).
        - previous_move_count: The total number of moves detected previously.
        - playing_as: Whether the player is "white" or "black".
        - loop_speed: Time to wait between checks (in seconds).
        - timeout: Maximum time (in seconds) to wait for a new move.

        Returns:
        - computer_move: The new computer move if detected within the timeout period.
        - None: If no new move is detected within the timeout period.
        """
        start_time = time.time()  # Record the start time

        while True:
            # Detect the current move and move count
            last_move, current_move_count = self.detect_last_table_move_and_count(
                playing_as
            )

            # Check if the move count has increased and the last move is different
            if current_move_count > previous_move_count and last_move != previous_move:
                print(f"New computer move detected: {last_move}")
                return last_move

            # Optional: Print status for debugging
            print(
                f"Waiting for new computer move... (Current move count: {current_move_count})"
            )

            # Check if the timeout has been reached
            if time.time() - start_time > timeout:
                print(f"Timeout reached after {timeout} seconds. No new move detected.")
                return None

            # Small timeout before the next check to avoid excessive CPU usage
            time.sleep(loop_speed)
