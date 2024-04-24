# Configure path and venv
cd ../../../
source venv/bin/activate

# Install Package
pip install -e .
cd examples/ || exit

# Configure Prompt Style
CYAN='\[\e[36m\]'
YELLOW='\[\e[33m\]'
BOLD='\[\e[1m\]'
RESET='\[\e[0m\]'

export PS1="${CYAN}${BOLD}user@itsprompt ${YELLOW}${BOLD}> ${RESET}"

# Clear the terminal
clear
