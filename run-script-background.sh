#!/bin/bash

session="cardano"
tmux has-session -t $session 2>/dev/null

# session exists
if [ $? == 0 ]; then
  # send command to execute script in session
  tmux send-keys -t 'cardano:node.0' "$HOME/script.sh" Enter
# no session
elif [ $? != 0 ]; then
# create new session and execute script
  tmux new -s "cardano" -n "node" -d
  tmux select-pane -t 'cardano:node.0'
  tmux send-keys -t 'cardano:node.0' "$HOME/script.sh" Enter
fi
