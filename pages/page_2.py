import streamlit as st
import streamlit.components.v1 as components

# Use the full width of the page
st.set_page_config(layout="wide")

def render_hacker_simulation():
    hacker_html = """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <title>Hacker Simulation Terminal</title>
        <style>
          html, body {
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            background: radial-gradient(circle, #000, #06111c);
            font-family: 'Courier New', monospace;
            overflow: hidden;
          }
          .terminal {
            margin: 20px auto;
            width: 90%;
            height: 80vh;
            background-color: rgba(0,0,0,0.85);
            padding: 20px;
            border-radius: 10px;
            overflow-y: auto;
            box-shadow: 0 0 20px #00FF00;
          }
          .command-line {
            margin: 5px 0;
            white-space: pre-wrap;
          }
          .command {
            font-weight: bold;
            color: #00FF00; /* Luminous green for commands */
            text-shadow: 0 0 5px #00FF00;
          }
          .output {
            margin-left: 20px;
            white-space: pre-wrap;
            color: #FFA500; /* Neon orange for outputs */
            text-shadow: 0 0 5px #39FF14;
          }
          .btn {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            background-color: #00FF00;
            border: none;
            border-radius: 5px;
            font-size: 1rem;
            color: #000;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0,0,0,0.4);
          }
          .btn:hover {
            background-color: #90EE90;
          }
        </style>
      </head>
      <body>
        <div class="terminal" id="terminal">
          <!-- Terminal content will be injected here -->
        </div>
        <button class="btn" id="runCommands">Run Simulation</button>
        <script>
          document.getElementById("runCommands").addEventListener("click", function(){
              var terminal = document.getElementById("terminal");
              terminal.innerHTML = "";  // Clear previous output

              var commands = [
                {
                  cmd: "echo 'Initializing system scan...'",
                  output: "[OK] System scan initialized."
                },
                {
                  cmd: "nmap -v localhost",
                  output: "Starting Nmap 7.80 ( https://nmap.org )\\nNmap scan report for localhost (127.0.0.1)\\nHost is up (0.00012s latency).\\nNot shown: 995 closed ports\\nPORT     STATE SERVICE\\n22/tcp   open  ssh\\n80/tcp   open  http\\n443/tcp  open  https"
                },
                {
                  cmd: "ping -c 3 8.8.8.8",
                  output: "PING 8.8.8.8 (8.8.8.8): 56 data bytes\\n64 bytes from 8.8.8.8: icmp_seq=0 ttl=115 time=14.2 ms\\n64 bytes from 8.8.8.8: icmp_seq=1 ttl=115 time=13.9 ms\\n64 bytes from 8.8.8.8: icmp_seq=2 ttl=115 time=13.7 ms\\n\\n--- 8.8.8.8 ping statistics ---\\n3 packets transmitted, 3 received, 0% packet loss, time 2003ms"
                },
                {
                  cmd: "ifconfig",
                  output: "eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\\n    inet 192.168.1.101  netmask 255.255.255.0  broadcast 192.168.1.255\\n    inet6 fe80::f816:3eff:fe20:57c4  prefixlen 64  scopeid 0x20<link>\\n    ether fa:16:3e:20:57:c4  txqueuelen 1000  (Ethernet)"
                },
                {
                  cmd: "cat /var/log/syslog | grep error",
                  output: "Jun 12 22:30:01 localhost kernel: [0.000000] ACPI: Error: [ECR1] Method parse/execution failed\\nJun 12 22:30:05 localhost systemd[1]: Failed to start LSB: AppArmor initialization."
                }
              ];

              var i = 0;
              function runNext() {
                 if (i < commands.length) {
                    // Create and display the command line
                    var cmdLine = document.createElement('div');
                    cmdLine.classList.add('command-line');
                    cmdLine.innerHTML = `<span class="command">> ${commands[i].cmd}</span>`;
                    terminal.appendChild(cmdLine);
                    
                    // Wait before showing output
                    setTimeout(function(){
                        var outLine = document.createElement('pre');
                        outLine.classList.add('output');
                        outLine.textContent = commands[i].output;
                        terminal.appendChild(outLine);
                        terminal.scrollTop = terminal.scrollHeight;
                        i++;
                        runNext();
                    }, 1500);
                 } else {
                    var doneLine = document.createElement('div');
                    doneLine.classList.add('command-line');
                    doneLine.innerHTML = "<span class='command'>[Simulation Complete]</span>";
                    terminal.appendChild(doneLine);
                    document.getElementById("runCommands").disabled = false;
                 }
              }
              document.getElementById("runCommands").disabled = true;
              runNext();
          });
        </script>
      </body>
    </html>
    """
    # Inject the HTML into the Streamlit app.
    components.html(hacker_html, height=800, width=0)

if __name__ == "__main__":
    render_hacker_simulation()
