import streamlit as st
import pandas as pd
# from tabula import read_pdf
from tempfile import NamedTemporaryFile
import time
from utils import *
from gptapi import *

st.title('✨OFET Parameters Extractor')

def update_status(message):
    # 使用这个函数来更新状态信息
    status_text.text(message)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    # "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    # "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"


# 创建文件上传框
uploaded_file1 = st.file_uploader("Please upload the Paper", type="pdf")
uploaded_file2 = st.file_uploader("Please upload the Supporting Information", type="pdf")
status_text = st.empty()


# 当用户点击"Extract"按钮时执行
if st.button('Extract'):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    
    update_status("Program is running...")
    # update_status(f"{uploaded_file1} {uploaded_file2}")
    if uploaded_file1 is not None and uploaded_file2 is not None:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile1, NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile2:
            tmpfile1.write(uploaded_file1.getvalue())
            tmpfile2.write(uploaded_file2.getvalue())
            tables_pages = find_pages(tmpfile1, r'\bTable\b')
            update_status(f"Page number of tables: {tables_pages}")
            table_images = get_pic_from_pdf(tmpfile1.name,tables_pages)
            # # 显示图片
            # for i, image in enumerate(table_images):
            #     st.image(image, caption=f"Page {i+1}", use_column_width=True)
            
            references_pages = find_pages(tmpfile1.name, 'References|Notes and references|Acknowledgements|ACKNOWLEDGMENTS|REFERENCES|References and notes')
            update_status(f"Page number of references: {references_pages}")
            if len(references_pages) > 0:
                min_ref_page = min(references_pages)
            else:
                # 如果没有参考文献，就用最后一页
                min_ref_page = get_page_number(tmpfile1.name)
            
            page1_text = extract_text_from_page(tmpfile1.name)
            all_pages_text = extract_text_by_page_and_paragraph(tmpfile1.name,min_ref_page)
            # update_status(all_pages_text)
            
            print('extracting table information use gpt4v...')
            table_text = extract_table_text(openai_api_key,table_images,status_text)
            
            # 读取SI文献
            update_status('reading SI...')
            SI_text = read_SI(tmpfile2.name)
            
            # table_text 可能为空，所以需要判断一下
            if table_text is None:
                all_text = '\n'.join([all_pages_text,SI_text])
            else:
                all_text = '\n'.join([all_pages_text,SI_text,table_text])
            update_status('all text gathered')
                   # use gpt 4 to extract table
            update_status('Extracting OFET parameters using gpt4...')

            response_md = use_gpt_4(api_key=openai_api_key,input_information=all_text)

            # 显示程序已经运行完毕
            update_status('All done! 🎉🎉🎉')

            table_df = process_response_md(response_md)
            # update_status(table_df)
            # 将table_df转置，方便展示
            table_df = table_df.T
            
            # 展示提取的表，标题为提取的表格
            st.markdown('### 📊 Extracted Table of OFET Design Parameters')
            st.dataframe(table_df)
            
        # 临时保存上传的文件，以便tabula使用
        # with NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile1, NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile2:
        #     tmpfile1.write(uploaded_file1.getvalue())
        #     tmpfile2.write(uploaded_file2.getvalue())
        #     tables1 = extract_tables_from_pdf(tmpfile1.name)
        #     tables2 = extract_tables_from_pdf(tmpfile2.name)

        
        # 展示提取的表
        # 帮我随机生成三个表格
        # 帮我生成一个7行2列的表格
        # tables1 = [pd.DataFrame({'A': range(7), 'B': range(7)}) for _ in range(3)]
        
        # st.dataframe(tables1[0])

        # for i, table in enumerate(tables1, start=1):
        #     update_status(f"正在执行步骤 {i+1}...")
        #     st.write(f"第一个PDF文件 - 表格 {i}")
        #     st.dataframe(table)

        # for i, table in enumerate(tables2, start=1):
        #     st.write(f"第二个PDF文件 - 表格 {i}")
        #     st.dataframe(table)

        # TODO: 实现下载按钮逻辑，此部分需要根据提取的数据和期望的输出格式进一步实现
        # 由于Streamlit直接支持的功能有限，您可能需要将表格数据转换为CSV或Excel文件，然后使用st.download_button提供下载。
        # 例如，如果您已经将表格存储在Pandas DataFrame中，可以这样实现下载CSV的功能：
        # csv = tables1[0].to_csv(index=False)  # 假设您想下载第一个表格
        # st.download_button(label="下载表格为CSV", data=csv, file_name="table.csv", mime='text/csv')
    else:
        st.error("Please upload a file first.")
