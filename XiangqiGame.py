# Author: Christopher Vu
# Date: 3/3/2020
# Description: Xiangqi. Chinese Chess.


class XiangqiGame:
    def __init__(self):
        """
        Initializes a game of Xiangqi with piece objects in an array that
        represents the board. Game state is initialized unfinished.
        The player turn is initialized to red. Both players are not in check so
        their booleans are initialized to False. There are dictionaries for
        Xiangqi coordinate to index conversion. There are methods for getting
        the objects at a coordinate on the board, getting the game state,
        checking whether a red or black are in check, moving a piece, and
        printing the board.
        """
        # All red pieces are initialized here with their respective coordinates
        self._rG = redGeneral()
        self._rA1 = redAdvisor('d1')
        self._rA2 = redAdvisor('f1')

        self._rS1 = redSoldier('a4')
        self._rS2 = redSoldier('c4')
        self._rS3 = redSoldier('e4')
        self._rS4 = redSoldier('g4')
        self._rS5 = redSoldier('i4')

        self._rH1 = redHorse('b1')
        self._rH2 = redHorse('h1')

        self._rE1 = redElephant('c1')
        self._rE2 = redElephant('g1')

        self._rC1 = redCannon('b3')
        self._rC2 = redCannon('h3')

        self._rR1 = redRook('a1')
        self._rR2 = redRook('i1')

        # Black Pieces
        self._bG = blackGeneral()
        self._bA1 = blackAdvisor('d10')
        self._bA2 = blackAdvisor('f10')

        self._bS1 = blackSoldier('a7')
        self._bS2 = blackSoldier('c7')
        self._bS3 = blackSoldier('e7')
        self._bS4 = blackSoldier('g7')
        self._bS5 = blackSoldier('i7')

        self._bH1 = blackHorse('b10')
        self._bH2 = blackHorse('h10')

        self._bE1 = blackElephant('c10')
        self._bE2 = blackElephant('g10')

        self._bC1 = blackCannon('b8')
        self._bC2 = blackCannon('h8')

        self._bR1 = blackRook('a10')
        self._bR2 = blackRook('i10')

        # This game board array will be initialized with all pieces in their
        # starting position.
        self._board = [[self._bR1, self._bH1, self._bE1, self._bA1, self._bG, self._bA2, self._bE2, self._bH2, self._bR2],
                       ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
                       ['--', self._bC1, '--', '--', '--', '--', '--', self._bC2, '--'],
                       [self._bS1, '--', self._bS2, '--', self._bS3, '--', self._bS4, '--', self._bS5],
                       ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
                       ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
                       [self._rS1, '--', self._rS2, '--', self._rS3, '--', self._rS4, '--', self._rS5],
                       ['--', self._rC1, '--', '--', '--', '--', '--', self._rC2, '--'],
                       ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
                       [self._rR1, self._rH1, self._rE1, self._rA1, self._rG, self._rA2, self._rE2, self._rH2, self._rR2]]

        # Game initialized to unfinished. Will be updated as the game goes.
        # Can be 'RED_WON' or 'BLACK_WON'
        self._game_state = "UNFINISHED"

        # Initialize to red's turn
        self._turn = 'r'
        # Red and Black initialized to not in check
        self._rCheck = False
        self._bCheck = False

        # Used for converting between Xiangqi coordinates and array indexing
        self._column_pairs = {
            'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
            'h': 7,
            'i': 8
        }
        self._row_pairs = {
            '10': 0,
            '9': 1,
            '8': 2,
            '7': 3,
            '6': 4,
            '5': 5,
            '4': 6,
            '3': 7,
            '2': 8,
            '1': 9
        }

    def get_board(self):
        """Returns the board"""
        return self._board

    def change_turn(self):
        """Passes turn to next player"""
        if self._turn == 'r':
            self._turn = 'b'
        else:
            self._turn = 'r'

    def get_index_from_coord(self, coord):
        """Given a Xiangqi board coordinate string, returns a list containing
        the respective row and column indexes for that coordinate."""
        # In the case that the coordinate string is 3 characters long, that
        # means the rank is 10
        if len(coord) == 3:
            row_index = self._row_pairs[coord[1:]]
        else:
            row_index = self._row_pairs[coord[1]]
        column_index = self._column_pairs[coord[0]]
        return [row_index, column_index]

    def get_object_from_coord(self, coord):
        """Gets object given Xiangqi coordinate string by converting the
        coordinates to index values and then returning the object from the board
        array"""
        if len(coord) == 3:
            row_index = self._row_pairs[coord[1:]]
        else:
            row_index = self._row_pairs[coord[1]]
        column_index = self._column_pairs[coord[0]]
        return self._board[row_index][column_index]

    def get_game_state(self):
        """Returns the state of the game. UNFINISHED, 'RED_WON', 'BLACK_WON'"""
        return self._game_state

    def is_in_check(self, color):
        """Given color as a string, returns whether the color is in check"""
        if color == 'red':
            return self._rCheck
        elif color == 'black':
            return self._bCheck

    def make_move(self, source, destination):
        """Given a source and destination coordinate as strings, moves piece
        from source to destination"""

        # If the game is over
        if self._game_state != "UNFINISHED":
            return False

        # This is the object at the source coordinate's index
        source_item = self.get_object_from_coord(source)
        source_index = self.get_index_from_coord(source)
        dest_index = self.get_index_from_coord(destination)

        # If the source is empty, or it isn't the source's turn, return False
        if source_item == '--' or source_item.get_color() != self._turn:
            return False

        # Get the legal destinations list for the piece by calling
        # legality_check. At this point, moves that cause self check or flying
        # general are included in the list.
        legal_destinations = self.legality_check(source_item)

        # A copy of the legal destinations list is made for iteration
        copy_legal_destinations = legal_destinations.copy()
        # Iterate through the legal destinations list to remove pieces that
        # cause self check. This is done by performing the move, checking for
        # check, and then resetting the board.
        for coord in copy_legal_destinations:
            coord_index = self.get_index_from_coord(coord)
            coord_item = self.get_object_from_coord(coord)

            # Move the piece from the source to the destination testing for self
            # check

            # Update the piece's coordinate, update board by moving piece to
            # destination and by clearing the source coordinates spot on the
            # board.
            source_item.update_coordinate(coord)
            self._board[coord_index[0]][coord_index[1]] = source_item
            self._board[source_index[0]][source_index[1]] = '--'

            # Check if that move causes self check, if so remove it as a legal
            # destination
            if self.check_for_check() is True:
                legal_destinations.remove(coord)

            # Reset the board
            self._board[source_index[0]][source_index[1]] = source_item
            self._board[coord_index[0]][coord_index[1]] = coord_item
            source_item.update_coordinate(source)

        # If the given destination is not in the list of legal destinations
        if destination not in legal_destinations:
            return False

        # Make the move, update player's check status, pass turn to next player,
        # update player's check status, check if current player has any legal
        # moves left, update game state, return True
        else:
            # Make the move
            source_item.update_coordinate(destination)
            self._board[dest_index[0]][dest_index[1]] = source_item
            self._board[source_index[0]][source_index[1]] = '--'

            # Update current player's check status
            currently_in_check = self.check_for_check()
            if currently_in_check:
                if self._turn == 'r':
                    self._rCheck = True
                elif self._turn == 'b':
                    self._bCheck = True
            elif currently_in_check is False:
                if self._turn == 'r':
                    self._rCheck = False
                elif self._turn == 'b':
                    self._bCheck = False

            # Change the turn the the next player
            self.change_turn()

            # Update the current player's check status
            current_in_check = self.check_for_check()
            if current_in_check:
                if self._turn == 'r':
                    self._rCheck = True
                elif self._turn == 'b':
                    self._bCheck = True
            elif current_in_check is False:
                if self._turn == 'r':
                    self._rCheck = False
                elif self._turn == 'b':
                    self._bCheck = False

            # There are no legal moves for the current player until one if found
            no_legal_moves = True

            # Loop through all of the pieces in the board
            for row in self._board:
                for item in row:
                    if item != '--':
                        # If it's b's turn, only check legal moves for black
                        if self._turn == 'b' and item.get_color() == 'b':
                            l_d = self.legality_check(item)

                            # Iterate through the legal destinations list to
                            # remove pieces that cause self check. This is done
                            # by performing the move, checking for check, and
                            # then resetting the board.
                            copy_l_d = l_d.copy()
                            for destination in copy_l_d:
                                destination_index = self.get_index_from_coord(destination)
                                destination_item = self.get_object_from_coord(destination)
                                item_coord = item.get_coordinate()
                                item_index = self.get_index_from_coord(item_coord)

                                item.update_coordinate(destination)
                                self._board[destination_index[0]][destination_index[1]] = item
                                self._board[item_index[0]][item_index[1]] = '--'

                                if self.check_for_check() is True:
                                    l_d.remove(destination)

                                self._board[item_index[0]][item_index[1]] = item
                                self._board[destination_index[0]][destination_index[1]] = destination_item
                                item.update_coordinate(item_coord)
                            # If any legal moves are found for this black piece,
                            # there are legal moves
                            if len(l_d) > 0:
                                no_legal_moves = False
                        # Same as above but for red pieces
                        elif self._turn == 'r' and item.get_color() == 'r':
                            l_d = self.legality_check(item)
                            copy_l_d = l_d.copy()
                            for destination in copy_l_d:
                                destination_index = self.get_index_from_coord(
                                    destination)
                                destination_item = self.get_object_from_coord(
                                    destination)
                                item_coord = item.get_coordinate()
                                item_index = self.get_index_from_coord(
                                    item_coord)

                                item.update_coordinate(destination)
                                self._board[destination_index[0]][
                                    destination_index[1]] = item
                                self._board[item_index[0]][item_index[1]] = '--'

                                if self.check_for_check() is True:
                                    l_d.remove(destination)

                                self._board[item_index[0]][item_index[1]] = item
                                self._board[destination_index[0]][
                                    destination_index[1]] = destination_item
                                item.update_coordinate(item_coord)

                            if len(l_d) > 0:
                                no_legal_moves = False

            # If there are no legal moves for the current player, update the
            # game state
            if no_legal_moves and self._turn == 'b':
                self._game_state = 'RED_WON'
            elif no_legal_moves and self._turn == 'r':
                self._game_state = 'BLACK_WON'
        return True

    def print_board(self):
        """Prints the board by iterating through it"""
        print('==========================')
        for row in self._board:
            for item in row:
                if item != '--':
                    print(item.print_piece(), end=" ")
                else:
                    print(item, end=" ")
            print()
        print('==========================')

    def check_for_check(self):
        """Checks if the current player is in check. Used for removing
        illegal moves. Returns True if in check, False otherwise"""
        # Call flying general to check if it has occurred
        flying_general = self.is_flying_general()
        if flying_general:
            return True
        # If it's red's turn, loop through the board and check black legal moves
        # to see if any of them contain's red general's coordinate
        for row in self._board:
            for item in row:
                if item != '--':
                    if self._turn == 'r':
                        if item.get_color() == 'b':
                            legal_dest = self.legality_check(item)
                            for legal_d in legal_dest:
                                if legal_d == self._rG.get_coordinate():
                                    return True
                    elif self._turn == 'b':
                        if item.get_color() == 'r':
                            legal_dest = self.legality_check(item)
                            for legal_d in legal_dest:
                                if legal_d == self._bG.get_coordinate():
                                    return True
        return False

    def is_flying_general(self):
        """Returns True if the space between the generals is empty, False if
        not."""
        # Coordinates of red and black generals
        rG_coord = self._rG.get_coordinate()
        bG_coord = self._bG.get_coordinate()
        # If the generals are in the same file, check if the space is empty
        # between them
        if rG_coord[0] == bG_coord[0]:
            file_index = self._column_pairs[bG_coord[0]]
            bG_rank_index = self._row_pairs[bG_coord[1:]]
            rG_rank_index = self._row_pairs[rG_coord[1:]]
            # Iterates through the pieces between the two generals to see if any
            # contain a piece. If so, return False, otherwise True
            for rank_index in range(bG_rank_index + 1, rG_rank_index):
                if self._board[rank_index][file_index] != '--':
                    return False
            return True
        # If the generals are not in the same file, False is returned
        return False

    def legality_check(self, piece):
        """Takes a piece, returns a list of legal moves including illegal
        self check moves as string coordinates."""
        # Coordinate of piece, name of piece, legal coordinates initialized to
        # empty list
        piece_coord = piece.get_coordinate()
        piece_type = piece.print_piece()
        legal_coords = []

        # Generals
        if piece_type == 'rG' or piece_type == 'bG':
            # These are the coordinates for destinations for general moves
            above_coord = piece_coord[0] + str(int(piece_coord[1:]) + 1)
            below_coord = piece_coord[0] + str(int(piece_coord[1:]) - 1)
            left_coord = chr(ord(piece_coord[0]) - 1) + piece_coord[1:]
            right_coord = chr(ord(piece_coord[0]) + 1) + piece_coord[1:]

            # If the piece is red General
            if piece_type == 'rG':
                # Initialize the legal destination coordinates to the in bounds
                # destination coordinates. Check's the general's starting
                # location and creates a list of the destination coordinates
                # that are in bounds.
                if piece_coord == 'e1':
                    legal_coords = [above_coord, left_coord, right_coord]
                elif piece_coord == 'd1':
                    legal_coords = [above_coord, right_coord]
                elif piece_coord == 'f1':
                    legal_coords = [above_coord, left_coord]

                elif piece_coord == 'e2':
                    legal_coords = [above_coord, below_coord, left_coord,
                                      right_coord]
                elif piece_coord == 'd2':
                    legal_coords = [above_coord, below_coord, right_coord]
                elif piece_coord == 'f2':
                    legal_coords = [above_coord, below_coord, left_coord]

                elif piece_coord == 'e3':
                    legal_coords = [below_coord, left_coord, right_coord]
                elif piece_coord == 'd3':
                    legal_coords = [below_coord, right_coord]
                elif piece_coord == 'f3':
                    legal_coords = [below_coord, left_coord]

            elif piece_type == 'bG':
                # Initialize the legal destination coordinates to the in bounds
                # destination coordinates. Check's the general's starting
                # location and creates a list of the destination coordinates
                # that are in bounds.
                if piece_coord == 'e10':
                    legal_coords = [below_coord, left_coord, right_coord]
                elif piece_coord == 'd10':
                    legal_coords = [below_coord, right_coord]
                elif piece_coord == 'f10':
                    legal_coords = [below_coord, left_coord]

                elif piece_coord == 'e9':
                    legal_coords = [above_coord, below_coord, left_coord,
                                    right_coord]
                elif piece_coord == 'd9':
                    legal_coords = [above_coord, below_coord, right_coord]
                elif piece_coord == 'f9':
                    legal_coords = [above_coord, below_coord, left_coord]

                elif piece_coord == 'e8':
                    legal_coords = [above_coord, left_coord, right_coord]
                elif piece_coord == 'd8':
                    legal_coords = [above_coord, right_coord]
                elif piece_coord == 'f8':
                    legal_coords = [above_coord, left_coord]

        # Advisor. If piece is red of black advisor
        elif piece_type == 'rA' or piece_type == 'bA':
            # Coordinates for destinations for advisor moves
            up_l = chr(ord(piece_coord[0]) - 1) + str(int(piece_coord[1:]) + 1)
            up_r = chr(ord(piece_coord[0]) + 1) + str(int(piece_coord[1:]) + 1)
            down_l = chr(ord(piece_coord[0]) - 1) + str(int(piece_coord[1:]) - 1)
            down_r = chr(ord(piece_coord[0]) + 1) + str(int(piece_coord[1:]) - 1)

            # Fill list with legal moves for advisors based on their coordinate
            if piece_type == 'rA':
                if piece_coord == 'd1':
                    legal_coords = [up_r]
                elif piece_coord == 'f1':
                    legal_coords = [up_l]
                elif piece_coord == 'd3':
                    legal_coords = [down_r]
                elif piece_coord == 'f3':
                    legal_coords = [down_l]
                elif piece_coord == 'e2':
                    legal_coords = [up_l, up_r, down_l, down_r]

            elif piece_type == 'bA':
                if piece_coord == 'd10':
                    legal_coords = [down_r]
                elif piece_coord == 'f10':
                    legal_coords = [down_l]
                elif piece_coord == 'd8':
                    legal_coords = [up_r]
                elif piece_coord == 'f8':
                    legal_coords = [up_l]
                elif piece_coord == 'e9':
                    legal_coords = [up_l, up_r, down_l, down_r]

        # Red Soldier
        elif piece_type == 'rS':
            # Coordinates for destinations for red soldier moves
            above_coord = piece_coord[0] + str(int(piece_coord[1:]) + 1)
            left_coord = chr(ord(piece_coord[0]) - 1) + piece_coord[1:]
            right_coord = chr(ord(piece_coord[0]) + 1) + piece_coord[1:]

            # If the soldier is not beyond the river, they can move forward only
            # If they are beyond the river, check edge cases such as corners,
            # left edge, right edge, and top edge
            if int(piece_coord[1:]) < 6:
                legal_coords = [above_coord]
            elif piece_coord == 'a10':
                legal_coords = [right_coord]
            elif piece_coord == 'i10':
                legal_coords = [left_coord]
            elif piece_coord[0] == 'a':
                legal_coords = [above_coord, right_coord]
            elif piece_coord[0] == 'i':
                legal_coords = [above_coord, left_coord]
            elif piece_coord[1:] == '10':
                legal_coords = [left_coord, right_coord]
            else:
                legal_coords = [above_coord, left_coord, right_coord]

        # Black Soldier
        elif piece_type == 'bS':
            # Coordinates for destinations for red soldier moves
            below_coord = piece_coord[0] + str(int(piece_coord[1:]) - 1)
            left_coord = chr(ord(piece_coord[0]) - 1) + piece_coord[1:]
            right_coord = chr(ord(piece_coord[0]) + 1) + piece_coord[1:]

            # If the soldier is not beyond the river, they can move forward only
            # If they are beyond the river, check edge cases such as corners,
            # left edge, right edge, and top edge
            if int(piece_coord[1:]) > 5:
                legal_coords = [below_coord]
            elif piece_coord == 'a1':
                legal_coords = [right_coord]
            elif piece_coord == 'i1':
                legal_coords = [left_coord]
            elif piece_coord[0] == 'a':
                legal_coords = [below_coord, right_coord]
            elif piece_coord[0] == 'i':
                legal_coords = [below_coord, left_coord]
            elif piece_coord[1:] == '1':
                legal_coords = [left_coord, right_coord]
            else:
                legal_coords = [below_coord, left_coord, right_coord]

        # Red Horse or black horse
        elif piece_type == 'rH' or piece_type == 'bH':
            # Coordinates for destinations for horse moves
            up_l = chr(ord(piece_coord[0])-1) + str(int(piece_coord[1:])+2)
            up_r = chr(ord(piece_coord[0])+1) + str(int(piece_coord[1:])+2)
            down_l = chr(ord(piece_coord[0])-1) + str(int(piece_coord[1:])-2)
            down_r = chr(ord(piece_coord[0])+1) + str(int(piece_coord[1:])-2)
            l_up = chr(ord(piece_coord[0])-2) + str(int(piece_coord[1:])+1)
            l_down = chr(ord(piece_coord[0])-2) + str(int(piece_coord[1:])-1)
            r_up = chr(ord(piece_coord[0])+2) + str(int(piece_coord[1:])+1)
            r_down = chr(ord(piece_coord[0])+2) + str(int(piece_coord[1:])-1)

            # Coordinates neighboring horse piece
            up = piece_coord[0] + str(int(piece_coord[1:]) + 1)
            down = piece_coord[0] + str(int(piece_coord[1:]) - 1)
            left = chr(ord(piece_coord[0]) - 1) + piece_coord[1:]
            right = chr(ord(piece_coord[0]) + 1) + piece_coord[1:]

            # Legal coords initialized to all destination coordinates, even out
            # of bounds. Same with neighbor coords list
            legal_coords = [up_l, up_r, down_l, down_r, l_up, l_down, r_up, r_down]
            neighbor_coords = [up, down, left, right]

            # Remove out of bound destinations
            c_legal_coords = legal_coords.copy()
            for coord in c_legal_coords:
                if ord(coord[0]) > ord('i'):
                    legal_coords.remove(coord)
                elif ord(coord[0]) < ord('a'):
                    legal_coords.remove(coord)
                elif int(coord[1:]) > 10:
                    legal_coords.remove(coord)
                elif int(coord[1:]) < 1:
                    legal_coords.remove(coord)

            # Remove out of bound neighboring coordinates
            c_neighbor_coords = neighbor_coords.copy()
            for coord in c_neighbor_coords:
                if ord(coord[0]) > ord('i'):
                    neighbor_coords.remove(coord)
                elif ord(coord[0]) < ord('a'):
                    neighbor_coords.remove(coord)
                elif int(coord[1:]) > 10:
                    neighbor_coords.remove(coord)
                elif int(coord[1:]) < 1:
                    neighbor_coords.remove(coord)

            # Remove hobbled destinations using the neighboring coordinates
            for coord in neighbor_coords:
                item_at_coord = self.get_object_from_coord(coord)
                if item_at_coord != '--':
                    if coord == up:
                        if up_l in legal_coords:
                            legal_coords.remove(up_l)
                        if up_r in legal_coords:
                            legal_coords.remove(up_r)
                    elif coord == down:
                        if down_l in legal_coords:
                            legal_coords.remove(down_l)
                        if down_r in legal_coords:
                            legal_coords.remove(down_r)
                    elif coord == left:
                        if l_up in legal_coords:
                            legal_coords.remove(l_up)
                        if l_down in legal_coords:
                            legal_coords.remove(l_down)
                    elif coord == right:
                        if r_up in legal_coords:
                            legal_coords.remove(r_up)
                        if r_down in legal_coords:
                            legal_coords.remove(r_down)

        # Elephants
        elif piece_type == 'rE' or piece_type == 'bE':
            # Coordinates for destinations for elephant moves
            up_l = chr(ord(piece_coord[0]) - 2) + str(int(piece_coord[1:]) + 2)
            up_r = chr(ord(piece_coord[0]) + 2) + str(int(piece_coord[1:]) + 2)
            down_l = chr(ord(piece_coord[0]) - 2) + str(int(piece_coord[1:]) - 2)
            down_r = chr(ord(piece_coord[0]) + 2) + str(int(piece_coord[1:]) - 2)

            n_up_l = chr(ord(piece_coord[0]) - 1) + str(int(piece_coord[1:]) + 1)
            n_up_r = chr(ord(piece_coord[0]) + 1) + str(int(piece_coord[1:]) + 1)
            n_down_l = chr(ord(piece_coord[0]) - 1) + str(int(piece_coord[1:]) - 1)
            n_down_r = chr(ord(piece_coord[0]) + 1) + str(int(piece_coord[1:]) - 1)

            # Legal coords initialized to all destination coordinates, even out
            # of bounds. Same with neighbor coords list
            legal_coords = [up_l, up_r, down_l, down_r]
            neighbor_coords = [n_up_l, n_up_r, n_down_l, n_down_r]

            # Remove out of bound destinations
            c_legal_coords = legal_coords.copy()
            for coord in c_legal_coords:
                if ord(coord[0]) > ord('i'):
                    legal_coords.remove(coord)
                elif ord(coord[0]) < ord('a'):
                    legal_coords.remove(coord)
                elif int(coord[1:]) > 10:
                    legal_coords.remove(coord)
                elif int(coord[1:]) < 1:
                    legal_coords.remove(coord)

            # Remove out of bound neighboring coordinates
            c_neighbor_coords = neighbor_coords.copy()
            for coord in c_neighbor_coords:
                if ord(coord[0]) > ord('i'):
                    neighbor_coords.remove(coord)
                elif ord(coord[0]) < ord('a'):
                    neighbor_coords.remove(coord)
                elif int(coord[1:]) > 10:
                    neighbor_coords.remove(coord)
                elif int(coord[1:]) < 1:
                    neighbor_coords.remove(coord)

            # Remove blocked destinations using the neighboring coordinates
            for coord in neighbor_coords:
                item_at_coord = self.get_object_from_coord(coord)
                if item_at_coord != '--':
                    if coord == n_up_l:
                        if up_l in legal_coords:
                            legal_coords.remove(up_l)
                    elif coord == n_up_r:
                        if up_r in legal_coords:
                            legal_coords.remove(up_r)
                    elif coord == n_down_l:
                        if down_l in legal_coords:
                            legal_coords.remove(down_l)
                    elif coord == n_down_r:
                        if down_r in legal_coords:
                            legal_coords.remove(down_r)

            # Remove moves that cross the river
            if piece_coord == 'c5' or piece_coord == 'g5':
                if up_l in legal_coords:
                    legal_coords.remove(up_l)
                if up_r in legal_coords:
                    legal_coords.remove(up_r)
            elif piece_coord == 'c6' or piece_coord == 'g6':
                if down_l in legal_coords:
                    legal_coords.remove(down_l)
                if down_r in legal_coords:
                    legal_coords.remove(down_r)

        # Rooks
        elif piece_type == 'rR' or piece_type == 'bR':
            # These are distances between the edges and the rook piece
            right = ord('i') - ord(piece_coord[0])
            left = ord(piece_coord[0]) - ord('a')
            up = 10 - int(piece_coord[1:])
            down = int(piece_coord[1:]) - 1

            distance = [right, left, up, down]

            # Loop through distance, loop through the coordinate between the
            # piece and the edge to find adjacent pieces. If they are found, add
            # as a legal destination for the rook piece
            n = 0
            while n < 4:
                direction = distance[n]
                # If it's the first value from distance. Distance between right
                # edge and piece
                if n == 0:
                    for i in range(1, direction + 1):
                        # Get the coordinate to the right, then get the object
                        # from the coordinate
                        right_coord = chr(ord(piece_coord[0]) + i) + piece_coord[1:]
                        object_rc = self.get_object_from_coord(right_coord)
                        legal_coords.append(right_coord)
                        if object_rc != '--':
                            break
                # Distance between left edge and piece
                elif n == 1:
                    for i in range(1, direction + 1):
                        # Get the coordinate to the left, then get the object
                        # from the coordinate, append the coordinate
                        left_coord = chr(ord(piece_coord[0]) - i) + piece_coord[1:]
                        object_lc = self.get_object_from_coord(left_coord)
                        legal_coords.append(left_coord)
                        # If the coordinate contains a piece, break
                        if object_lc != '--':
                            break
                # Distance between top edge and piece
                elif n == 2:
                    for i in range(1, direction + 1):
                        up_coord = piece_coord[0] + str(int(piece_coord[1:]) + i)
                        object_uc = self.get_object_from_coord(up_coord)
                        legal_coords.append(up_coord)
                        if object_uc != '--':
                            break
                # Distance between bottom edge and piece
                elif n == 3:
                    for i in range(1, direction + 1):
                        down_coord = piece_coord[0] + str(int(piece_coord[1:]) - i)
                        object_dc = self.get_object_from_coord(down_coord)
                        legal_coords.append(down_coord)
                        if object_dc != '--':
                            break
                n += 1

        # Cannons
        elif piece_type == 'rC' or piece_type == 'bC':
            # These are distances between the edges and the cannon piece
            right = ord('i') - ord(piece_coord[0])
            left = ord(piece_coord[0]) - ord('a')
            up = 10 - int(piece_coord[1:])
            down = int(piece_coord[1:]) - 1

            # The distances are put in a list, neighbor_coords will contain the
            # coordinate of an adjacent piece for the respective direction if it
            # exists. If it does exist, piece_adjacent will be changed to 1 for
            # that direction. Index: 0, 1, 2, 3 / right, left, up, down
            distance = [right, left, up, down]
            neighbor_coords = [0, 0, 0, 0]
            piece_adjacent = [0, 0, 0, 0]

            # Loop through board, direction by direction, append empty spaces
            # until reaching another piece or the edge, same fashion as rooks
            n = 0
            while n < 4:
                direction = distance[n]
                # If right
                if n == 0:
                    # Iterate through spaces to right of piece
                    for i in range(1, direction + 1):
                        right_coord = chr(ord(piece_coord[0]) + i) + piece_coord[1:]
                        object_rc = self.get_object_from_coord(right_coord)
                        # If the coordinate contains a piece, append that as an
                        # adjacent piece for the 0th index in neighbor_coords
                        if object_rc != '--':
                            neighbor_coords[n] = right_coord
                            piece_adjacent[n] = 1
                            break
                        # If there is not piece, add the coordinate as a legal
                        # destination
                        legal_coords.append(right_coord)
                # If left
                elif n == 1:
                    for i in range(1, direction + 1):
                        left_coord = chr(ord(piece_coord[0]) - i) + piece_coord[1:]
                        object_lc = self.get_object_from_coord(left_coord)
                        if object_lc != '--':
                            neighbor_coords[n] = left_coord
                            piece_adjacent[n] = 1
                            break
                        legal_coords.append(left_coord)
                # If up
                elif n == 2:
                    for i in range(1, direction + 1):
                        up_coord = piece_coord[0] + str(int(piece_coord[1:]) + i)
                        object_uc = self.get_object_from_coord(up_coord)
                        if object_uc != '--':
                            neighbor_coords[n] = up_coord
                            piece_adjacent[n] = 1
                            break
                        legal_coords.append(up_coord)
                # If down
                elif n == 3:
                    for i in range(1, direction + 1):
                        down_coord = piece_coord[0] + str(int(piece_coord[1:]) - i)
                        object_dc = self.get_object_from_coord(down_coord)
                        if object_dc != '--':
                            neighbor_coords[n] = down_coord
                            piece_adjacent[n] = 1
                            break
                        legal_coords.append(down_coord)
                n += 1

            # Appends legal destinations for directions that contain adjacent
            # pieces. Used to append where the cannon jumps to.
            j = 0
            # Loop through the four directions
            while j < 4:
                # If it is the case that there is a piece adjacent to the right
                if j == 0 and piece_adjacent[j] == 1:
                    right_dist = ord('i') - ord(neighbor_coords[j][0])
                    # Loop through the spaces between the right adjacent piece
                    # and the edge.
                    for i in range(1, right_dist + 1):
                        right_coord = chr(ord(neighbor_coords[j][0]) + i) + neighbor_coords[j][1:]
                        object_rc = self.get_object_from_coord(right_coord)
                        # If a piece is found, append it as a destination
                        if object_rc != '--':
                            legal_coords.append(right_coord)
                            break
                # Adjacent piece to left
                elif j == 1 and piece_adjacent[j] == 1:
                    left_dist = ord(neighbor_coords[j][0]) - ord('a')
                    for i in range(1, left_dist + 1):
                        left_coord = chr(ord(neighbor_coords[j][0]) - i) + neighbor_coords[j][1:]
                        object_lc = self.get_object_from_coord(left_coord)
                        if object_lc != '--':
                            legal_coords.append(left_coord)
                            break
                # Adjacent piece above
                elif j == 2 and piece_adjacent[j] == 1:
                    up_dist = 10 - int(neighbor_coords[j][1:])
                    for i in range(1, up_dist + 1):
                        up_coord = neighbor_coords[j][0] + str(int(neighbor_coords[j][1:]) + i)
                        object_uc = self.get_object_from_coord(up_coord)
                        if object_uc != '--':
                            legal_coords.append(up_coord)
                            break
                # Adjacent piece below
                elif j == 3 and piece_adjacent[j] == 1:
                    down_dist = int(neighbor_coords[j][1:]) - 1
                    for i in range(1, down_dist + 1):
                        down_coord = neighbor_coords[j][0] + str(int(neighbor_coords[j][1:]) - i)
                        object_dc = self.get_object_from_coord(down_coord)
                        if object_dc != '--':
                            legal_coords.append(down_coord)
                            break
                j += 1

        # This checks the list for destination coordinates that contain the same
        # color as the current piece and removes them as possible destinations
        # Loops through legal destination spots
        copy_legal_coords = legal_coords.copy()
        for coord in copy_legal_coords:
            coord_object = self.get_object_from_coord(coord)
            # If the coordinate is not empty
            if coord_object != '--':
                # Check the color of the piece at that coordinate. If it matches
                # the color of the piece that is being moved. Remove that coord
                # from the list of legal destinations
                if coord_object.get_color() == piece.get_color():
                    legal_coords.remove(coord)

        return legal_coords

    def print_all_legal_destinations(self):
        """This is used for testing only. It returns all the legal moves for
        the current player before and after removing self check moves"""

        print('Legal destinations for all pieces before and after removing self'
              ' check moves:')
        for row in self.get_board():
            for item in row:
                if item != '--':
                    if item.get_color() == self._turn:
                        l_d = self.legality_check(item)
                        print(item.print_piece(), 'before:', l_d)
                        copy_l_d = l_d.copy()
                        for destination in copy_l_d:
                            destination_index = self.get_index_from_coord(
                                destination)
                            destination_item = self.get_object_from_coord(
                                destination)
                            item_coord = item.get_coordinate()
                            item_index = self.get_index_from_coord(item_coord)

                            item.update_coordinate(destination)
                            self._board[destination_index[0]][
                                destination_index[1]] = item
                            self._board[item_index[0]][item_index[1]] = '--'

                            is_check = self.check_for_check()
                            if is_check is True:
                                l_d.remove(destination)

                            self._board[item_index[0]][item_index[1]] = item
                            self._board[destination_index[0]][
                                destination_index[1]] = destination_item
                            item.update_coordinate(item_coord)

                        print(item.print_piece(), ' after:', l_d)
                        print('-----------------------------------------------')

    def print_all_piece_coordinates(self):
        """This is used for testing, it prints all the coordinates of the
        pieces on the board"""
        print("Here are the coordinates of the current player's pieces:")
        for row in self._board:
            for item in row:
                if item != '--':
                    if self._turn == item.get_color():
                        print(item.get_coordinate())
        print("Here are the coordinates of the enemy's pieces:")
        for row in self._board:
            for item in row:
                if item != '--':
                    if self._turn != item.get_color():
                        print(item.get_coordinate())


