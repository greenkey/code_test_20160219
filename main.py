from random import uniform as rnd
from math import sqrt, sin, cos


class SoccerPlayer(object):
    def __init__(self, name, step=1):
        self.name = name.__str__()
        self.step = step
        self.x = None
        self.y = None
        self.willing_to_play = rnd(1, 10)

    def __str__(self):
        if not self.is_placed():
            return 'Player {} (None)'.format(self.name)
        return 'Player {} ({:.2f},{:.2f})'.format(self.name, self.x, self.y)

    def get_position(self):
        '''
        :return: the position of the player: (x,y)
        '''
        return (self.x, self.y)

    def is_placed(self):
        '''
        :return: True if the player is inside the board (has a position != None)
        '''
        return self.x is not None and self.y is not None

    def place(self, x, y):
        ''' Place the player at the position specified
        :param x: x coordinate
        :param y: y coordinate
        :return: None
        '''
        self.x = x
        self.y = y

    def move(self, board_size):
        ''' Let the player make a move
        :param board_size: the size of the board (x,y)
        :return: the new position or none
        If the player is on the board, he goes random in one direction, then returns the new position.
        If the player is not on the board, check his willingness to play and then propose a new position.
        In the latter case, the player do not change his position.
        '''
        if self.is_placed():
            while True:
                direction = rnd(0, 360)
                (new_x, new_y) = self.get_position()
                new_x += sin(direction) * self.step
                new_y += cos(direction) * self.step
                if new_x < 0 or new_x > board_size[0] - 1 \
                        or new_y < 0 or new_y > board_size[1] - 1:
                    # if the coordinates are outside the board size, retry
                    continue
                else:
                    self.place(new_x, new_y)
                    return self.get_position()
        else:
            # if the player is outside the board
            # returns the new random coordinates if the player want to play
            if rnd(1, 10) < self.willing_to_play:
                return rnd(0, board_size[0] - 1), rnd(0, board_size[1] - 1)


class SoccerGame(object):
    def __init__(self, size_x=100, size_y=100, players=10, safety_distance=2):
        '''
        :param size_x: one of the sizes of the board
        :param size_y: one of the sizes of the board
        :param players: the number of players
        '''
        self.board_size = (size_x, size_y)
        self.turn_number = 0
        self.safety_distance = safety_distance
        self.players = list()
        for i in range(players):
            self.players.append({
                'player': SoccerPlayer(i),
                'yellow_cards': 0,
                'red_cards': 0,
                'exit_turn': None
            })

    def __str__(self):
        board = [['·' for y in range(self.board_size[1])] for x in range(self.board_size[0])]
        for p in self.players:
            if p['player'].is_placed():
                (px, py) = p['player'].get_position()
                board[round(px)][round(py)] = p['player'].name
        return '\n'.join([''.join(r) for r in board])

    def get_players(self):
        '''
        :return: the players in the match (objects of type SoccerPlayer)
        '''
        for player in self.players:
            yield player['player']

    def run_turn(self):
        ''' The method asks every player to make the move, then check if they are to be penalized
        :return: the turn number
        '''
        future_players = self.players[:]
        for p in future_players:
            new_pos = p['player'].move(self.board_size)
            if p['player'].is_placed():
                (new_x, new_y) = new_pos
                if self.count_players_near(new_x, new_y) > 1:
                    p['yellow_cards'] += 1
                    if p['yellow_cards'] == 2:
                        p['yellow_cards'] = 0
                        p['red_cards'] += 1
                        p['player'].place(None, None)
                        p['exit_turn'] = self.turn_number
            else:
                if new_pos is not None \
                        and p['red_cards'] <= 1 \
                        and self.turn_number >= p['exit_turn'] + 10:
                    p['player'].place(new_pos[0], new_pos[1])

        self.players = future_players
        self.turn_number += 1
        return self.turn_number

    def get_winner(self):
        '''
        :return: the winner player if there is one
        '''
        players_on_race = list(filter(lambda p: p['red_cards'] <= 1, self.players))
        if len(players_on_race) == 1:
            return players_on_race[0]['player']

    def place_player_randomly(self, player, keep_distance=True):
        '''
        :param player: the player to be placed on board (object of type SoccerPlayer)
        :param keep_distance: weather or not keep the safety distance between players, default True
        :return: the new position
        '''
        if player.x is not None:
            raise Exception('The player is already in the board')

        while True:
            x = rnd(0, self.board_size[0] - 1)
            y = rnd(0, self.board_size[1] - 1)
            if keep_distance and self.count_players_near(x, y) > 0:
                continue
            else:
                break
        player.place(x, y)
        return (x, y)

    def count_players_near(self, x, y):
        '''
        :param x: x position on the board
        :param y: y position on the board
        :return: the number of players is in a range of 2 meters near the given position
        '''
        count = 0
        for p in self.players:
            if p['player'].is_placed():
                (px, py) = p['player'].get_position()
                distance = sqrt(pow(px - x, 2) + pow(py - y, 2))
                if distance <= self.safety_distance:
                    count += 1
        return count


if __name__ == '__main__':

    # init the game
    g = SoccerGame(100, 100)

    # place the player randomly
    for p in g.get_players():
        g.place_player_randomly(p)

    # print the board
    print(g)

    while True:

        g.run_turn()

        winner = g.get_winner()
        if winner is None:
            print(g.turn_number)
            continue
        else:
            print("The winner is {} ({} turns)".format(winner, g.turn_number))
            break
