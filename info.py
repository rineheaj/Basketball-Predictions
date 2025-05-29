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


def show_system_info_modal():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    total_mem_mb = memory.total // (1024 ** 2)
    used_mem_mb = memory.used // (1024 ** 2)
    
    html_content = f"""
    <html>
      <head>
        <style>
          /* The Modal (background) */
          .modal {{
            display: block; /* Show the modal */
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
          }}

          /* Modal Content/Box */
          .modal-content {{
            background-color: #fefefe;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 40%;
            border-radius: 10px;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
          }}

          /* The Close Button */
          .close {{
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
          }}

          .close:hover,
          .close:focus {{
            color: black;
            text-decoration: none;
          }}
        </style>
        <script>
          function closeModal() {{
            document.getElementById("modalOverlay").style.display = "none";
          }}
        </script>
      </head>
      <body>
        <div id="modalOverlay" class="modal">
          <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2>System Information</h2>
            <p><strong>CPU Usage:</strong> {cpu_percent}%</p>
            <p><strong>Memory Usage:</strong> {memory.percent}%</p>
            <p><strong>Total Memory:</strong> {total_mem_mb:,} MB</p>
            <p><strong>Used Memory:</strong> {used_mem_mb:,} MB</p>
          </div>
        </div>
      </body>
    </html>
    """
    components.html(html_content, height=400)