import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

# Function to add numbers to the bottom-left and bottom-right corners of PDFs
def add_numbers_to_pdfs(folder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            # Extract the number from the file name
            number = file_name.split()[0]
            
            # Read the original PDF
            pdf_path = os.path.join(folder_path, file_name)
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            # Dimensions of A4 paper
            page_width, page_height = A4

            # Process each page
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]

                # Create a temporary PDF with the number overlay
                packet = BytesIO()
                can = canvas.Canvas(packet, pagesize=A4)
                can.setFont("Helvetica", 16)  # Set font and size

                # Bottom-left corner
                left_x_position = 30  # Distance from the left edge
                left_y_position = 30  # Distance from the bottom edge
                can.drawString(left_x_position, left_y_position, number)

                # Bottom-right corner
                text_width = can.stringWidth(number, "Helvetica", 16)
                right_x_position = page_width - 30 - text_width  # Distance from the right edge
                right_y_position = 30  # Distance from the bottom edge
                can.drawString(right_x_position, right_y_position, number)

                can.save()
                packet.seek(0)

                # Merge the overlay with the original page
                overlay = PdfReader(packet).pages[0]
                page.merge_page(overlay)
                writer.add_page(page)
            
            # Save the modified PDF
            output_path = os.path.join(output_folder, file_name)
            with open(output_path, "wb") as output_file:
                writer.write(output_file)


input_folder = "inputpdf"
output_folder = "outputpdf"

add_numbers_to_pdfs(input_folder, output_folder)
