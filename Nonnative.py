# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 17:10:27 2023

@author: punam.chaudhari
"""
import os
import ocrmypdf
#import pdftotext
import concurrent.futures


input_directory = r'C:\punam\Proj_Nonnative\PDF_output\input'


output_directory = 'C:\punam\Proj_Nonnative\PDF_output\output'

# Get a list of PDF files in the input directory
pdf_files = [file for file in os.listdir(input_directory) if file.endswith('.PDF')]

def process_pdf(pdf_file):
    try:
       
        input_pdf_file = os.path.join(input_directory, pdf_file)
        output_pdf_file = os.path.join(output_directory, pdf_file)

     
        ocrmypdf.ocr(input_pdf_file, output_pdf_file)

        print(f"OCR completed for {pdf_file}.")

        # the output text file path for the current PDF file
        output_txt_file = os.path.splitext(output_pdf_file)[0] + '.txt'

        # Open the OCR'ed PDF file in binary mode
        with open(output_pdf_file, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf = pdftotext.PDF(pdf_file)

            # Extract the text from all pages in the PDF file
            text = "\n\n".join(pdf)

           
            with open(output_txt_file, 'w') as txt_file:
                txt_file.write(text)

        print(f"Text extracted and saved for {pdf_file}.")
    except Exception as e:
        print(f"Error processing {pdf_file}: {e}")

# Set the maximum number of threads to use
max_threads = 4

# Create a ThreadPoolExecutor to process PDF files concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    # Submit the PDF files for processing
    future_results = [executor.submit(process_pdf, pdf_file) for pdf_file in pdf_files]

    # Wait for all tasks to complete
    concurrent.futures.wait(future_results)

print("OCR and text extraction process completed for all PDF files.")