# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 13:36:07 2023

@author: punam.chaudhari
"""

import os
import ocrmypdf
import pdftotext
import concurrent.futures
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_pdfs', methods=['GET', 'POST'])
def process_pdfs():
    if request.method == 'GET':
        return jsonify({'message': 'Welcome to the PDF processing API!'})

    elif request.method == 'POST':
        try:
            input_directory = request.form.get('input_directory')
            output_directory = request.form.get('output_directory')

            # Get a list of PDF files in the input directory
            pdf_files = [file for file in os.listdir(input_directory) if file.endswith('.PDF')]

            def process_pdf(pdf_file):
                try:
                    input_pdf_file = os.path.join(input_directory, pdf_file)
                    output_pdf_file = os.path.join(output_directory, pdf_file)

                    ocrmypdf.ocr(input_pdf_file, output_pdf_file)

                    print(f"OCR completed for {pdf_file}.")

                    
                    output_txt_file = os.path.splitext(output_pdf_file)[0] + '.txt'

                    
                    with open(output_pdf_file, 'rb') as pdf_file:
                       
                        pdf = pdftotext.PDF(pdf_file)

                        
                        text = "\n\n".join(pdf)

                        with open(output_txt_file, 'w') as txt_file:
                            txt_file.write(text)

                    print(f"Text extracted and saved for {pdf_file}.")
                except Exception as e:
                    print(f"Error processing {pdf_file}: {e}")

           
            max_threads = 4

           
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
                
                future_results = [executor.submit(process_pdf, pdf_file) for pdf_file in pdf_files]

                
                concurrent.futures.wait(future_results)

            return jsonify({'message': 'OCR and text extraction process completed for all PDF files.'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
