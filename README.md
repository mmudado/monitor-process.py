# monitor-process.py

This script is intended to check if a given process is running by using pgrep to retrieve its PID from process name.
If the PID is absent, it runs a script provided by the user to start the process again. 

## Purpose of the script

If you have a process intended to be run 24/7, and it may die out of a sudden, one might want to monitor this process and 
run it again whenever it dies - **and you don't want or cannot use Linux's Systemd**, which would be a better option in this case.

Example: cardano-node is a software run in a Cardano producer node or relay node, part of a stake pool operation. Although cardano-node is stable enough, it may die out of a sudden
leaving that relay or block producer node not working.

## How it works

This script should be run in linux's cron, every 1 min (this it the max. granularity cron provides). It checks for the process's PID, and if it is absent,
 it runs a script provided by the user. E.g: "script.sh" is a common script used to run "cardano-node" in a relay node, provided as follows:

    /usr/bin/nice -19 cardano-node run \
    --topology files/mainnet-topology.json \
    --database-path db \
    --socket-path db/node.socket \
    --config files/mainnet-config.json \
    --host-addr 0.0.0.0 \
    --port 3000
*Example of script.sh provided by the user*

## Before you begin

One might want to wrap the "script.sh" that runs the process in a background terminal, such as screen or tmux. Tmux's example is provided:

Just create a script like the following and rename it as "run-script-background.sh". It will run the "script.sh" into a tmux's terminal, either 
it already exists or not:

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
*Example of run-script-background.sh*

Make sure the scripts are runnable by typing:

    chmod +x script.sh
    chmod +x run-script-background.sh

To check if it is working, just type in a terminal after one minute:

    tmux -a

## Installation

Just put the following line in cron as follows (using as example "cardano-node" for a given process):

Type:

    crontab -e

Insert the line to run monitor-process.py every 1 minute:

    */1 * * * * /usr/bin/python3 monitor-process.py -s run-script-background.sh -p cardano-node -v >> monitor.log 2>&1

Make sure you you have "python3" installed in default paths (script was written in a Ubuntu OS).
Python3 should reside in: "/usr/bin/python3".

 **Verify that the variables point to the correct location of these programs in your OS. Change the paths if needed in the "monitor-process.py" script, lines 27 and 28**:
 
    BASH = "/bin/bash"
    PGREP =  "/usr/bin/pgrep"

## NOTE:

 If you liked it, consider delegating your ADA to [BioStakingPool - BIO](https://biostakingpool.hopto.org) - this is Darwin's Stake Pool ;-)

 Or if you prefer, donate lovelaces to:  
    
    addr1q8dcts6dqy4x28kazkt6snqkskpf7wl0awa9m3xqzv3nnyxg66dcjy55dyrnplgszvzfj6gv3unjk0n3w4qhvvka2ufqmj9nt0

## LICENSE

monitor-process.py is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Additional permission under GNU GPL version 3 section 7

If you modify this Program, or any covered work, by linking or combining
it with Chado (or a modified version of that library), containing parts
covered by the terms of Artistic License 2.0, the licensors of this Program
grant you additional permission to convey the resulting work. {Corresponding
Source for a non-source form of such a combination shall include the source
code for the parts of Chado used as well as that of the covered work.}

See LICENSE.txt for complete gpl-3.0 license.

