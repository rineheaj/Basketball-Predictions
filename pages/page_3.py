import streamlit as st
import streamlit.components.v1 as components

def render_crazy_test_page():
    crazy_html = """
    <html>
      <head>
        <style>
          body {
            background: radial-gradient(circle, #ff6b6b, #f06595);
            font-family: 'Courier New', Courier, monospace;
            color: white;
            text-align: center;
            padding-top: 50px;
          }
          .crazy-box {
            width: 150px;
            height: 150px;
            background: linear-gradient(45deg, #fab1a0, #ff7675);
            animation: spin 3s linear infinite, pulse 2s ease-in-out infinite;
            border-radius: 20px;
            margin: 0 auto;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
          }
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
          @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
          }
          .crazy-text {
            margin-top: 30px;
            font-size: 24px;
            font-weight: bold;
            animation: colorchange 4s infinite;
          }
          @keyframes colorchange {
            0% { color: #ffeaa7; }
            25% { color: #fd79a8; }
            50% { color: #74b9ff; }
            75% { color: #55efc4; }
            100% { color: #ffeaa7; }
          }
          .crazy-btn {
            margin-top: 40px;
            padding: 10px 20px;
            font-size: 18px;
            border: none;
            background-color: #00b894;
            color: white;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
          }
          .crazy-btn:hover {
            background-color: #019875;
          }
        </style>
      </head>
      <body>
        <div class="crazy-box"></div>
        <div class="crazy-text">Welcome to the Crazy Test Page!</div>
        <button class="crazy-btn" id="crazyBtn">Click Me!</button>
        <script>
          document.getElementById("crazyBtn").addEventListener("click", function(){
            let count = 0;
            const button = this;
            button.disabled = true; // Disable the button during the alert cycle

            function crazyAlert() {
              count++;
              if (count <= 3) {
                alert("You clicked " + count + " time" + (count > 1 ? "s" : "") + "! Stay crazy!");
                setTimeout(crazyAlert, 500);
              } else {
                alert("Enough crazy clicks!");
                button.disabled = false; // Re-enable the button after finishing
              }
            }
            crazyAlert();
          });
        </script>
      </body>
    </html>
    """
    components.html(crazy_html, height=500)

if __name__ == "__main__":
    render_crazy_test_page()
