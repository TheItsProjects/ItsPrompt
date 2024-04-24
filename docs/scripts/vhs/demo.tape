# --- Set Up --------------------------
# Load Config
Source ./configuration/base_config.tape
Source ./configuration/big_window_config.tape

# Set Output
Output ../../source/media/ItsPrompt.gif

# --- Main ----------------------------
# run example.py
Type@0.1s "python3 demo.py" Enter Sleep 1s

# Prompt 1
Up
Down 2
Enter
Sleep 1s

# Prompt 2
Up 2
Enter
Sleep 1s

# Prompt 3
Space
Enter
Down
Space
Enter
Sleep 1s

# Prompt 4
Type "h"
Type "m"
Enter
Sleep 1s

# Prompt 5
Type@0.1s "test" Enter
Sleep 1s

# Prompt 6
Type@0.1s "ItsNameless" Enter
Sleep 1s

# Prompt 7
Type@0.1s "Main"
Tab
Enter
Sleep 1s

# Prompt 8
Type@0.1s "1234" Enter
Sleep 1s

# Prompt 9
Type "y"
Sleep 1s

# Prompt 10
Right
Down
Backspace
Type "1" Enter
Sleep 1s

# Exit
Hide
Ctrl+C
Show
