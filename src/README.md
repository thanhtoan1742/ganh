## Board and game
To use different `move(board, player)` function to play the game,
pass it to the `game` constructor as `first_move_maker` argument or
`second_move_maker` argument.
See the code in `main.py` for example.


## Note
The `random_player_clone.py` and `random_player_for_input_player` is to help
importing same module as different modules to resolve global variable
accessing conflict.
You can ignore this if you make sure each `move` function
is only used for one player.

The `run.sh` file is a bash script to automate cloning `random_layer` to
`random_player_clone` and `random_player_for_input_player` and run `main.py`.
