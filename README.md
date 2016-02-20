I created this repository just to share the results of a coding test.

# Soccer Game

## Requirements

A playing area is 100m x 100m. A game has a referee and 10 players. A player moves 1m
every second and starts out in a random place on the playing area. A referee gives a yellow
card to a player if that player moves within 2m of another player. It is the player that moves
to within 2m of another player, that gets the yellow card. If a player gets 2 yellow cards, the
player is ejected from the game for 10 seconds. When a player is sent off the player needs to
ask the referee if they are eligible to play again. The referee will let the player return to
playing the first time this happens, but not subsequent times. The last player left playing is
the winner. Write an application that simulates these game requirements. Please document
all assumptions or decisions you’ve made, that helped ensure you delivered a working result
in the time provided.

## Assumptions

* the player moves randomly but stays on the playing area;
* the player don't always ask to come into playing area again, a random "willingness to play" is assigned to decide the urge of the player to play;

## Description

The game is implemented using two Python Classes:

* SoccerGame, it manages the players, the turns, the yellow cards and whether a player can play;
* SoccerPlayer, it has a position and the intelligence to make moves and decide to play agin.

## How to run the game

The script doesn't need any external packages, it's all Python 3 native modules.

If you want to just run the game, do as follows:

```
python3 main.py
```

It will create a game as illustrated in the requirements (100x100, 10 players...) and then run all the turns.
The time in the game is fast as possible, to avoid useless waits.
