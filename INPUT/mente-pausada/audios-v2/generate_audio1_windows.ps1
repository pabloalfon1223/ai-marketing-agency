Add-Type -AssemblyName System.Speech

# Read text from file
$text = Get-Content -Path "C:\Users\lucas\AppData\Roaming\Claude\CLAUDE\mente-pausada\audios-v2\audio1_text.txt" -Raw -Encoding UTF8

$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice('Microsoft Sabina Desktop')
$synth.Rate = -3  # -10 (fastest) to 10 (slowest). -3 = slightly slow, natural for guided audio

$outputPath = "C:\Users\lucas\AppData\Roaming\Claude\CLAUDE\mente-pausada\audios-v2\output\audio_01_interruptor_fisiologico.wav"
$synth.SetOutputToWaveFile($outputPath)
$synth.Speak($text)
$synth.Dispose()

Write-Host "Audio generated: $outputPath"
