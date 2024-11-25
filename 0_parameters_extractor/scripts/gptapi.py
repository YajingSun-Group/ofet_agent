import requests
import openai
import base64
import os
import time

current_date = time.strftime("%Y-%m-%d", time.localtime())
base_url = 'https://api.openai.com/v1/chat/completions'
# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def use_gpt_4v(image_path,api_key):
    
    base64_image = encode_image(image_path)
        
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {"role": "system", "content":f"""
You are ChatGPT, a large language model trained by OpenAI.
Knowledge cutoff: 2023-04
Current date: {current_date}
"""
                },
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": """
Read the uploaded image, which is taken from an academic literature piece concerning Organic Field-Effect Transistors (OFETs). The image might include text, diagrams, figures, and tables pertinent to the study of OFETs. Your task is to identify whether a table is present in the image. If a table is detected, respond with 'Yes' and transcribe the entire table including its title, header, body, and footer (or notes, if any) in Markdown format. If no table is found, respond with 'No'.

Response format:
{Yes or No}
{Table if applicable}
"""
            },
            {
                "type": "image_url",
                "image_url":{
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail":"high"
                }
            }
            ]
        }
        ]}
    try:
        response = requests.post(base_url, headers=headers, json=payload)
    except:
        print("Error: API request failed, sleep 30s or longer, retrying...")
        time.sleep(30)
    
    if response.status_code != 200:
        print(response.text)
        print('sleep 60s.....')
        time.sleep(60)
        response = requests.post(base_url, headers=headers, json=payload)
    else:
        response = response.json()
        answers = response.get('choices')[0].get('message').get('content')
        return answers


def use_gpt_4(api_key,input_information):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}
   
    payload = {
        "model": "gpt-4-1106-preview",
        "messages": [
            {"role": "system", "content":f"""
You are ChatGPT, a large language model trained by OpenAI.
Knowledge cutoff: 2023-04
Current date: {current_date}
"""
                },
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": """
# Task Description
You are an AI assistant with expertise in organic chemistry. Extract key data from the provided Organic Field-Effect Transistor (OFET) literature and automatically save it to a table in markdown format. The goal is to create a detailed and structured table that reflects the complexity and variations in the fabrication process of OFETs. Directly output the markdown table, don't say any other sentence.

# Excel Spreadsheet Requirements
- **File Format:** .xlsx
- **Column Headings:**
  a. Organic Semiconductor Layer
  b. Fabrication Method
  c. Organic Layer Thickness (nm)
  d. OFET Device Fabrication Details (including temperature, humidity, time, pressure, and so on.)
  e. Source Electrodes
  f. Drain Electrodes
  g. Dielectric Layer
  h. Dielectric Layer Thickness (nm)
  i. Gate Electrode
  j. Device Geometries (such as BGBC, TGBC, BGTC, TGTC)
  k. Test Atmosphere (e.g., air, vacuum, hydrogen, nitrogen)
  l. On-to-Off Current Ratios (I_on/I_off)
  m. Threshold Voltage
  n. Conduction Type (p-type, n-type, etc.)
  o. Mobility (cm²/Vs)
  p. Other important parameters and details

# Data Organization Guidelines
- Use separate rows for each distinct organic layer, fabrication method, or test condition combination.
- Indicate "N/A" for missing or uncertain data.
- Exclude details of electrode synthesis and substrate material, unless these are critical to the device's performance.
- Use distinct rows for multiple units/components instead of consolidating within a cell.
- If multiple mobility values or a range is given, record the highest value for each case. Add notes if the range is significant for understanding material properties under different conditions.
- Prioritize detailed names or chemical formulas of organic layers over generic descriptions.
- Infer device geometries based on context, especially when multiple geometries are involved. If unsure, default to the most common geometry, BGTC.
- Ensure the table you compile is a clear and accurate representation of the diverse information presented in the OFET literature.


# Response format
{Table in markdown format}
==============================================================
# Literature and tables:

""" + input_information
            }
            ]
        }
        ]}
    try:
        response = requests.post(base_url, headers=headers, json=payload)
    except:
        print("Error: API request failed, sleep 30s or longer, retrying...")
        time.sleep(30)
    
    if response.status_code != 200:
        raise Exception(response.text)
    else:
        response = response.json()
        answers = response.get('choices')[0].get('message').get('content')
        return answers


def use_gpt_4_get_category(api_key,input_information):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}
   
    payload = {
        "model": "gpt-4-1106-preview",
        "messages": [
            {"role": "system", "content":f"""
