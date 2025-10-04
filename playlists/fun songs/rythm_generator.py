import wave, struct, math

def generate_clicks(filename, bpm, duration_sec):
    framerate = 44100
    amplitude = 16000
    period = 60.0 / bpm  # seconds between clicks
    nframes = int(duration_sec * framerate)
    with wave.open(filename, 'w') as w:
        w.setparams((1, 2, framerate, nframes, 'NONE', 'not compressed'))
        for i in range(nframes):
            t = i / framerate
            sample = amplitude if (t % period) < 0.01 else 0
            w.writeframes(struct.pack('<h', int(sample)))
    print(f"Wygenerowano plik {filename}")

generate_clicks("clicks200.wav", bpm=200, duration_sec=15)
