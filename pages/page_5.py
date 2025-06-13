import streamlit as st
import re

st.set_page_config(page_title="Interactive Terminal Simulator Game", layout="wide")

# Initialize session state for terminal log and game stage
if 'terminal_log' not in st.session_state:
    st.session_state.terminal_log = [
        "<span class='system-output'>Welcome to the Hacker Sim Terminal Game.</span>",
        "<span class='system-output'>Your mission: Infiltrate the target system using legitimate commands.</span>",
        "<span class='system-output'>Step 1: Scan the target using the command: nmap 192.168.1.10</span>"
    ]
if 'game_stage' not in st.session_state:
    st.session_state.game_stage = 0

# Define our target and expected credentials
ALLOWED_IP = "192.168.1.10"
EXPECTED_SSH_USER = "admin"
EXPECTED_PASSWORD = "letmein"

def process_command(cmd):
    args = cmd.strip().split()
    if not args:
        return ""
    command = args[0].lower()
    game_stage = st.session_state.game_stage

    # Global commands
    if command == "help":
        return (
            "Available commands:\n"
            "  help                         - Show this help message.\n"
            "  clear                        - Clear the terminal output.\n\n"
            "Mission-specific commands:\n"
            "  nmap <target_IP>             - Scan the target for open ports.\n"
            "  ssh <user>@<target_IP>         - Initiate an SSH connection.\n"
            "  password <your_password>     - Authenticate your SSH session."
        )
    elif command == "clear":
        st.session_state.terminal_log = []
        return ""
    
    # Stage 0: Expect a proper Nmap scan
    if game_stage == 0:
        if command == "nmap":
            if len(args) != 2:
                return "Usage: nmap <target_IP>"
            target = args[1]
            ip_pattern = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
            if not ip_pattern.match(target):
                return f"Invalid IP address: {target}"
            if target != ALLOWED_IP:
                return f"Host {target} is down or unresponsive."
            # Successful scan!
            st.session_state.game_stage = 1
            return (
                f"Starting Nmap scan on {target}...\n"
                "Scan results:\n"
                "Host is up. Open ports:\n"
                "22/tcp open  ssh\n"
                "80/tcp open  http\n"
                "\n[SCAN COMPLETE]\n"
                "Scanning is crucial to understand your target.\n"
                "Next, establish an SSH connection using: ssh admin@192.168.1.10"
            )
        else:
            return "Please start by scanning the target: nmap 192.168.1.10"
    
    # Stage 1: Expect SSH command
    if game_stage == 1:
        if command == "ssh":
            if len(args) != 2:
                return "Usage: ssh <user>@<target_IP>"
            ssh_arg = args[1]
            if "@" not in ssh_arg:
                return "Usage: ssh <user>@<target_IP>"
            user, target = ssh_arg.split("@", 1)
            if target != ALLOWED_IP or user != EXPECTED_SSH_USER:
                return "SSH connection failed: Incorrect user or target."
            st.session_state.game_stage = 2
            return (
                f"Attempting SSH connection to {user}@{target}...\n"
                "Connection established.\n"
                "admin@192.168.1.10's password:\n"
                "Authentication is critical for secure access.\n"
                "Enter your password using: password <your_password>"
            )
        else:
            return "Establish an SSH connection with: ssh admin@192.168.1.10"
    
    # Stage 2: Expect the password command
    if game_stage == 2:
        if command == "password":
            if len(args) != 2:
                return "Usage: password <your_password>"
            pw = args[1]
            if pw != EXPECTED_PASSWORD:
                return "Authentication failed: Incorrect password."
            st.session_state.game_stage = 3
            return (
                "Authentication successful!\n"
                "You have gained access to the target system.\n"
                "\nMission Accomplished!\n" +
                r"""
       __  __           _      _                 _ 
      |  \/  |         | |    (_)               | |
      | \  / | ___   __| | ___ _ _ __   __ _  __| |
      | |\/| |/ _ \ / _` |/ _ \ | '_ \ / _` |/ _` |
      | |  | | (_) | (_| |  __/ | | | | (_| | (_| |
      |_|  |_|\___/ \__,_|\___|_|_| |_|\__,_|\__,_|
                                             
                """
            )
        else:
            return "Please authenticate by typing: password <your_password>"
    
    # Game completed
    if game_stage == 3:
        return "Mission already accomplished! Type 'help' for available commands."
    
    return f"Unknown command: {cmd}"

def add_command_to_log(command, output):
    # Wrap user commands in a span with class .user-cmd and output in .system-output
    st.session_state.terminal_log.append(f"<span class='user-cmd'>&gt; {command}</span>")
    if output:
        # Split multiple lines from output and wrap each in system-output
        wrapped_output = "\n".join([f"<span class='system-output'>{line}</span>" for line in output.split('\n')])
        st.session_state.terminal_log.append(wrapped_output)

st.markdown(
    """
    <style>
      body {
          background: linear-gradient(135deg, #000000, #006400);
          font-family: 'Courier New', Courier, monospace;
      }
      .terminal-title {
          color: #1E90FF; /* Dodger Blue for the title */
          text-align: center;
      }
      .terminal-area {
          background: #000;
          padding: 20px;
          border: 2px solid #00FF00;
          height: 70vh;
          overflow-y: auto;
          white-space: pre-wrap;
      }
      .user-cmd {
          color: #FF4500; /* OrangeRed for user commands */
      }
      .system-output {
          color: #00FF00; /* Neon green for system responses */
      }
      .command-input {
          width: 100%;
          padding: 10px;
          font-size: 1.2em;
          background: #222;
          color: #00FF00;
          border: 1px solid #00FF00;
      }
      .submit-button {
          padding: 10px 20px;
          font-size: 1.2em;
          background: #00FF00;
          color: #000;
          border: none;
          cursor: pointer;
          margin-top: 10px;
      }
      .submit-button:hover {
          background: #90EE90;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Instead of using st.title, we use a custom HTML title for color control.
st.markdown("<h1 class='terminal-title'>Interactive Terminal Simulator Game</h1>", unsafe_allow_html=True)

terminal_container = st.empty()

with st.form(key="cmd_form", clear_on_submit=True):
    command = st.text_input(
        "Enter command",
        placeholder="Type your command here...",
        key="command_input",
        help="Examples:\n • nmap 192.168.1.10\n • ssh admin@192.168.1.10\n • password letmein"
    )
    submitted = st.form_submit_button("Execute")

if submitted and command:
    output = process_command(command)
    add_command_to_log(command, output)

# Wrap each log entry in HTML and join with line breaks
terminal_output = "\n".join(st.session_state.terminal_log)
terminal_container.markdown(f"<div class='terminal-area'>{terminal_output}</div>", unsafe_allow_html=True)