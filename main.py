import Files.OCR as OCR
import threaded_main
import Files.interface as interface
import time
import Files.overlay as overlay

import tkinter as tk
import threading

def background_task():
    threaded_main.main()
    print("Background task is running")

def run_tkinter_app():
    overlay.main(1)
    root = interface.interface()
    print("Running Tkinter app")
    root.mainloop()

def main():
    # Start the background task in a separate thread
    background_thread = threading.Thread(target=background_task)
    background_thread.start()

    # Run Tkinter app on the main thread
    '''run_tkinter_app()'''

if __name__ == "__main__":
    main()