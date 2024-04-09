import os 
import pandas as pd
import fitz  # PyMuPDF
import re
from pdf2image import convert_from_path
from gptapi import use_gpt_4v
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from io import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage


def process_response_md(response_md):
    # Regular expression pattern to find markdown contents
    # Regular expression pattern to find markdown table within markdown tags
    pattern = r'```markdown\n(.*?)\n```'
    
    # Finding the markdown table
    extracted_table = re.search(pattern, response_md, re.DOTALL)

    
    # 提取文本中 ```markdown ``` 中的内容
    extracted_content = extracted_table.group(1) if extracted_table else "No markdown table found"
    if extracted_content != "No markdown content found":
        df = transcribe_md_table_to_csv(extracted_content)
        return df
    else:
        return None

def transcribe_md_table_to_csv(md_table):
    # csv_table = '\n'.join([line.strip('|').replace('|', ';') for line in md_table.strip().split('\n')])
    
    # # delete the second line
    # csv_table = '\n'.join(csv_table.split('\n')[1:])
    # csv_file = StringIO(csv_table)
    # df = pd.read_csv(csv_file, delimiter=';')
        # Splitting the markdown table into lines
    lines = md_table.strip().split('\n')

    # Filtering out the separator line (which contains a series of '-')
    filtered_lines = [line for line in lines if not set(line.strip()).issubset({'|', '-', ' '})]

    # Converting the filtered lines to CSV format
    csv_table = '\n'.join([line.strip('|').replace('|', '\t') for line in filtered_lines])
    
    # Creating a DataFrame from the CSV-formatted string
    csv_file = StringIO(csv_table)
    df = pd.read_csv(csv_file, delimiter='\t')

    return df

    
def get_page_number(pdf_path):
    with open(pdf_path, 'rb') as file:
        return sum(1 for _ in PDFPage.get_pages(file))

def extract_full_text_from_pdf(pdf_path):
    all_text = []
    for page_number, page_layout in enumerate(extract_pages(pdf_path), start=1):
        # print(f"Page {page_number}:")
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                # print(element.get_text())
                all_text.append(element.get_text())
    
    # # save the first page text
    # base_dir = os.path.dirname(pdf_path)
    # pdf_name = os.path.basename(pdf_path)
    # if not os.path.exists(base_dir + '/text'):
    #     os.makedirs(base_dir + '/text')
    # with open(f'{base_dir}/text/{pdf_name[:-4]}_all_pages.txt', 'w', encoding='utf-8') as f:
    #     f.write('\n'.join(all_text))
    # print(f'Save the first page text in {base_dir}/text/{pdf_name[:-4]}_all_pages.txt')
    
    return '\n'.join(all_text)

                
                
def read_SI(SI_path):
    # base_dir = os.path.dirname(pdf_path)
    # pdf_name = os.path.basename(pdf_path)[0:-4]
    # SI_path = f'{base_dir}/SI/{pdf_name}_SI.pdf'

    # references_pages = [] # 2024-01-12 记录，SI最好全部读取，不然会有问题
    # references_pages = find_pages(pdf_path, 'References|Notes and references|Acknowledgements|ACKNOWLEDGMENTS|REFERENCES|References and notes')
    # if len(references_pages) > 0:
    #     min_ref_page = min(references_pages)
    # else:
    #     # 如果没有参考文献，就用最后一页
    #     min_ref_page = get_page_number(pdf_path)
    
    if os.path.exists(SI_path):
        SI_text = extract_full_text_from_pdf(SI_path)
        # SI_text = extract_text_by_page_and_paragraph(SI_path,min_ref_page)
        # print(f"Save SI text in {base_dir}/SI/text/{pdf_name}_SI_all_pages.txt")
        
        return SI_text
        
    else:
        print(f"No SI in {SI_path}")
        return None

