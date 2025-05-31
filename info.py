import streamlit as st
import streamlit.components.v1 as components
import psutil

def show_system_info():
    
    st.write("## System Information")
    
    
    cpu_percent = psutil.cpu_percent(interval=1)
    
    memory = psutil.virtual_memory()
    
    total_mem_mb = memory.total // (1024**2)
    used_mem_mb = memory.used // (1024**2)
    
    st.write(f"**CPU Usage:** {cpu_percent}%")
    st.write(f"**Memory Usage:** {memory.percent}%")
    st.write(f"**Total Memory:** {total_mem_mb:,} MB")
    st.write(f"**Used Memory:** {used_mem_mb:,} MB")


import streamlit as st
import streamlit.components.v1 as components
import psutil

def show_system_info_modal():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    total_mem_mb = memory.total // (1024 ** 2)
    used_mem_mb = memory.used // (1024 ** 2)

    html_content = f"""
    <html>
      <head>
        <style>
          @keyframes fadeIn {{
              from {{ opacity: 0; }}
              to {{ opacity: 1; }}
          }}

          @keyframes popUp {{
              from {{ transform: scale(0.9); }}
              to {{ transform: scale(1); }}
          }}

          @keyframes neonGlow {{
              0% {{ text-shadow: 0 0 5px #ff00ff, 0 0 10px #ff00ff, 0 0 15px #ff00ff; }}
              50% {{ text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff; }}
              100% {{ text-shadow: 0 0 5px #ff00ff, 0 0 10px #ff00ff, 0 0 15px #ff00ff; }}
          }}

          @keyframes lavaFlow {{
              0% {{ background: linear-gradient(45deg, red, orange, yellow); }}
              50% {{ background: linear-gradient(45deg, yellow, orange, red); }}
              100% {{ background: linear-gradient(45deg, red, orange, yellow); }}
          }}

          /* Lava Scrollbar */
          ::-webkit-scrollbar {{
              width: 12px;
          }}

          ::-webkit-scrollbar-track {{
              background: black;
          }}

          ::-webkit-scrollbar-thumb {{
              background: linear-gradient(45deg, red, orange, yellow);
              border-radius: 6px;
              animation: lavaFlow 3s infinite linear;
          }}

          /* Modal Styling */
          .modal {{
            display: block;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: auto;
            height: auto;
            overflow: auto;
            background-color: rgba(0,0,0,0.9);
            animation: fadeIn 0.5s ease-in-out;
          }}

          /* Modal Content */
          .modal-content {{
            background-color: black;
            color: white;
            margin: 10% auto;
            padding: 15px;
            border: 1px solid #555;
            width: auto;
            max-width: 40%;
            border-radius: 10px;
            box-shadow: 0 4px 8px 0 rgba(255,255,255,0.2);
            animation: popUp 0.5s ease-in-out;
          }}

          /* Close Button */
          .close {{
            color: white;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
          }}

          .close:hover,
          .close:focus {{
            color: gray;
            text-decoration: none;
          }}

          /* Neon Glowing Text */
          .neon-text {{
            font-size: 24px;
            font-weight: bold;
            color: white;
            animation: neonGlow 2s infinite alternate;
          }}
        </style>
        <script>
          function showModal() {{
              document.getElementById("modalOverlay").style.display = "block";
          }}

          function closeModal() {{
              document.getElementById("modalOverlay").style.display = "none";
          }}
        </script>
      </head>
      <body>
        <div id="modalOverlay" class="modal">
          <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2 class="neon-text">System Information</h2>
            <p class="neon-text"><strong>CPU Usage:</strong> {cpu_percent}%</p>
            <p class="neon-text"><strong>Memory Usage:</strong> {memory.percent}%</p>
            <p class="neon-text"><strong>Total Memory:</strong> {total_mem_mb:,} MB</p>
            <p class="neon-text"><strong>Used Memory:</strong> {used_mem_mb:,} MB</p>
          </div>
        </div>
      </body>
    </html>
    """
    
    components.html(html_content, height=300)