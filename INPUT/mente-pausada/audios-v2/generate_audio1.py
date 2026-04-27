import asyncio
import edge_tts
import zipfile
import re

def extract_audio1_text():
    docx_path = r"C:\Users\lucas\AppData\Roaming\Claude\CLAUDE\inbox\MENTE PAUSADA\AUDIOS RUIDO MENTAL (1).docx"
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            raw_bytes = f.read()

    text = re.sub(r'<[^>]+>', ' ', raw_bytes.decode('latin-1'))
    text = re.sub(r'\s+', ' ', text).strip()

    start = text.find('AUDIO 1')
    end = text.find('AUDIO 2')
    raw = text[start:end]

    # Remove title
    raw = raw.replace('AUDIO 1 - EL INTERRUPTOR FISIOLOGICO ', '', 1)

    # Replace ellipsis-like chars and curly quotes for clean TTS
    raw = raw.replace('…', ', ')  # …
    raw = raw.replace('’', "'").replace('‘', "'")
    raw = raw.replace('“', '"').replace('”', '"')
    raw = raw.replace('\xab', '"').replace('\xbb', '"')
    raw = raw.replace('«', '"').replace('»', '"')

    return raw.strip()

async def generate():
    text = extract_audio1_text()
    print(f"Text length: {len(text)} chars")
    print("Preview:")
    print(text[:200])
    print("\nGenerating audio with es-ES-LuciaNeural...")

    output_path = r"C:\Users\lucas\AppData\Roaming\Claude\CLAUDE\mente-pausada\audios-v2\output\audio_01_interruptor_fisiologico.mp3"

    tts = edge_tts.Communicate(
        text=text,
        voice="es-ES-LuciaNeural",
        rate="-10%",
        volume="+0%",
        pitch="-3Hz"
    )
    await tts.save(output_path)
    print(f"\nDone! Audio saved to:\n{output_path}")

asyncio.run(generate())
