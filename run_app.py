import subprocess
import sys
import os
import time

def main():
    print("Starting Enterprise Decision Path Auditor...")
    
    python_exe = sys.executable
    print(f"Using Python executable: {python_exe}")
    
    print("Launching FastAPI Backend on port 8000...")
    backend_process = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    
    # Give the backend a few seconds to start up before launching the frontend
    time.sleep(3)
    
    # Render binds to the $PORT environment variable provided at runtime
    port = os.getenv("PORT", "8501")
    print(f"Launching Streamlit Frontend on port {port}...")
    env = os.environ.copy()
    env["BACKEND_URL"] = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    
    frontend_process = subprocess.Popen(
        [python_exe, "-m", "streamlit", "run", "frontend/Home.py", "--server.port", port, "--server.address", "0.0.0.0"],
        env=env,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    
    try:
        # Keep the main script running while the servers are active
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("Servers stopped successfully.")

if __name__ == "__main__":
    main()
