import streamlit as st
import re

st.set_page_config(page_title="Interactive Terminal Simulator Game", layout="wide")

# Initialize session state for terminal log and game stage
if 'terminal_log' not in st.session_state:
    st.session_state.terminal_log = [
        "<span class='system-output'>Welcome to the Hacker Sim Terminal Game.</span>",
        "<span class='system-output'>Your mission: Infiltrate the target system using legitimate commands.</span>",
        "<span class='system-output'>Step -1: Begin by performing a network ping sweep to discover active hosts.</span>",
        "<span class='system-output'>Hint: Type <code>pingall</code> to start the scan.</span>"
    ]
if 'game_stage' not in st.session_state:
    # Game stages:
    # -1: Ping sweep; 0: nmap scanning; 1: SSH connection; 2: Password authentication; 3: Mission accomplished.
    st.session_state.game_stage = -1

ALLOWED_IP = "192.168.1.10"
EXPECTED_SSH_USER = "admin"
EXPECTED_PASSWORD = "letmein"

def process_command(cmd):
    args = cmd.strip().split()
    if not args:
        return ""
    command = args[0].lower()
    game_stage = st.session_state.game_stage

    # Global command: Display help text
    if command == "help":
        return (
            "=== HELP MENU ===\n"
            "This simulation guides you through the reconnaissance phase. Commands available:\n\n"
            "  help                                - Display this help message.\n"
            "  clear                               - Clear the terminal output.\n\n"
            "Mission-specific commands based on the current step:\n"
            "  pingall                             - Perform a ping sweep of the network.\n"
            "  nmap <target_IP>                    - Scan a target for open ports.\n"
            "  ssh <user>@<target_IP>                - Initiate an SSH connection to the target.\n"
            "  password <your_password>            - Authenticate your SSH session.\n\n"
            "If you're stuck, check which step you are on:\n"
            "   Stage -1: Discover the live host (use pingall).\n"
            "   Stage 0: Scan the target using nmap.\n"
            "   Stage 1: Connect to the target via SSH.\n"
            "   Stage 2: Authenticate your session with a password.\n"
            "   Stage 3: Mission accomplished!\n\n"
            "Example Commands:\n"
            "   pingall\n"
            "   nmap 192.168.1.10\n"
            "   ssh admin@192.168.1.10\n"
            "   password letmein\n"
            "================="
        )
    elif command == "clear":
        st.session_state.terminal_log = []
        return ""
    
    # Stage -1: Ping sweep stage. User must type "pingall"
    if game_stage == -1:
        if command == "pingall":
            st.session_state.game_stage = 0
            return (
                "Performing ping sweep on network 192.168.1.0/24...\n"
                "192.168.1.5 ... No response\n"
                "192.168.1.10 ... Reply received!\n"
                "192.168.1.20 ... No response\n\n"
                "Live host(s) found: 192.168.1.10\n"
                "Ping sweep complete.\n"
                "Tip: Scanning a network with a ping sweep is vital to identify active devices.\n"
                "Next, scan the target using: nmap 192.168.1.10"
            )
        else:
            return "Please perform a network scan by typing: pingall"
    
    # Stage 0: Expect a proper nmap scan
    if game_stage == 0:
        if command == "nmap":
            if len(args) != 2:
                return "Usage: nmap <target_IP>\nTry: nmap 192.168.1.10"
            target = args[1]
            ip_pattern = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
            if not ip_pattern.match(target):
                return f"Invalid IP address: {target}"
            if target != ALLOWED_IP:
                return f"Host {target} is down or unresponsive."
            st.session_state.game_stage = 1
            return (
                f"Starting Nmap scan on {target}...\n"
                "Scan results:\n"
                "Host is up. Open ports:\n"
                "22/tcp open  ssh\n"
                "80/tcp open  http\n\n"
                "[SCAN COMPLETE]\n"
                "Scanning helps reveal vulnerabilities in services running on the target.\n"
                "Next, establish an SSH connection using: ssh admin@192.168.1.10"
            )
        else:
            return "After the ping sweep, scan the live host using: nmap 192.168.1.10"
    
    # Stage 1: Expect SSH command (simulate proper SSH syntax)
    if game_stage == 1:
        if command == "ssh":
            if len(args) != 2:
                return "Usage: ssh <user>@<target_IP>\nExample: ssh admin@192.168.1.10"
            ssh_arg = args[1]
            if "@" not in ssh_arg:
                return "Usage: ssh <user>@<target_IP>\nEnsure you include an '@' between user and IP."
            user, target = ssh_arg.split("@", 1)
            if target != ALLOWED_IP or user != EXPECTED_SSH_USER:
                return "SSH connection failed: Incorrect user or target."
            st.session_state.game_stage = 2
            return (
                f"Attempting SSH connection to {user}@{target}...\n"
                "Connection established.\n"
                "admin@192.168.1.10's password:\n"
                "Authentication is critical for secure access.\n"
                "Next, enter your password using: password <your_password>"
            )
        else:
            return "Establish SSH connection using: ssh admin@192.168.1.10"
    
    # Stage 2: Expect the password command for authentication
    if game_stage == 2:
        if command == "password":
            if len(args) != 2:
                return "Usage: password <your_password>\nExample: password letmein"
            pw = args[1]
            if pw != EXPECTED_PASSWORD:
                return "Authentication failed: Incorrect password."
            st.session_state.game_stage = 3
            return (
                "Authentication successful!\n"
                "You have gained access to the target system.\n\n"
                "Mission Accomplished!\n" +
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
    
    # Stage 3: Mission Accomplished -- game complete
    if game_stage == 3:
        return "Mission already accomplished! Type 'help' if you need instructions."
    
    return f"Unknown command: {cmd}"

def add_command_to_log(command, output):
    st.session_state.terminal_log.append(f"<span class='user-cmd'>&gt; {command}</span>")
    if output:
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
          color: #1E90FF;
          text-align: center;
          margin-bottom: 20px;
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
          color: #FF4500;
      }
      .system-output {
          color: #00FF00;
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

st.markdown("<h1 class='terminal-title'>Interactive Terminal Simulator Game</h1>", unsafe_allow_html=True)

terminal_container = st.empty()

with st.form(key="cmd_form", clear_on_submit=True):
    command = st.text_input(
        "Enter command",
        placeholder="Type your command here...",
        key="command_input",
        help="Examples:\n • pingall\n • nmap 192.168.1.10\n • ssh admin@192.168.1.10\n • password letmein\n\nIf you get stuck, type 'help' for detailed instructions."
    )
    submitted = st.form_submit_button("Execute")

if submitted and command:
    output = process_command(command)
    add_command_to_log(command, output)

terminal_output = "\n".join(st.session_state.terminal_log)
terminal_container.markdown(f"<div class='terminal-area'>{terminal_output}</div>", unsafe_allow_html=True)
