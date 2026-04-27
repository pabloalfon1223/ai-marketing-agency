"""
Extrae el texto del Audio 1 del DOCX y lo guarda en TXT limpio para el PowerShell.
"""
import zipfile, re

docx_path = r"C:\Users\lucas\AppData\Roaming\Claude\CLAUDE\inbox\MENTE PAUSADA\AUDIOS RUIDO MENTAL (1).docx"
output_txt = r"C:\Users\lucas\AppData\Roaming\Claude\CLAUDE\mente-pausada\audios-v2\audio1_text.txt"

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

# Clean special chars
raw = raw.replace(u'…', '... ')  # ellipsis
raw = raw.replace(u'‘', "'").replace(u'’', "'")
raw = raw.replace(u'“', '"').replace(u'”', '"')

with open(output_txt, 'w', encoding='utf-8') as f:
    f.write(raw.strip())

print(f"Text saved to: {output_txt}")
print(f"Length: {len(raw)} chars")
