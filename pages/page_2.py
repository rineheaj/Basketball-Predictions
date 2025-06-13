import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")  # Make the app use full screen width

def render_crazy_test_page():
    crazy_html = """
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
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
          }
          .crazy-box {
            width: 50vw;
            height: 30vh;
            background: linear-gradient(135deg, #000000, #006400);
            border: 2px dashed #00FF00;
            border-radius: 10px;
            margin: 0 auto;
            padding: 20px;
            box-shadow: 0 0 20px #00FF00;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
          }
          .crazy-text {
            font-size: 1.5vw;
            font-weight: bold;
            animation: flicker 1.5s infinite alternate;
          }
          @keyframes flicker {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
          }
          .crazy-btn {
            margin-top: 40px;
            padding: 10px 20px;
            font-size: 1.5vw;
            border: none;
            background-color: #00FF00;
            color: #000000;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
          }
          .crazy-btn:hover {
            background-color: #90EE90;
          }
        </style>
      </head>
      <body>
        <div class="crazy-box" id="crazyBox">
          <div class="crazy-text" id="crazyText">Hacker mode inactive.</div>
        </div>
        <button class="crazy-btn" id="crazyBtn">Activate Hacker Mode</button>
        <script>
          document.getElementById("crazyBtn").addEventListener("click", function(){
            var messages = [
              "Accessing mainframe...",
              "Bypassing firewall...",
              "Decrypting data streams...",
              "Injecting code...",
              "Compiling virus payload...",
              "Overriding security protocols...",
              "Hacker mode active!",
              "System breach complete."
            ];
            var count = 0;
            var box = document.getElementById("crazyText");
            var button = document.getElementById("crazyBtn");
            button.disabled = true;
            
            function updateMessage() {
              var randomIndex = Math.floor(Math.random() * messages.length);
              box.innerHTML = messages[randomIndex];
              count++;
              if(count < 8) {
                setTimeout(updateMessage, 700);
              } else {
                box.innerHTML = "Hacker mode deactivated.";
                button.disabled = false;
              }
            }
            updateMessage();
          });
        </script>
      </body>
    </html>
    """
    components.html(crazy_html, height=800, width=0)
    
if __name__ == "__main__":
    render_crazy_test_page()
