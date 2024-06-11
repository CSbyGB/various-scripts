import sys
from PIL import Image
import pytesseract

def extract_text(image_path, output_file):
    # Charger l'image
    img = Image.open(image_path)
    
    # Utiliser pytesseract pour extraire le texte
    text = pytesseract.image_to_string(img)
    
    # Écrire le texte dans un fichier
    with open(output_file, 'w') as file:
        file.write(text)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <image_path> <output_file>")
        sys.exit(1)

    image_path = sys.argv[1]
    output_file = sys.argv[2]
    
    extract_text(image_path, output_file)