class Piece:
    """
    Every piece will inherit from Piece and have a get_color and print_piece
    method. Each piece will be defined a string of two characters, the first
    defines color and the second defines the piece type
    """

    def get_color(self):
        """Prints the color of the piece"""
        return self._color_name[0]

    def print_piece(self):
        """Used for displaying the piece on the board"""
        return self._color_name

    def get_coordinate(self):
        """Returns the coordinate of the piece"""
        return self._coordinate

    def update_coordinate(self, coord):
        """Updates the coordinate of the piece"""
        self._coordinate = coord


class redGeneral(Piece):
    def __init__(self):
        """Name of red general piece is rG, inherits from Piece so contains
        methods for getting the color and printing the piece. This piece has
        a move legality check method."""
        self._color_name = 'rG'
        self._coordinate = 'e1'


class blackGeneral(Piece):
    def __init__(self):
        """Name of red general piece is rG, inherits from Piece so contains
        methods for getting the color and printing the piece. This piece has
        a move legality check method."""
        self._color_name = 'bG'
        self._coordinate = 'e10'


class redAdvisor(Piece):
    def __init__(self, coordinate):
        """Initializes name to rA. Represents red advisor piece"""
        self._color_name = 'rA'
        self._coordinate = coordinate


class blackAdvisor(Piece):
    def __init__(self, coordinate):
        """Initializes name to bA. Represents black advisor piece"""
        self._color_name = 'bA'
        self._coordinate = coordinate


