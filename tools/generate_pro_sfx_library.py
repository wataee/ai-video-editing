import os
import wave
import struct
import numpy as np

SAMPLE_RATE = 48000

def write_wav(path, samples):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Normalize to -1.0 dB peak
    max_val = np.max(np.abs(samples))
    if max_val > 0:
        samples = samples / max_val * 0.89 # -1.0 dB
    int_samples = (samples * 32767).astype(np.int16)
    with wave.open(path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(int_samples.tobytes())
    print(f"Generated: {path} ({len(samples)/SAMPLE_RATE:.2f}s)")

# --- 1. WHOOSHES ---

# Deep Voice Whooshes (Low-pass filtered resonant sub sweep with noise texture)
def gen_deep_voice_whoosh(duration, f_start, f_peak, f_end):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    # Bell shaped frequency trajectory
    bell = np.exp(-((t - duration * 0.45) / (duration * 0.28)) ** 2)
    freq = f_start + (f_peak - f_start) * bell
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    sub = np.sin(phase) + 0.3 * np.sin(2 * phase)
    # Noise texture
    noise = np.random.normal(0, 1, len(t))
    # Lowpass filter on noise using simple moving average
    kernel_size = 40
    noise_smooth = np.convolve(noise, np.ones(kernel_size)/kernel_size, mode='same')
    out = (sub * 0.75 + noise_smooth * 0.5) * bell
    # Envelope
    env = np.sin(np.pi * (t / duration)) ** 1.5
    return out * env

# Hollow Whoosh (Resonant bandpass sweep)
def gen_hollow_whoosh(duration, center_f):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    bell = np.exp(-((t - duration * 0.5) / (duration * 0.25)) ** 2)
    carrier = np.sin(2 * np.pi * center_f * t)
    noise = np.random.normal(0, 1, len(t))
    mod = np.sin(2 * np.pi * 12 * t)
    out = (noise * 0.6 + carrier * 0.4 * (1 + 0.5 * mod)) * bell
    return out

# Transition Spacey Whoosh
def gen_spacey_whoosh(duration):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    f = np.geomspace(80, 2400, len(t))
    phase = 2 * np.pi * np.cumsum(f) / SAMPLE_RATE
    fm = np.sin(2 * np.pi * 35 * t)
    sig = np.sin(phase + 1.5 * fm)
    env = np.exp(-((t - duration * 0.7) / (duration * 0.3)) ** 2)
    return sig * env

# --- 2. TEXTURES ---

# Pops (Short clean transient pitch drop)
def gen_pop(f_start, f_end, duration):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    f = np.geomspace(f_start, f_end, len(t))
    phase = 2 * np.pi * np.cumsum(f) / SAMPLE_RATE
    env = np.exp(-t * (1.0 / (duration * 0.18)))
    return np.sin(phase) * env

# UI Clicks (Ultra-short tactile click)
def gen_click(freq, decay):
    t = np.linspace(0, 0.04, int(0.04 * SAMPLE_RATE), endpoint=False)
    sig = np.sin(2 * np.pi * freq * t) + 0.3 * np.random.normal(0, 1, len(t))
    env = np.exp(-t * decay)
    return sig * env

# Camera Shutter Click
def gen_camera_shutter():
    # Double click: mirror flip + curtain close
    t = np.linspace(0, 0.18, int(0.18 * SAMPLE_RATE), endpoint=False)
    click1 = gen_click(1800, 350)
    click2 = gen_click(950, 400)
    out = np.zeros(len(t))
    out[:len(click1)] += click1 * 0.8
    offset2 = int(0.045 * SAMPLE_RATE)
    out[offset2:offset2+len(click2)] += click2 * 1.0
    return out

# Gears / Mechanical Typewriter
def gen_gears_mechanical(repeats=4, spacing=0.04):
    total_dur = repeats * spacing + 0.05
    t = np.linspace(0, total_dur, int(total_dur * SAMPLE_RATE), endpoint=False)
    out = np.zeros(len(t))
    for i in range(repeats):
        clk = gen_click(1200 + i * 150, 500)
        idx = int(i * spacing * SAMPLE_RATE)
        out[idx:idx+len(clk)] += clk
    return out

# Sci-Fi Hit / Impact
def gen_scifi_hit(duration=0.8):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    f_drop = np.geomspace(850, 45, len(t))
    phase = 2 * np.pi * np.cumsum(f_drop) / SAMPLE_RATE
    laser = np.sin(phase)
    # Sub boom
    sub = np.sin(2 * np.pi * 55 * t) * np.exp(-t * 4.5)
    env = np.exp(-t * 7.0)
    return (laser * 0.6 + sub * 0.8) * env

# --- 3. RISERS & HITS ---

# Sharp Bass Riser (Exponential low-end pitch bend up, Joseph's #1 favorite)
def gen_sharp_bass_riser(duration=2.2):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    # Pitch rises from 35 Hz to 240 Hz with dramatic curve
    f = 35 + (240 - 35) * ((t / duration) ** 2.8)
    phase = 2 * np.pi * np.cumsum(f) / SAMPLE_RATE
    sub = np.sin(phase) + 0.4 * np.sin(2 * phase)
    # Swelling volume envelope
    env = (t / duration) ** 2.2
    # Add subtle saturation / harmonics near the end
    out = np.tanh(sub * (1.0 + 2.0 * (t / duration))) * env
    return out

# Metallic Riser (FM synthesis shimmering build, Joseph's #2 favorite)
def gen_metallic_riser(duration=2.5):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    carrier_f = np.geomspace(220, 1800, len(t))
    mod_f = np.geomspace(311, 2450, len(t))
    phase_mod = 2 * np.pi * np.cumsum(mod_f) / SAMPLE_RATE
    modulator = np.sin(phase_mod)
    phase_c = 2 * np.pi * np.cumsum(carrier_f) / SAMPLE_RATE
    # Metallic FM
    metallic = np.sin(phase_c + 3.0 * (t/duration) * modulator)
    env = (t / duration) ** 2.5
    return metallic * env

# Suck-back Riser (Reversed cymbal/whoosh effect)
def gen_suck_back_riser(duration=1.8):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    noise = np.random.normal(0, 1, len(t))
    f_center = np.geomspace(120, 3200, len(t))
    carrier = np.sin(2 * np.pi * f_center * t)
    env = (t / duration) ** 3.5 # Steep exponential rise to dead cut
    out = (noise * 0.7 + carrier * 0.5) * env
    return out

# Impact Hit (Deep cinematic boom)
def gen_impact_hit(duration=1.6):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    sub = np.sin(2 * np.pi * 48 * t) * np.exp(-t * 2.8)
    click = np.sin(2 * np.pi * 320 * t[:int(0.05*SAMPLE_RATE)]) * np.exp(-t[:int(0.05*SAMPLE_RATE)] * 80)
    out = sub
    out[:len(click)] += click * 0.9
    return out

def main():
    base = "assets/01_SFX"
    
    # 1. Whooshes
    write_wav(f"{base}/01_whooshes/deep_voice/deep_voice_whoosh_01.wav", gen_deep_voice_whoosh(0.7, 70, 340, 50))
    write_wav(f"{base}/01_whooshes/deep_voice/deep_voice_whoosh_02.wav", gen_deep_voice_whoosh(0.9, 55, 280, 40))
    write_wav(f"{base}/01_whooshes/deep_voice/deep_voice_whoosh_03.wav", gen_deep_voice_whoosh(0.5, 90, 420, 60))
    
    write_wav(f"{base}/01_whooshes/hollow/hollow_whoosh_01.wav", gen_hollow_whoosh(0.65, 450))
    write_wav(f"{base}/01_whooshes/hollow/hollow_whoosh_02.wav", gen_hollow_whoosh(0.85, 380))
    
    write_wav(f"{base}/01_whooshes/transitions/synthetic_transition_whoosh.wav", gen_spacey_whoosh(1.1))
    write_wav(f"{base}/01_whooshes/transitions/transition_spacey_whoosh.wav", gen_spacey_whoosh(1.4))

    # 2. Textures
    write_wav(f"{base}/02_textures/pops/pop_cartoon_clean.wav", gen_pop(1400, 220, 0.08))
    write_wav(f"{base}/02_textures/pops/pop_bubble_high.wav", gen_pop(1900, 350, 0.06))
    
    write_wav(f"{base}/02_textures/clicks_ui/mouse_click_soft.wav", gen_click(2200, 600))
    write_wav(f"{base}/02_textures/clicks_ui/mechanical_button.wav", gen_click(850, 400))
    
    write_wav(f"{base}/02_textures/camera_shutter/camera_click_fast.wav", gen_camera_shutter())
    write_wav(f"{base}/02_textures/gears_typewriter/tiny_gearwheel_loop.wav", gen_gears_mechanical(5, 0.035))
    write_wav(f"{base}/02_textures/gears_typewriter/complex_mechanism_gizmo.wav", gen_gears_mechanical(8, 0.045))
    
    write_wav(f"{base}/02_textures/sci_fi_hits/sci_fi_impact_reveal.wav", gen_scifi_hit(0.7))
    write_wav(f"{base}/02_textures/sci_fi_hits/activate_energy_hit.wav", gen_scifi_hit(0.9))

    # 3. Risers & Hits
    write_wav(f"{base}/03_risers_hits/sharp_bass_risers/sharp_bass_riser_01.wav", gen_sharp_bass_riser(2.2))
    write_wav(f"{base}/03_risers_hits/sharp_bass_risers/sharp_bass_riser_02.wav", gen_sharp_bass_riser(1.6))
    write_wav(f"{base}/03_risers_hits/sharp_bass_risers/sharp_bass_riser_fast.wav", gen_sharp_bass_riser(1.1))
    
    write_wav(f"{base}/03_risers_hits/metallic_risers/metallic_riser_01.wav", gen_metallic_riser(2.4))
    write_wav(f"{base}/03_risers_hits/metallic_risers/metallic_riser_02.wav", gen_metallic_riser(1.8))
    
    write_wav(f"{base}/03_risers_hits/suck_back_risers/suck_back_riser_01.wav", gen_suck_back_riser(1.8))
    write_wav(f"{base}/03_risers_hits/suck_back_risers/suck_back_riser_fast.wav", gen_suck_back_riser(1.2))
    
    write_wav(f"{base}/03_risers_hits/impact_hits/cinematic_boom_01.wav", gen_impact_hit(1.8))
    write_wav(f"{base}/03_risers_hits/impact_hits/bass_drop_hit_01.wav", gen_impact_hit(1.4))

    print("\nSUCCESS: All signature SFX generated according to Joseph's specifications!")

if __name__ == '__main__':
    main()
