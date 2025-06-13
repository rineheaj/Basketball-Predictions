import streamlit as st

st.set_page_config(page_title="Interactive Terminal Simulator", layout="wide")

if 'terminal_log' not in st.session_state:
    st.session_state.terminal_log = ["Welcome to the Hacker Sim Terminal. Type 'help' for commands."]

def process_command(cmd):
    args = cmd.strip().split()
    if not args:
        return ""
    command = args[0].lower()
    if command == "help":
        return (
            "Available commands:\n"
            "  help                - Show this help message.\n"
            "  netstat             - Show active connections and open ports (simulated).\n"
            "  nmap <target>       - Scan the target for open ports (simulated).\n"
            "  connect <target> <port> - Attempt to connect to a specific port on a target (simulated).\n"
            "  clear               - Clear the terminal output."
        )
    elif command == "clear":
        st.session_state.terminal_log = []
        return ""
    elif command == "netstat":
        return (
            "Proto Recv-Q Send-Q Local Address           Foreign Address         State\n"
            "tcp        0      0 192.168.1.10:22         192.168.1.50:52344      ESTABLISHED\n"
            "tcp        0      0 192.168.1.10:80         192.168.1.60:34567      TIME_WAIT"
        )
    elif command == "nmap":
        if len(args) < 2:
            return "Usage: nmap <target>"
        target = args[1]
        return (
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
    elif command == "connect":
        if len(args) < 3:
            return "Usage: connect <target> <port>"
        target = args[1]
        port = args[2]
        return (
            f"Attempting to connect to {target} on port {port}...\n"
            f"Connection to {target}:{port} established successfully!"
        )
    else:
        return f"Unknown command: {cmd}"

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

st.title("Interactive Terminal Simulator")

terminal_container = st.empty()

with st.form(key="cmd_form", clear_on_submit=True):
    command = st.text_input("Enter command", placeholder="Type your command here...", key="command_input", 
                              help="Example: help, netstat, nmap localhost, connect localhost 22")
    submitted = st.form_submit_button("Execute")

if submitted and command:
    output = process_command(command)
    add_command_to_log(command, output)

terminal_output = "\n".join(st.session_state.terminal_log)
terminal_container.markdown(f"<div class='terminal-area'>{terminal_output}</div>", unsafe_allow_html=True)