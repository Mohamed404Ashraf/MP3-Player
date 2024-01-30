import tkinter as tk
import os
import random
import pygame

class MusicPlayer:
    def __init__(self, master):
        self.master = master
        master.title("Music Player")

        # Create the playlist
        self.playlist = []
        for filename in os.listdir("music"):
            if filename.endswith(".mp3"):
                self.playlist.append(os.path.join("music", filename))
        random.shuffle(self.playlist)

        # Initialize variables
        self.current_song = None
        self.paused = False
        self.shuffle = True

        # Create the widgets
        self.playlist_label = tk.Label(master, text="Playlist")
        self.playlist_label.pack(pady=5)
        self.playlist_listbox = tk.Listbox(master)
        for song in self.playlist:
            self.playlist_listbox.insert(tk.END, os.path.basename(song))
        self.playlist_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.controls_frame = tk.Frame(master)
        self.controls_frame.pack(pady=5)
        self.play_button = tk.Button(self.controls_frame, text="Play", command=self.play_pause)
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.skip_button = tk.Button(self.controls_frame, text="Skip", command=self.skip)
        self.skip_button.pack(side=tk.LEFT, padx=5)
        self.shuffle_button = tk.Button(self.controls_frame, text="Shuffle", command=self.toggle_shuffle)
        self.shuffle_button.pack(side=tk.LEFT, padx=5)
        self.volume_label = tk.Label(self.controls_frame, text="Volume:")
        self.volume_label.pack(side=tk.LEFT, padx=5)
        self.volume_scale = tk.Scale(self.controls_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(50)
        self.volume_scale.pack(side=tk.LEFT, padx=5)
        
        # Initialize Pygame mixer
        pygame.mixer.init()

        # Start playing the first song
        self.play()

    def play(self):
        if not self.current_song:
            self.current_song = self.playlist[0]
        pygame.mixer.music.load(self.current_song)
        pygame.mixer.music.play()

    def pause(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            self.play_button.config(text="Resume")
        else:
            pygame.mixer.music.unpause()
            self.paused = False
            self.play_button.config(text="Pause")

    def play_pause(self):
        if not pygame.mixer.music.get_busy():
            self.play()
        else:
            self.pause()

    def skip(self):
        if self.shuffle:
            self.current_song = random.choice(self.playlist)
        else:
            index = self.playlist.index(self.current_song)
            if index == len(self.playlist) - 1:
                self.current_song = self.playlist[0]
            else:
                self.current_song = self.playlist[index + 1]
        self.play()

    def toggle_shuffle(self):
        if self.shuffle:
            self.shuffle = False
            self.shuffle_button.config(text="Shuffle Off")
        else:
            self.shuffle = True
            self.shuffle_button.config(text="Shuffle On")

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(int(volume) / 100)

# Create the main window
root = tk.Tk()

# music player
music_player = MusicPlayer(root)

# Run the main loop
root.mainloop()