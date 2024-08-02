import os
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import tempfile

from process import process
from process import processLayout


def save_page_as_pdf(page, output_path):
    writer = PdfWriter()
    writer.add_page(page)
    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf)


def process_pdfs(input_folder, output_folder):
    # Assurez-vous que le dossier de sortie existe
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Parcours des fichiers PDF dans le dossier d'entrée
    for pdf_file in os.listdir(input_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, pdf_file)
            pdf_name = os.path.splitext(pdf_file)[0]
            pdf_output_folder = os.path.join(output_folder, pdf_name)

            # Créez un dossier pour chaque PDF dans le dossier de sortie
            Path(pdf_output_folder).mkdir(parents=True, exist_ok=True)

            reader = PdfReader(pdf_path)
            pathName = pdf_output_folder + '/text.txt'

            if not os.path.exists(pathName):
                open(pathName, 'w').close()

            for page_number, page in enumerate(reader.pages):
                pathImage = pdf_output_folder + \
                    '/imagePage' + str(page_number) + '.pdf'
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                    temp_pdf_path = temp_pdf.name
                    save_page_as_pdf(page, temp_pdf_path)

                    # Appel de la fonction process avec le chemin du fichier temporaire
                    result_dfs = process(temp_pdf_path)
                    processLayout(temp_pdf_path, pathName, pathImage)

                    if result_dfs:
                        for i, df in enumerate(result_dfs):
                            excel_filename = os.path.join(
                                pdf_output_folder, f'table_{page_number + 1}_{i + 1}.xlsx')
                            df.to_excel(excel_filename, index=False)
                            print(
                                f"Page {page_number + 1}, Tableau {i + 1} du fichier {pdf_name} traitée et sauvegardée.")

                # Suppression du fichier temporaire après traitement
                os.remove(temp_pdf_path)


input_folder = '/Users/alexandreclin/Desktop/test/input'
output_folder = '/Users/alexandreclin/Desktop/test/output'

process_pdfs(input_folder, output_folder)
