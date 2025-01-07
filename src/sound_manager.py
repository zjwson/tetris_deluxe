import pygame
from pathlib import Path
from .settings import SOUNDS_DIR, SOUND_EFFECTS, SOUND_VOLUME

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self._load_sounds()
        
    def _load_sounds(self):
        """加载所有音效"""
        for sound_name, sound_file in SOUND_EFFECTS.items():
            try:
                sound_path = SOUNDS_DIR / sound_file
                if sound_path.exists():
                    sound = pygame.mixer.Sound(str(sound_path))
                    sound.set_volume(SOUND_VOLUME)
                    self.sounds[sound_name] = sound
            except Exception as e:
                print(f"无法加载音效 {sound_file}: {e}")
    
    def play(self, sound_name):
        """播放指定音效"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
            
    def stop_all(self):
        """停止所有音效"""
        pygame.mixer.stop()
