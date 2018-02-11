import ghostscript

def pdf2jpeg(pdf_input_path, jpeg_output_path):
    args = ["pdf2jpeg", # actual value doesn't matter
            "-dNOPAUSE",
            "-sDEVICE=jpeg",
            "-r144",
            "-sOutputFile=" + jpeg_output_path,
            pdf_input_path]
    ghostscript.Ghostscript(*args)