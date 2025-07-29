import mimetypes
import fitz  # PyMuPDF
import PyPDF2

def unlock_pdf(input_path, output_path, password):
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Check if PDF is encrypted
        if reader.is_encrypted:
            if not reader.decrypt(password):
                raise ValueError("Invalid password or unable to unlock PDF.")
            
            # Write unlocked PDF to a new file
            writer = PyPDF2.PdfWriter()
            for page_num in range(len(reader.pages)):
                writer.add_page(reader.pages[page_num])

            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

    return output_path

def convert_pdf_to_images(pdf_path):
    pdf_document = fitz.open(pdf_path)
    image_paths = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image = page.get_pixmap()
        
        img_path = f"{pdf_path}_page_{page_num}.png"
        image.save(img_path)
        image_paths.append(img_path)

    return image_paths