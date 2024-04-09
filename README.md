# LLM-Based AI Agent for Organic Semiconductor Devices Research

<img src="\Fig1.jpg" alt="Fig1" style="zoom: 25%;" />

An artificial intelligence agent for enhancing organic field-effect transistors (OFETs) performance by combining GPT-4 with advanced machine learning algorithms is presented. It efficiently extracts OFET experimental data from extensive literature and gives intelligent suggestions for OFET fabrication. 

## Installation

```sh
git clone https://github.com/YajingSun-Group/ofet_agent.git
cd ofet_agent
```

For anaconda, create a new python environment:

```sh
conda create -n ofet_agent python=3.8.8
```

### Requirement

For **0_parameters_extractor** using LLMs:

```
openai=1.10.0
habanero = 1.2.3
tiktoken  
PyMuPDF
pdf2image
pdfminer
pandas
numpy
```

For **1_ML_modes**:

```
rdkit=2023.9.5
shap=0.44.1
xgboost=2.0.3
scikit-learn=1.3.2
```

For **2_Online_demo**:

```sh
cd 2_Online_demo
pip install -r requirements.txt
```

For **3_Other_tools**:

For journal_information_extractor, you can just install the 

For DECIMER, please read the [official latest reponsity](https://github.com/Kohulan/DECIMER-Image-Segmentation).

### Getting started

For parameters extractor:

```
cd 0_paramters_extractor/scripts

# add OpenAI key in main.py
# add PDF file in pdf/
# add SI file in pdf/SI/

python main.py
```

For 1_ML_models:

```
cd 1_ML_models

python 0_make_dataset.py
python 1_train_models.py
```

### Online demo

You can try our model in [Online-Demo site](https://ofet-v1.streamlit.app/). It requires an OpenAI key (For more information, visit the OpenAI site). In online demo, information extractor, performance predictor and lab advisor are available.

<img src="\demo.jpg" alt="demo" style="zoom: 25%;" />



