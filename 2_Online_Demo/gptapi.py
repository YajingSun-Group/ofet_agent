import requests
import openai
import base64
import os
import time
from io import BytesIO

current_date = time.strftime("%Y-%m-%d", time.localtime())

def get_image_base64(image):
    """将PIL图像转换为Base64编码的字符串"""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  # 或PNG
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def use_gpt_4v(image_path,api_key):
    
    base64_image = get_image_base64(image_path)
        
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
        
        response = requests.post("https://api.chatanywhere.com.cn/v1/chat/completions", headers=headers, json=payload)
    except:
        print("Error: API request failed, sleep 30s or longer, retrying...")
        time.sleep(30)
    
    if response.status_code != 200:
        print(response.text)
        print('sleep 60s.....')
        time.sleep(60)
        response = requests.post("https://api.chatanywhere.com.cn/v1/chat/completions", headers=headers, json=payload)
    else:
        response = response.json()
        answers = response.get('choices')[0].get('message').get('content')
        return answers


def use_gpt_4(api_key,input_information):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}
   
    payload = {
        "model": "gpt-4-0125-preview",
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
You are an AI assistant specializing in extracting and organizing key data from Organic Field-Effect Transistor (OFET) research articles. Your task is to parse provided literature and format the findings into a detailed markdown table. This table should accurately reflect the nuances in OFET fabrication processes, including variations in materials, methods, and testing atmospheres, ensuring each variant in the fabrication process, such as differing test atmospheres, is represented on separate rows. This table should provide a clear, organized representation of OFET fabrication processes and variations. Your output should be a markdown table directly showcasing this structured information, without additional commentary.

# Spreadsheet Requirements
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
- Clearly separate rows for each unique combination of organic layer, fabrication method, or testing condition to reflect the full range of experimental setups.
- Utilize "N/A" to denote unavailable or inapplicable data points.
- Focus on key elements affecting device performance while omitting general electrode synthesis and substrate details, unless directly relevant.
- Distinguish rows for individual components or units rather than merging information within a single cell to ensure clarity.
- When presented with multiple or range values for mobility, record only the highest value, adding a note for significant ranges to highlight their impact on material performance.
- Emphasize precise chemical formulas or detailed names for organic layers over vague descriptions to enhance specificity.
- Infer device geometries from the context if not explicitly mentioned, defaulting to BGTC when in doubt, and adjust based on information available.
- Aim for the markdown table to serve as an accurate, comprehensive representation of the diverse data encountered in OFET research.

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
    api_key = 'sk-syc0O7aRswVlTFJAQVaEJhGqI2TxLP2Tad64g2DNJuJpB0aX'
    # r = use_gpt_4v("../1_table_page_7.jpg",api_key=api_key)
    input_information = open('../pdfs/JACS/pdf/summary/1_article_SI_table.txt', 'r',encoding='utf-8').read()
    r = use_gpt_4(api_key=api_key,input_information=input_information)
    print(r)


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
阅读以下OFET的制备文献，回答OFET的构型属于以下什么类型：
Bottom gate, bottom contact (BGBC)
Bottom gate, top contact (BGTC)
Top gate, bottom contact (TGBC)
Top gate, top contact (TGTC)

经过你的推理，请只回复属于哪种类型，不需要回复其他的信息。
你的回复格式：
{文献中OFET的类型}

OFET文献：

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
请阅读以下OFET制备的文献，回答OFET的半导体类型属于以下三种的哪一种：p-type, n-type, Ambipolar

你的回复格式:
{半导体类型}

OFET文献：

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
    api_key = 'sk-syc0O7aRswVlTFJAQVaEJhGqI2TxLP2Tad64g2DNJuJpB0aX'
    # r = use_gpt_4v("../1_table_page_7.jpg",api_key=api_key)
    input_information = open('../pdfs/JACS/pdf/summary/1_article_SI_table.txt', 'r',encoding='utf-8').read()
    r = use_gpt_4(api_key=api_key,input_information=input_information)
    print(r)