class redSoldier(Piece):
    def __init__(self, coordinate):
        """Initializes name to rS. Represents red soldier piece"""
        self._color_name = 'rS'
        self._coordinate = coordinate


class blackSoldier(Piece):
    def __init__(self, coordinate):
        """Initializes name to bS. Represents black soldier piece"""
        self._color_name = 'bS'
        self._coordinate = coordinate


class redHorse(Piece):
    def __init__(self, coordinate):
        """Represents red horse piece"""
        self._color_name = 'rH'
        self._coordinate = coordinate


class blackHorse(Piece):
    def __init__(self, coordinate):
        """Represents black horse piece"""
        self._color_name = 'bH'
        self._coordinate = coordinate


class redElephant(Piece):
    def __init__(self, coordinate):
        """Represents red elephant piece"""
        self._color_name = 'rE'
        self._coordinate = coordinate


class blackElephant(Piece):
    def __init__(self, coordinate):
        """Represents black elephant piece"""
        self._color_name = 'bE'
        self._coordinate = coordinate


class redCannon(Piece):
    def __init__(self, coordinate):
        """Represents red cannon piece"""
        self._color_name = 'rC'
        self._coordinate = coordinate


class blackCannon(Piece):
    def __init__(self, coordinate):
        """Represents black cannon piece"""
        self._color_name = 'bC'
        self._coordinate = coordinate


class redRook(Piece):
    def __init__(self, coordinate):
        """Represents red rook/chariot piece"""
        self._color_name = 'rR'
        self._coordinate = coordinate


class blackRook(Piece):
    def __init__(self, coordinate):
        """Represents black rook/chariot piece"""
        self._color_name = 'bR'
        self._coordinate = coordinate
