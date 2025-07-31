import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
import webbrowser
import subprocess
import sys
import os
from pathlib import Path
import uvicorn
import time

class FinanceAgentTray:
    def __init__(self):
        self.icon = None
        self.server_process = None
        self.server_thread = None
        self.running = False
        
    def create_image(self):
        width = 64
        height = 64
        
        image = Image.new('RGB', (width, height), (0, 128, 0))
        dc = ImageDraw.Draw(image)
        
        dc.rectangle(
            [(width // 4, height // 4), (3 * width // 4, 3 * height // 4)],
            fill=(255, 255, 255)
        )
        
        dc.text((width // 2 - 5, height // 2 - 5), "$", fill=(0, 128, 0))
        
        return image

    def start_backend_server(self):
        try:
            from ..ui.backend.main import app
            config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
            server = uvicorn.Server(config)
            server.run()
        except Exception as e:
            print(f"Failed to start backend server: {e}")

    def open_app(self, icon, item):
        if not self.running:
            self.server_thread = threading.Thread(target=self.start_backend_server, daemon=True)
            self.server_thread.start()
            self.running = True
            time.sleep(2)
        
        webbrowser.open('http://127.0.0.1:8000')

    def open_settings(self, icon, item):
        if not self.running:
            self.server_thread = threading.Thread(target=self.start_backend_server, daemon=True)
            self.server_thread.start()
            self.running = True
            time.sleep(2)
        
        webbrowser.open('http://127.0.0.1:8000/settings')

    def open_documents(self, icon, item):
        if not self.running:
            self.server_thread = threading.Thread(target=self.start_backend_server, daemon=True)
            self.server_thread.start()
            self.running = True
            time.sleep(2)
        
        webbrowser.open('http://127.0.0.1:8000/documents')

    def open_chat(self, icon, item):
        if not self.running:
            self.server_thread = threading.Thread(target=self.start_backend_server, daemon=True)
            self.server_thread.start()
            self.running = True
            time.sleep(2)
        
        webbrowser.open('http://127.0.0.1:8000/chat')

    def open_rag(self, icon, item):
        if not self.running:
            self.server_thread = threading.Thread(target=self.start_backend_server, daemon=True)
            self.server_thread.start()
            self.running = True
            time.sleep(2)
        
        webbrowser.open('http://127.0.0.1:8000/rag')

    def quit_app(self, icon, item):
        self.running = False
        icon.stop()
        if self.server_thread and self.server_thread.is_alive():
            # In a real implementation, we'd gracefully shut down the server
            pass
        sys.exit(0)

    def run(self):
        image = self.create_image()
        
        menu = pystray.Menu(
            item('Open Finance Agent', self.open_app, default=True),
            pystray.Menu.SEPARATOR,
            item('Settings', self.open_settings),
            item('Document Analysis', self.open_documents),
            item('Chat Interface', self.open_chat),
            item('RAG Documents', self.open_rag),
            pystray.Menu.SEPARATOR,
            item('Quit', self.quit_app)
        )
        
        self.icon = pystray.Icon("finance_agent", image, "Personal Finance Agent", menu)
        self.icon.run()

def main():
    try:
        app = FinanceAgentTray()
        app.run()
    except KeyboardInterrupt:
        print("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()