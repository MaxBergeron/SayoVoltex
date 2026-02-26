import pygame, time
from game import settings, utils

class MusicPlayer:
    def __init__(self, audio_path):
        game_settings = settings.load_settings()
        self.audio_delay = game_settings["audio_delay"]
        self.audio_path = audio_path

        self.length_ms = 0

        # Playback state
        self.is_playing = False
        self.is_loaded = False

        # Timing reference
        self.start_perf = 0.0
        self.start_position_ms = 0


    # ----------------------------
    # Load Audio Once
    # ----------------------------

    def load(self):
        pygame.mixer.music.stop()
    

        try:
            pygame.mixer.music.load(self.audio_path)
            self.length_ms = int( pygame.mixer.Sound(self.audio_path).get_length() * 1000 )    

        except pygame.error as e:
            utils.show_error_modal(None, str(e))
            self.is_loaded = False
            return False, e
        
        self.is_loaded = True
        return True, None

    # ----------------------------
    # Play / Pause / Stop
    # ----------------------------

    def play(self):
        """Start from beginning."""
        self.load()
        try: 
            pygame.mixer.music.play()

        except pygame.error as e:
            utils.show_error_modal(None, str(e))


        self.start_position_ms = 0.0
        self.start_perf = time.perf_counter()

        self.is_playing = True

    def pause(self):
        """Freeze playback position."""
        if not self.is_playing:
            return

        elapsed = (time.perf_counter() - self.start_perf) * 1000
        self.start_position_ms += elapsed

        pygame.mixer.music.pause()
        self.is_playing = False

    def unpause(self):
        if self.is_playing:
            return

        pygame.mixer.music.unpause()

        # Reset high precision anchor
        self.start_perf = time.perf_counter()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()

        self.is_playing = False
        self.start_position_ms = 0.0
        self.start_perf = 0.0


    def get_position_ms(self):
        if not self.is_playing:
            return self.start_position_ms + self.audio_delay

        elapsed = (time.perf_counter() - self.start_perf) * 1000
        return self.start_position_ms + elapsed + self.audio_delay


    def set_position_ms(self, position_ms):

        position_ms = max(0, min(position_ms, self.length_ms))

        self.start_position_ms = float(position_ms)
        self.start_perf = time.perf_counter()

        if self.is_playing:
            pygame.mixer.music.play(start=position_ms / 1000.0)
        else:
            pygame.mixer.music.play(start=position_ms / 1000.0)
            pygame.mixer.music.pause()


    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
        pass


    def get_length_ms(self):
        return self.length_ms
