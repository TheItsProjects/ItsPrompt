# --- Set Up --------------------------
# Load Config
Source ./configuration/base_config.tape
Source ./configuration/small_window_config.tape

# --- Main ----------------------------
# run example.py
Type@0.1s "python3 demos/input_demo.py" Enter Sleep 1s

Screenshot ../../source/media/input.png

Sleep 1s

Ctrl+C
