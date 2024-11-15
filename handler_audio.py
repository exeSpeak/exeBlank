import os
import pygame

class AudioHandler:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}  # Dictionary to store sound effects
        self.music = {}   # Dictionary to store music tracks
        self.current_music = None
        self.music_volume = 1.0
        self.sound_volume = 1.0
        self._load_default_audio()
    
    def _load_default_audio(self):
        """Load default audio from the defaults directory"""
        script_dir = os.path.dirname(__file__)
        default_audio_dir = os.path.join(script_dir, 'defaults', 'audio')
        
        # Create audio directories if they don't exist
        os.makedirs(os.path.join(default_audio_dir, 'sounds'), exist_ok=True)
        os.makedirs(os.path.join(default_audio_dir, 'music'), exist_ok=True)
        
        # Load default sound effects
        sounds_dir = os.path.join(default_audio_dir, 'sounds')
        if os.path.exists(sounds_dir):
            for file in os.listdir(sounds_dir):
                if file.endswith(('.wav', '.ogg', '.mp3')):
                    name = os.path.splitext(file)[0]
                    self.add_sound(name, os.path.join(sounds_dir, file))
        
        # Load default music
        music_dir = os.path.join(default_audio_dir, 'music')
        if os.path.exists(music_dir):
            for file in os.listdir(music_dir):
                if file.endswith(('.wav', '.ogg', '.mp3')):
                    name = os.path.splitext(file)[0]
                    self.add_music(name, os.path.join(music_dir, file))
    
    def add_sound(self, name, sound_path):
        """
        Add a sound effect to the collection
        :param name: Name identifier for the sound
        :param sound_path: Path to the sound file
        """
        try:
            self.sounds[name] = pygame.mixer.Sound(sound_path)
            self.sounds[name].set_volume(self.sound_volume)
        except pygame.error as e:
            print(f"Error loading sound {name}: {e}")
    
    def add_music(self, name, music_path):
        """
        Add a music track to the collection
        :param name: Name identifier for the music
        :param music_path: Path to the music file
        """
        if os.path.exists(music_path):
            self.music[name] = music_path
        else:
            print(f"Music file not found: {music_path}")
    
    def play_sound(self, name, loops=0):
        """
        Play a sound effect
        :param name: Name of the sound to play
        :param loops: Number of times to loop (-1 for infinite)
        """
        if name in self.sounds:
            self.sounds[name].play(loops)
        else:
            print(f"Sound not found: {name}")
    
    def play_music(self, name, loops=-1, fade_ms=0):
        """
        Play a music track
        :param name: Name of the music to play
        :param loops: Number of times to loop (-1 for infinite)
        :param fade_ms: Fade-in time in milliseconds
        """
        if name in self.music:
            try:
                if fade_ms > 0:
                    pygame.mixer.music.fadeout(fade_ms)
                pygame.mixer.music.load(self.music[name])
                pygame.mixer.music.play(loops, fade_ms=fade_ms)
                pygame.mixer.music.set_volume(self.music_volume)
                self.current_music = name
            except pygame.error as e:
                print(f"Error playing music {name}: {e}")
        else:
            print(f"Music not found: {name}")
    
    def stop_music(self, fade_ms=0):
        """
        Stop the currently playing music
        :param fade_ms: Fade-out time in milliseconds
        """
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()
        self.current_music = None
    
    def pause_music(self):
        """Pause the currently playing music"""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause the currently playing music"""
        pygame.mixer.music.unpause()
    
    def set_music_volume(self, volume):
        """
        Set the music volume
        :param volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sound_volume(self, volume):
        """
        Set the sound effects volume
        :param volume: Volume level (0.0 to 1.0)
        """
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def get_music_volume(self):
        """Get the current music volume"""
        return self.music_volume
    
    def get_sound_volume(self):
        """Get the current sound effects volume"""
        return self.sound_volume
    
    def is_music_playing(self):
        """Check if music is currently playing"""
        return pygame.mixer.music.get_busy()

# Create a global audio handler instance
audio_handler = AudioHandler()

# Global access functions
def play_sound(name, loops=0):
    """Play a sound effect"""
    audio_handler.play_sound(name, loops)

def play_music(name, loops=-1, fade_ms=0):
    """Play a music track"""
    audio_handler.play_music(name, loops, fade_ms)

def stop_music(fade_ms=0):
    """Stop the current music"""
    audio_handler.stop_music(fade_ms)

def set_music_volume(volume):
    """Set music volume"""
    audio_handler.set_music_volume(volume)

def set_sound_volume(volume):
    """Set sound effects volume"""
    audio_handler.set_sound_volume(volume)