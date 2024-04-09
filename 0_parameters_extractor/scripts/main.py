
from utils import *
from gptapi import *
import time
 
def make_print_to_file(path='./'):
    '''
    path， it is a path for save your log about fuction print
    example:
    use  make_print_to_file()   and the   all the information of funtion print , will be write in to a log file
    :return:
    '''
    import sys
    import os
    import sys
    import datetime
 
    class Logger(object):
        def __init__(self, filename="Default.log", path="./"):
            self.terminal = sys.stdout
            self.path= os.path.join(path, filename)
            self.log = open(self.path, "a", encoding='utf8',)
            print("save:", os.path.join(self.path, filename))
 
        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)
 
        def flush(self):
            pass


 
    fileName = datetime.datetime.now().strftime('day'+'%Y_%m_%d')
    sys.stdout = Logger(fileName + '.log', path=path)

    print(fileName.center(60,'*'))



if __name__ == '__main__':
    
    # log file
    make_print_to_file(path='./')
    
    pdfs_df = get_all_pdfs('../examples')
     
    api_key = 'Your OPENAI API KEY'
    
    for i_pdf, pdf_path in enumerate(pdfs_df['pdf_path']): 
        tic = time.time()
        print('Start time:',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        pdf_name = pdf_path.split('/')[-1]
        print(f'Process #{i_pdf}:',pdf_path)

        tables_pages = find_pages(pdf_path, r'\bTable\b')
        # save table pages in pdfs_df[pdf_path]
        pdfs_df.loc[pdfs_df['pdf_path'] == pdf_path, 'tables_pages'] = str(tables_pages)
        print(f"Page number of tables: {tables_pages}")
        table_images = get_pic_from_pdf(pdf_path,tables_pages)
        
        # 查找参考文献所在页码
        references_pages = find_pages(pdf_path, 'References|Notes and references|Acknowledgements|ACKNOWLEDGMENTS|REFERENCES|References and notes')
        print(f"Page number of references: {references_pages}")
        if len(references_pages) > 0:
            min_ref_page = min(references_pages)
        else:
            # 如果没有参考文献，就用最后一页
            min_ref_page = get_page_number(pdf_path)
        # save min_ref_page in pdfs_df[pdf_path]
        pdfs_df.loc[pdfs_df['pdf_path'] == pdf_path, 'min_ref_page'] = min_ref_page
    
        # 提取第1页的文本
        page1_text = extract_text_from_page(pdf_path)
        all_pages_text = extract_text_by_page_and_paragraph(pdf_path,min_ref_page)

        # extract table use gpt4v
       
        print('extracting table information use gpt4v...')
        extract_table_text(api_key,table_images)
        
        
        # 读取SI文献
        print('reading SI...')
        SI_text = read_SI(pdf_path)
        
        all_text = gather_article_SI_table(pdf_path)
        print('all text gathered')
        
        
        # use gpt 4 to extract table
        print('extracting OFET table use gpt4...')
        base_dir = os.path.dirname(pdf_path)
        if not os.path.exists(f'{base_dir}/response/{pdf_name[:-4]}.md'):
            response_md = use_gpt_4(api_key=api_key,input_information=all_text)
        
            # save response_md to response dir
            if not os.path.exists(f'{base_dir}/response'):
                os.makedirs(f'{base_dir}/response')
            with open(f'{base_dir}/response/{pdf_name[:-4]}.md', 'w', encoding='utf-8') as f:
                f.write(response_md)
        else:
            print('response file already exists')
            response_md = open(f'{base_dir}/response/{pdf_name[:-4]}.md', 'r',encoding='utf-8').read()
        
        table_df = process_response_md(response_md)
        # save table_df to excel
        table_df.to_excel(f'{base_dir}/response/{pdf_name[:-4]}.xlsx',index=False)
        
        toc = time.time()
        print('End Time:',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print('Spend time(s):',toc-tic)
        
        print('*'*50)
        print('\n')

