import pygame


class MusicPlayer:
    def __init__(self, audio_path):
        self.audio_path = audio_path

        self.length_ms = 0

        # Playback state
        self.is_playing = False
        self.is_loaded = False

        # Timing reference
        self.start_ticks = 0
        self.start_position_ms = 0

        pygame.mixer.init()

    # ----------------------------
    # Load Audio Once
    # ----------------------------

    def load(self):
        if self.is_loaded:
            return

        pygame.mixer.music.load(self.audio_path)

        # Length only used for bounds
        self.length_ms = int(
            pygame.mixer.Sound(self.audio_path).get_length() * 1000
        )

        self.is_loaded = True

    # ----------------------------
    # Play / Pause / Stop
    # ----------------------------

    def play(self):
        """Start from beginning."""
        self.load()

        pygame.mixer.music.play()
        self.start_ticks = pygame.time.get_ticks()
        self.start_position_ms = 0

        self.is_playing = True

    def pause(self):
        """Freeze playback position."""
        if not self.is_playing:
            return

        # Store exact current position
        self.start_position_ms = self.get_position_ms()

        pygame.mixer.music.pause()
        self.is_playing = False

    def unpause(self):
        if self.is_playing:
            return

        pygame.mixer.music.unpause()

        # Reset tick anchor so time continues correctly
        self.start_ticks = pygame.time.get_ticks()

        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()

        self.is_playing = False
        self.start_ticks = 0
        self.start_position_ms = 0


    def get_position_ms(self):
        if self.is_playing:
            elapsed = pygame.time.get_ticks() - self.start_ticks
            return self.start_position_ms + elapsed

        return self.start_position_ms


    def set_position_ms(self, position_ms):
        self.load()

        position_ms = max(0, min(position_ms, self.length_ms))
        was_playing = self.is_playing
        pygame.mixer.music.play(start=position_ms / 1000)

        self.start_ticks = pygame.time.get_ticks()
        self.start_position_ms = position_ms

        self.is_playing = True

        if not was_playing:
            pygame.mixer.music.pause()
            self.is_playing = False


    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)


    def get_length_ms(self):
        return self.length_ms
