"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """ A behaviour that penalize opponent player when the upperbound limit is exceeded
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    active_player_moves = len(game.get_legal_moves(player))
    opponent_player_moves = len(game.get_legal_moves(game.get_opponent(player)))

    if active_player_moves is 0:
        return float("-inf")

    if opponent_player_moves is 0:
        return float("inf")

    available_positions = len(game.get_blank_spaces())

    total_positions = game.height * game.width
    limit = float(total_positions / 2)
    weight_1 = float(limit / available_positions)
    weight_2 = float(available_positions / limit)
    return float(weight_1 * active_player_moves - weight_2 * opponent_player_moves)

def custom_score_2(game, player):
    """ A simply division of player moves by opponent moves
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    player_moves = len(game.get_legal_moves(player))
    if game.is_loser(player) or player_moves is 0:
        return float("-inf")

    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    if game.is_winner(player) or opponent_moves is 0:
        return float("inf")

    return float(player_moves / opponent_moves)


def custom_score_3(game, player):
    """ A non-Euclidean distance between points as score function

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")


    active_x, active_y = game.get_player_location(game.active_player)

    center_x, center_y = int(game.width / 2), int(game.height / 2)

    active_distance = abs(active_x - active_y) + abs(center_x - center_y)

    return float(active_distance)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def terminal_check(self, game):
        return True if len(game.get_legal_moves()) == 0 else False

    def timer_check(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        self.timer_check()

        if len(game.get_legal_moves()) is 0:
            return (-1, -1)

        moves = [(move, self.__min_value(game.forecast_move(move), depth - 1))
                 for move in game.get_legal_moves()]

        best_action_move = max(moves, key=lambda move: move[1])

        best_action = best_action_move[0]

        return best_action

    def __max_value(self, game, depth):
        """
            This function go through the whole game tree to the leaves and determines
            the backed-up max value of a state
                :param game: the current board state
                :return: the max value of a current board state
        """
        self.timer_check()
        value = float("-inf")
        if self.terminal_check(game):
            return game.utility(game.active_player)
        if depth == 0:
            return self.score(game, game.active_player)
        for move in game.get_legal_moves():
            post_game_value = self.__min_value(game.forecast_move(move), depth - 1)
            value = max(value, post_game_value)
        return value

    def __min_value(self, game, depth):
        """
            This function go through the whole game tree to the leaves and determines
            the backed-up min value of a state
                :param game: the current board state
                :return: the max value of a current board state
        """
        self.timer_check()
        value = float("+inf")
        if self.terminal_check(game):
            return game.utility(game.inactive_player)
        if depth == 0:
            return self.score(game, game.inactive_player)
        for move in game.get_legal_moves():
            post_game_value = self.__max_value(game.forecast_move(move), depth - 1)
            value = min(value, post_game_value)
        return value

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        best_move = (-1, -1)
        depth = 1
        try:
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1
        except SearchTimeout:
            pass
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if len(game.get_legal_moves()) is 0:
            return (-1, -1)

        score = float("-inf")
        best_action = (-1, -1)

        for move in game.get_legal_moves():
            value = self.__min_value(game.forecast_move(move), depth - 1, alpha, beta)
            alpha = max(alpha, value)
            if value >= score:
                score = value
                best_action = move
            if beta <= alpha:
                break

        return best_action


    def __max_value(self, game, depth, alpha, beta):
        self.timer_check()
        value = float("-inf")
        if self.terminal_check(game):
            return game.utility(game.active_player)
        if depth == 0:
            return self.score(game, game.active_player)
        for move in game.get_legal_moves():
            post_game_value = self.__min_value(game.forecast_move(move), depth - 1, alpha, beta)
            value = max(value, post_game_value)
            if post_game_value >= beta:
                return post_game_value
            alpha = max(alpha, post_game_value)
            if beta <= alpha:
                break
        return value

    def __min_value(self, game, depth, alpha, beta):
        self.timer_check()
        value = float("+inf")
        if self.terminal_check(game):
            return game.utility(game.inactive_player)
        if depth == 0:
            return self.score(game, game.inactive_player)
        for move in game.get_legal_moves():
            post_game_value = self.__max_value(game.forecast_move(move), depth - 1, alpha, beta)
            value = min(value, post_game_value)
            if post_game_value <= alpha:
                return post_game_value
            beta = min(beta, post_game_value)
            if beta <= alpha:
                break
        return value
