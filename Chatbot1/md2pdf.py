import os
from markdown2 import markdown
from weasyprint import HTML
import glob

def convert_directory_markdown_to_pdf(input_dir, output_dir):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):

        input_file_path = os.path.join(input_dir, filename)
        if os.path.isdir(input_file_path) and filename != ".git":
            convert_directory_markdown_to_pdf(input_dir + "/" + filename, output_dir+"/"+filename+"-pdf")
        
        if filename.endswith('.md'):
            input_file_path = os.path.join(input_dir, filename)
            output_file_name = filename[:-3] + '.pdf'
            output_file_path = os.path.join(output_dir, output_file_name)

            # Read the Markdown file
            with open(input_file_path, 'r', encoding='utf-8') as file:
                markdown_text = file.read()

            # Convert Markdown to HTML
            html_text = markdown(markdown_text)

            # Convert HTML to PDF
            HTML(string=html_text).write_pdf(output_file_path)
            print(f"Converted {input_file_path} to {output_file_path}")


def dir_walk(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            print(len(path) * '---', file)



# Automatically set paths relative to the script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))
input_directory = os.path.join(script_directory, './wiki/capella-docs')
output_directory = os.path.join(script_directory, './wiki/capella-docs-pdf')

convert_directory_markdown_to_pdf("./wiki/capella-docs", output_directory)
# dir_walk(input_directory, output_directory)
# for filename in glob.iglob(input_directory + '**/**', recursive=True):
#      print(filename)
