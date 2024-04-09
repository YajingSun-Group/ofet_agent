#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   gather_all.py
@Time    :   2024/01/12 19:53:19
@Author  :   Zhang Qian
@Contact :   zhangqian.allen@gmail.com
@License :   Copyright (c) 2024 by Zhang Qian, All Rights Reserved. 
@Desc    :   None
"""

# here put the import lib
import os 
import pandas as pd
from utils import process_response_md


# gather all tables in pdfs
def gather_all_tables(pdfs_path):
    # gather all tables in pdfs
    dirs = os.listdir(pdfs_path)

    columns = ['Organic Semiconductor Layer', 'Fabrication Method', 'Organic Layer Thickness', 'OFET Device Fabrication Details', 'Source Electrodes', 'Drain Electrodes', 'Dielectric Layer', 'Dielectric Layer Thickness', 'Gate Electrode', 'Device Geometries', 'Test Atmosphere', 'On-to-Off Current Ratios (I_on/I_off)', 'Threshold Voltage', 'Conduction Type', 'Mobility']

    for dir_ in dirs[8:]:
        print(f'processing {dir_}...')
        dir_tables = pd.DataFrame()
        response_dir = f'{pdfs_path}/{dir_}/pdf/response'
        if os.path.exists(response_dir):
            # find all xlsx files in response_dir
            response_files = os.listdir(response_dir)
            response_files = [f for f in response_files if f.endswith('.xlsx')]
            # read all xlsx files
            for response_file in response_files:
                response_df = pd.read_excel(f'{response_dir}/{response_file}')
                # 去除空列
                response_df = response_df.dropna(axis=1,how='all')
                if response_df.shape[1] == len(columns):
                    response_df.columns = columns
                    response_df['pdf'] = response_file[:-5] + '.pdf'
                    response_df['dir'] = dir_
                    dir_tables = dir_tables.append(response_df)
                    continue
                if response_df.shape[1] == 16:
                    # 只要前15列
                    response_df = response_df.iloc[:,:15]
                    # rename columns
                    response_df.columns = columns
                    # add pdf_name column and base_dir name column
                    response_df['pdf'] = response_file[:-5] + '.pdf'
                    response_df['dir'] = dir_
                    
                    # append to dir_tables
                    dir_tables = dir_tables.append(response_df)
                else:
                    # 重新提取目录下的md文件，重新保存成xlsx文件
                    response_md = open(f'{response_dir}/{response_file[:-5]}.md', 'r',encoding='utf-8').read()
                    response_df = process_response_md(response_md)
                    response_df.to_excel(f'{response_dir}/{response_file}',index=False)
                    print('Error: ',response_file)
                    print('Response file mardown:',open(f'{response_dir}/{response_file[:-5]}.md', 'r',encoding='utf-8').read())
                    print('response_df.columns:',response_df.columns,'response_df.shape[1]:',response_df.shape[1],'len(columns):',len(columns))
                    print(f'{response_dir}/{response_file} columns number not equal to columns')
                    raise Exception(f'{response_file} columns number not equal to columns')
        else:
            print(f'{dir_} has no response dir')
            raise Exception(f'{dir_} has no response dir')
        # save dir_tables to excel
        print(f'saving {dir_} to excel...')
        dir_tables.to_excel(f'{pdfs_path}/{dir_}/gpt4V_outputs.xlsx',index=False)
        
pdfs = '../完毕'
gather_all_tables(pdfs)



