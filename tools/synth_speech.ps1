# Synthesis script with proper UTF-8 handling
param(
    [string]$TextFile = "clients\_demo\raw\russian_ref_15s_text.txt",
    [string]$OutWav = "clients\_demo\raw\russian_ref_clean.wav",
    [string]$OutMp4 = "clients\_demo\raw\russian_ref_15s.mp4"
)

$text = [System.IO.File]::ReadAllText($TextFile, [System.Text.Encoding]::UTF8).Trim()
Write-Host "Read text: $text"

Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice("Microsoft Irina Desktop")
$synth.SetOutputToWaveFile($OutWav)
$synth.Speak($text)
$synth.Dispose()

Write-Host "Synthesized WAV to $OutWav"

# Create 15s MP4 with FFmpeg
ffmpeg -y -f lavfi -i color=c=0x111827:s=1080x1920:r=30 -i $OutWav -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest $OutMp4

Write-Host "Synthesized MP4 to $OutMp4"
