import os
import pygame

from recognizer.hand_checks import is_rock_hand
from modes.base import BaseMode

class RockMode(BaseMode):
    def __init__(self):
        self.name = "Rock"
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.is_rock_gesture = False
        self.song_paths = [
            os.path.join("assets/songs", filename)
            for filename in os.listdir("assets/songs")
            if filename.endswith((".mp3", ".wav"))
        ]
        self.current_index = -1
        self.is_playing_song = False
        self.was_rock_gesture = False
    
    def begin_frame(self):
        self.is_rock_gesture = False
    
    def process_hand(self, landmarks):
        if is_rock_hand(landmarks):
            self.is_rock_gesture = True

    def draw_overlay(self, frame):
        if self.is_rock_gesture and not self.was_rock_gesture:
            self.current_index = (self.current_index + 1) % len(self.song_paths)
            self.play_current_song()

        self.was_rock_gesture = self.is_rock_gesture
    
    def close(self):
        if self.is_playing_song:
            pygame.mixer.music.stop()
            self.is_playing_song = False
        self.was_rock_gesture = False
    
    def play_current_song(self):
        song_path = self.song_paths[self.current_index]
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.is_playing_song = True