def gather_article_SI_table(pdf_path):
    # base_dir = os.path.dirname(pdf_path)
    # pdf_name = os.path.basename(pdf_path)[0:-4]

    all_text = []
    # read article text
    article_text = open(f'{base_dir}/text/{pdf_name}_all_pages.txt', 'r', encoding='utf-8').read()
    all_text.append(article_text)
    
    # 是否有table,查看images/下是否有pdf_name_tabel_page_*.md的文件
    dir_files = os.listdir(f'{base_dir}/images')
    table_all = []
    for file in dir_files:
        if file.endswith('.md') and file.startswith(f'{pdf_name}_table_page_'):
            file_md = open(f'{base_dir}/images/{file}', 'r', encoding='utf-8').read()
            table_all.append(file_md)
    table_text = '\n'.join(table_all)
    all_text.append(table_text)
    
    # 是否有SI
    if os.path.exists(f'{base_dir}/SI/{pdf_name}_SI.pdf'):
        SI_path = f'{base_dir}/SI/{pdf_name}_SI.pdf'
        SI_text = open(f'{base_dir}/SI/text/{pdf_name}_SI_all_pages.txt', 'r', encoding='utf-8').read()
        all_text.append(SI_text)
    else:
        print(f"No SI in {pdf_path}")
    
    # save all text
    if not os.path.exists(base_dir + '/summary'):
        os.makedirs(base_dir + '/summary')
    with open(f'{base_dir}/summary/{pdf_name}_article_SI_table.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_text))
    print(f'Save all text in {base_dir}/summary/{pdf_name}_article_SI_table.txt')
    
    return '\n'.join(all_text)

def get_all_pdfs(dir_path):
    
    if not os.path.exists('./pdfs.csv'):
        pdfs = []
        pdf_dirs = []

        pdf_dir = os.path.join(dir_path, 'pdf')
        for file in os.listdir(pdf_dir):
            if file.endswith('.pdf'):
                pdfs.append(os.path.join(pdf_dir, file).replace("\\", "/"))
                pdf_dirs.append([pdf_dir, file])
        pdfs_df = pd.DataFrame()
        pdfs_df['pdf_path'] = pdfs
        pdfs_df['pdf_dir'] = [pdf_dir[0].replace("\\", "/") for pdf_dir in pdf_dirs]
        pdfs_df['pdf_name'] = [pdf_dir[1].replace("\\", "/") for pdf_dir in pdf_dirs]

        pdfs_df.to_csv('./pdfs.csv', index=False)
    else:
        pdfs_df = pd.read_csv('./pdfs.csv')
        
    return pdfs_df


def find_pages(pdf_path, keyword):
    doc = fitz.open(pdf_path)
    pages_with_keyword = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        if re.search(keyword, text, re.IGNORECASE):
            pages_with_keyword.append(page_num + 1)  # 页码从1开始

    doc.close()
    return pages_with_keyword

#  get picture from pdf of pages
def get_pic_from_pdf(pdf_path,pages):
    

    
    # dpi 参数控制图像质量，数值越高，质量越好，但文件大小也越大
    images = convert_from_path(pdf_path, dpi=300)
    images = [images[i-1] for i in pages] # 从1开始
    
    # # 保存图片
    # images_path = []
    # for i, image in enumerate(images):
    #     page_i = pages[i]
    #     image.save(f'{pdf_dir}/images/{pdf_name[:-4]}_table_page_{page_i+1}.jpg', 'JPEG')
    #     images_path.append(f'{pdf_dir}/images/{pdf_name[:-4]}_table_page_{page_i+1}.jpg')
    # print(f"Save table images in {pdf_dir}/images/{pdf_name[:-4]}_table_page_*.jpg")
    
    return images
    # # 保存图片
    # for i, image in enumerate(images):
    #     image.save(f'page_{i}.jpg', 'JPEG')

def extract_text_from_page(pdf_path, page_number=1):
    the_first_page_text = []
    for current_page_number, page_layout in enumerate(extract_pages(pdf_path), start=1):
        if current_page_number == page_number:
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    # print(element.get_text())
                    the_first_page_text.append(element.get_text())
    # save the first page text
    # base_dir = os.path.dirname(pdf_path)
    # pdf_name = os.path.basename(pdf_path)
    # if not os.path.exists(base_dir + '/text'):
    #     os.makedirs(base_dir + '/text')
    # with open(f'{base_dir}/text/{pdf_name[:-4]}_page1.txt', 'w', encoding='utf-8') as f:
    #     f.write('\n'.join(the_first_page_text))
    # print(f'Save the first page text in {base_dir}/text/{pdf_name[:-4]}_page1.txt')
    return '\n'.join(the_first_page_text)
                    
def extract_text_by_page_and_paragraph(pdf_path,min_ref_page):
    all_pages_text = []
    for page_number, page_layout in enumerate(extract_pages(pdf_path), start=1):
        # print(f"Page {page_number}:")
        if page_number <= min_ref_page:
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    # print(element.get_text())
                    all_pages_text.append(element.get_text())    
    # # save all pages text
    # base_dir = os.path.dirname(pdf_path)
    # pdf_name = os.path.basename(pdf_path)
    # if not os.path.exists(base_dir + '/text'):
    #     os.makedirs(base_dir + '/text')
    # with open(f'{base_dir}/text/{pdf_name[:-4]}_all_pages.txt', 'w', encoding='utf-8') as f:
    #     f.write('\n'.join(all_pages_text))
    # print(f'Save all pages text in {base_dir}/text/{pdf_name[:-4]}_all_pages.txt')
    return '\n'.join(all_pages_text)

def extract_table_text(api_key,images_path,update_status):
    r_all = []
    if len(images_path) > 0:
        update_status.text("Call GPT-4 Vision API...")
        # answers_csv = []
        for image_path in images_path:
            # base_dir = os.path.dirname(image_path)
            # image_name = os.path.basename(image_path)
            
            r = use_gpt_4v(image_path,api_key=api_key)
            
            # answers_csv.append([image_path,r])
            
            if r.startswith('Yes'):
                update_status.text(f"Table in {image_path}")
                # save table text
                # with open(f'{base_dir}/{image_name[:-4]}.md', 'w', encoding='utf-8') as f:
                #     f.write(r[4:])
                r_all.append(r[4:])
            else:
                print(f"No table in {image_path}")
        return r_all
            # save answers_csv to base_dir
        # answers_csv = pd.DataFrame(answers_csv,columns=['image_path','answers'])
        # answers_csv.to_csv(f'{base_dir}/answers.csv', index=False)
    
    else:
        update_status.text("No table in this pdf")
    
    
if __name__ == '__main__':

    pdfs_df = get_all_pdfs('../pdfs')
    
    
    for pdf_path in pdfs_df['pdf_path'][:1]:
        pdf_name = pdf_path.split('/')[-1]
        print('Process #:',pdf_path)

        tables_pages = find_pages(pdf_path, r'\bTable\b')
        # save table pages in pdfs_df[pdf_path]
        pdfs_df.loc[pdfs_df['pdf_path'] == pdf_path, 'tables_pages'] = str(tables_pages)
        print(f"Page number of tables: {tables_pages}")
        table_images = get_pic_from_pdf(pdf_path,tables_pages)
        
        # 查找参考文献所在页码
        references_pages = find_pages(pdf_path, 'References|Notes and references|Acknowledgements|ACKNOWLEDGMENTS|REFERENCES|References and notes')
        print(f"Page number of references: {references_pages}")
        min_ref_page = min(references_pages)
        # save min_ref_page in pdfs_df[pdf_path]
        pdfs_df.loc[pdfs_df['pdf_path'] == pdf_path, 'min_ref_page'] = min_ref_page
    
        # 提取第1页的文本
        page1_text = extract_text_from_page(pdf_path,min_ref_page)
        all_pages_text = extract_text_by_page_and_paragraph(pdf_path,min_ref_page)

        # extract table use gpt4v
        api_key = 'sk-syc0O7aRswVlTFJAQVaEJhGqI2TxLP2Tad64g2DNJuJpB0aX'
        extract_table_text(api_key,table_images)
        
        # 
        
        # save page1


    
    
    
    



