import streamlit as st
import re

st.set_page_config(page_title="Interactive Terminal Simulator Game", layout="wide")

# Initialize session state for terminal log and game stage
if 'terminal_log' not in st.session_state:
    st.session_state.terminal_log = [
        "Welcome to the Hacker Sim Terminal Game.",
        "Your mission: Use scanning and enumeration commands to infiltrate the target system.",
        "Step 1: Scan the target by using the command: nmap 192.168.1.10"
    ]
if 'game_stage' not in st.session_state:
    st.session_state.game_stage = 0

ALLOWED_IP = "192.168.1.10"

def process_command(cmd):
    args = cmd.strip().split()
    if not args:
        return ""
    
    command = args[0].lower()
    game_stage = st.session_state.game_stage

    # Common help command (always available)
    if command == "help":
        return (
            "Available commands:\n"
            "  help                         - Show this help message.\n"
            "  nmap <target_IP>             - Scan the target for open ports (simulated).\n"
            "  connect <target_IP> <port>     - Attempt to connect to a specific port (simulated).\n"
            "  netstat                      - Show active connections (simulated).\n"
            "  clear                        - Clear the terminal output."
        )
    elif command == "clear":
        st.session_state.terminal_log = []
        return ""

    # Stage 0: Expect the nmap command to scan the target
    elif command == "nmap":
        if len(args) != 2:
            return "Usage: nmap <target_IP>"
        target = args[1]
        ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if not ip_pattern.match(target):
            return f"Invalid IP address: {target}"
        if target != ALLOWED_IP:
            return f"Host {target} is down or not responding. Unable to scan."
        # Only update game stage if currently at stage 0.
        response = (
            f"Starting Nmap 7.80 ( https://nmap.org ) at 2025-06-12 22:00 CDT\n"
            f"Nmap scan report for {target}\n"
            f"Host is up (0.0010s latency).\n"
            f"Not shown: 997 closed ports\n"
            f"PORT     STATE SERVICE\n"
            f"22/tcp   open  ssh\n"
            f"80/tcp   open  http\n"
            f"443/tcp  open  https\n"
            f"MAC Address: AA:BB:CC:DD:EE:FF (Vendor)"
        )
        if game_stage == 0:
            st.session_state.game_stage = 1
            response += (
                "\n\n[SCAN COMPLETE]\n"
                "Scanning is the first step in understanding the target. "
                "Now, use the command 'connect 192.168.1.10 22' to try connecting via SSH."
            )
        return response

    # Stage 1: Expect the connect command on port 22.
    elif command == "connect":
        if len(args) != 3:
            return "Usage: connect <target_IP> <port>"
        target = args[1]
        port = args[2]
        if target != ALLOWED_IP:
            return f"Unable to connect: host {target} is not available."
        if port != "22":
            return f"Port {port} is not available for connection. Try port 22."
        response = (
            f"Attempting to connect to {target} on port {port}...\n"
            f"Connection to {target}:{port} established successfully!"
        )
        if game_stage == 1:
            st.session_state.game_stage = 2
            response += (
                "\n\n[CONNECTION ESTABLISHED]\n"
                "Connecting to the target confirms a weak or unprotected entry point. "
                "Now, check the connection status with the 'netstat' command."
            )
        return response

    # Stage 2: Expect the netstat command to confirm the active connection.
    elif command == "netstat":
        response = (
            "Proto Recv-Q Send-Q Local Address           Foreign Address         State\n"
            "tcp        0      0 192.168.1.10:22         192.168.1.50:52344      ESTABLISHED\n"
            "tcp        0      0 192.168.1.10:80         192.168.1.60:34567      TIME_WAIT"
        )
        if game_stage == 2:
            st.session_state.game_stage = 3
            response += (
                "\n\n[ENUMERATION COMPLETE]\n"
                "Port enumeration reveals the active connections and services. "
                "You have successfully completed the scanning and enumeration phase!"
                "\n\n" +
                r"""
       _____                           _     _ _           
      / ____|                         | |   (_) |          
     | |     ___  _ ____   _____ _ __ | |__  _| |_ ___ _ __ 
     | |    / _ \| '_ \ \ / / _ \ '_ \| '_ \| | __/ _ \ '__|
     | |___| (_) | | | \ V /  __/ | | | | | | | ||  __/ |   
      \_____\___/|_| |_|\_/ \___|_| |_|_| |_|_|\__\___|_|   
                                                           
    """
            )
        return response

    # Allow the user to run netstat even if not at the right game stage.
    else:
        return f"Unknown command or try a different command: {cmd}"

def add_command_to_log(command, output):
    st.session_state.terminal_log.append(f"> {command}")
    if output:
        st.session_state.terminal_log.append(output)

st.markdown(
    """
    <style>
      body {
          background: linear-gradient(135deg, #000000, #006400);
          font-family: 'Courier New', Courier, monospace;
          color: #00FF00;
      }
      .terminal-area {
          background: #000;
          padding: 20px;
          border: 2px solid #00FF00;
          height: 70vh;
          overflow-y: auto;
          white-space: pre-wrap;
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

st.title("Interactive Terminal Simulator Game")

terminal_container = st.empty()

with st.form(key="cmd_form", clear_on_submit=True):
    command = st.text_input(
        "Enter command", 
        placeholder="Type your command here...",
        key="command_input", 
        help="For example: help, nmap 192.168.1.10, connect 192.168.1.10 22, netstat"
    )
    submitted = st.form_submit_button("Execute")

if submitted and command:
    output = process_command(command)
    add_command_to_log(command, output)

terminal_output = "\n".join(st.session_state.terminal_log)
terminal_container.markdown(f"<div class='terminal-area'>{terminal_output}</div>", unsafe_allow_html=True)