import sys
import pytesseract
from PIL import Image
import os

def extract_text_from_image(image_path):
    # Abrir a imagem
    img = Image.open(image_path)

    # Extrair texto da imagem
    text = pytesseract.image_to_string(img)

    return text

def save_text_to_txt(text, txt_path):
    # Salvar o texto extraído em um arquivo .txt
    with open(txt_path, "w") as text_file:
        text_file.write(text)

if __name__ == "__main__":
    # Verificar se o caminho da imagem foi passado como argumento
    if len(sys.argv) != 2:
        print("Uso: python extract_text.py <caminho_da_imagem>")
        sys.exit(1)

    # Obter o caminho do arquivo de imagem a partir dos argumentos
    image_file = sys.argv[1]

    # Extrair o texto da imagem
    extracted_text = extract_text_from_image(image_file)

    # Definir o nome do arquivo de saída .txt (mesmo nome da imagem)
    output_file = os.path.splitext(image_file)[0] + ".txt"

    # Salvar o texto extraído em um arquivo .txt
    save_text_to_txt(extracted_text, output_file)

    # Confirmar a conclusão
    print(f"Texto extraído e salvo em: {output_file}")