You are ChatGPT, a large language model trained by OpenAI.
Knowledge cutoff: 2023-04
Current date: {current_date}
"""
                },
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": """
#  Task Description
Your role as an AI specialist in Organic Field-Effect Transistors (OFETs) involves analyzing the abstract and introduction of an OFET research paper. Your analysis should focus on identifying:

a. The principal category of the organic semiconductor material presented in the research, among the following options: [Acenes, Chalcogen-Containing Heterocyclic Semiconductors, Nitrogen-Containing Heterocyclic Semiconductors, Halogen-Containing Semiconductors, Cyano-Containing Semiconductors, Carbonyl-Containing Semiconductors and Imide Derivatives, Fullerenes, Others].

b. The specific subclass within the 'Acenes' category, select from: ["Pyrene, Perylene, Coronene, and Other Fused Arenes", "Oligoacenes", "Other Aromatic Hydrocarbons"].

c. The precise subclass under 'Nitrogen-Containing Heterocyclic Semiconductors', choices include: ["Phthalocyanines and Porphyrins", "Azaacenes", "Oligomers Based on Nitrogen-Containing π Systems"].

Ensure that the response is direct and follows the specified format without additional commentary.

# Response format:
{Major Category}; {Subcategory or "N/A" if not applicable}

# Provided OFET Abstract and Introduction:

""" + input_information
            }
            ]
        }
        ]}
    try:
        response = requests.post(base_url, headers=headers, json=payload)
    except:
        print("Error: API request failed, sleep 30s or longer, retrying...")
        time.sleep(30)
    
    if response.status_code != 200:
        raise Exception(response.text)
    else:
        response = response.json()
        answers = response.get('choices')[0].get('message').get('content')
        return answers   




def use_gpt_4_get_geometries(api_key,input_information):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}
   
    payload = {
        "model": "gpt-4-1106-preview",
        "messages": [
            {"role": "system", "content":f"""
You are ChatGPT, a large language model trained by OpenAI.
Knowledge cutoff: 2023-04
Current date: {current_date}
"""
                },
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": """
Read the following literature on the preparation of OFETs and answer what type of OFET configurations belong to the following categories:
Bottom gate, bottom contact (BGBC)
Bottom gate, top contact (BGTC)
Top gate, bottom contact (TGBC)
Top gate, top contact (TGTC)

After your reasoning, please reply only to which type you belong to, and do not need to reply to other messages.

Format your response:

{Types of OFETs in the literature}

OFET Literature:

""" + input_information
            }
            ]
        }
        ]}
    try:
        response = requests.post("https://api.chatanywhere.com.cn/v1/chat/completions", headers=headers, json=payload)
    except:
        print("Error: API request failed, sleep 30s or longer, retrying...")
        time.sleep(30)
    
    if response.status_code != 200:
        raise Exception(response.text)
    else:
        response = response.json()
        answers = response.get('choices')[0].get('message').get('content')
        return answers   


def use_gpt_4_get_gate(api_key,input_information):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}
   
    payload = {
        "model": "gpt-4-1106-preview",
        "messages": [
            {"role": "system", "content":f"""
You are ChatGPT, a large language model trained by OpenAI.
Knowledge cutoff: 2023-04
Current date: {current_date}
"""
                },
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": """
Please read the following literature on OFET preparation and answer which of the three types of OFET semiconductors is: p-type, n-type, and ambipolar



Format your response:

{Semiconductor Type}



OFET Literature:

""" + input_information
            }
            ]
        }
        ]}
    try:
        response = requests.post("https://api.chatanywhere.com.cn/v1/chat/completions", headers=headers, json=payload)
    except:
        print("Error: API request failed, sleep 30s or longer, retrying...")
        time.sleep(30)
    
    if response.status_code != 200:
        raise Exception(response.text)
    else:
        response = response.json()
        answers = response.get('choices')[0].get('message').get('content')
        return answers   
    
if __name__ == '__main__':
    api_key = ''
    # r = use_gpt_4v("../1_table_page_7.jpg",api_key=api_key)
    input_information = open('../pdfs/JACS/pdf/summary/1_article_SI_table.txt', 'r',encoding='utf-8').read()
    r = use_gpt_4(api_key=api_key,input_information=input_information)
    print(r)