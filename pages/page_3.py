import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

def render_interactive_hacker_page():
    html_code = """
    <html>
      <head>
        <style>
          html, body {
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
          }
          body {
            background: linear-gradient(135deg, #000000, #006400);
            font-family: 'Courier New', Courier, monospace;
            color: #00FF00;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
          }
          #terminal {
            width: 80vw;
            height: 60vh;
            background: #000;
            border: 2px solid #00FF00;
            padding: 10px;
            overflow-y: auto;
            font-size: 1.2rem;
          }
          #commandInput {
            width: 80vw;
            padding: 10px;
            margin-top: 10px;
            font-size: 1.2rem;
            background: #222;
            color: #00FF00;
            border: 1px solid #00FF00;
          }
          #sendBtn {
            padding: 10px 20px;
            margin-top: 10px;
            background: #00FF00;
            color: #000;
            border: none;
            font-size: 1.2rem;
            border-radius: 5px;
            cursor: pointer;
          }
          #sendBtn:hover {
            background: #90EE90;
          }
        </style>
      </head>
      <body>
        <div id="terminal">Welcome, hacker. Type a command below...</div>
        <input type="text" id="commandInput" placeholder="Enter command..." autofocus />
        <button id="sendBtn">Send Command</button>
        <script>
          const terminal = document.getElementById("terminal");
          const commandInput = document.getElementById("commandInput");
          const sendBtn = document.getElementById("sendBtn");

          const commands = {
            "help": "Available commands: help, scan, breach, shutdown.",
            "scan": "Scanning network... Found open ports: 22, 80, 443.",
            "breach": "Security breach initiated. Access granted.",
            "shutdown": "Shutting down target system..."
          };

          function appendToTerminal(text) {
            terminal.innerHTML += "<br>" + text;
            terminal.scrollTop = terminal.scrollHeight;
          }

          sendBtn.addEventListener("click", function() {
            var inputText = commandInput.value.trim().toLowerCase();
            if (inputText) {
              appendToTerminal("> " + inputText);
              if (commands[inputText]) {
                appendToTerminal(commands[inputText]);
              } else {
                appendToTerminal("Unknown command: " + inputText);
              }
              commandInput.value = "";
            }
          });

          commandInput.addEventListener("keypress", function(e) {
            if (e.key === "Enter") {
              sendBtn.click();
            }
          });
        </script>
      </body>
    </html>
    """
    components.html(html_code, width=0, height=700)

if __name__ == '__main__':
    render_interactive_hacker_page()