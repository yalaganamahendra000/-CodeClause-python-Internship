import tkinter as tk
from tkinter import messagebox
import pyaudio
import wave
import threading
import time

class AudioRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder")

        self.record_button = tk.Button(root, text="Record", command=self.record)
        self.record_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False

    def record(self):
        self.is_recording = True
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=1024)
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.frames = []
        threading.Thread(target=self._record_audio).start()

    def _record_audio(self):
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def stop(self):
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        self.save()

    def save(self):
        timestamp = time.strftime("%Y%m%d-%H%M%S")  # Generate timestamp
        filename = f"recording_{timestamp}"  # Create filename with timestamp

        with wave.open(f"{filename}.wav", 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))

        messagebox.showinfo("Success", f"Recording saved as {filename}.wav")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorder(root)
    root.mainloop()
