import streamlit as st
import psutil

def show_system_info():
    """
    Gathers and displays system resource usage information using psutil.
    """
    st.write("## System Information")
    
    # Get CPU usage percentage over a 1-second interval.
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Get virtual memory details.
    memory = psutil.virtual_memory()
    
    # Convert memory totals to MB for easier reading.
    total_mem_mb = memory.total // (1024**2)
    used_mem_mb = memory.used // (1024**2)
    
    st.write(f"**CPU Usage:** {cpu_percent}%")
    st.write(f"**Memory Usage:** {memory.percent}%")
    st.write(f"**Total Memory:** {total_mem_mb:,} MB")
    st.write(f"**Used Memory:** {used_mem_mb:,} MB")
    