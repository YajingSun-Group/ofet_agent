import streamlit as st
import pandas as pd
# from tabula import read_pdf
from tempfile import NamedTemporaryFile
import time
import pickle
import numpy as np
# import shap
st.title('🎯OFET Performance Predictor')


# load pickle
with open('enc.pkl', 'rb') as f:
    enc = pickle.load(f)


def update_status(message):
    # 使用这个函数来更新状态信息
    status_text.text(message)


# update_status(enc.categories_)

column_name = ['Semiconductor Category','Fabrication Method Category','Source Electrodes Category','Drain Electrodes Category','Gate Electrode Category','Dielectric Layer Category','Device Geometries Category','Conduction Type Category','Test Atmosphere Category','Publication Year']
# 合并
options_list = enc.categories_
# default options
default_options = ['Chalcogen-Containing Heterocyclic Semiconductors',
       'Vacuum Techniques', 'Gold', 'Gold', 'Indium Tin Oxide',
       'Pure SiO2', 'TGBC', 'p-type', 'Air Environment', 2021]
default_index = [2,3,7,8,4,3,2,2,0,4]


user_input = st.text_input('Please enter SMILES of semiconductor material:', 'c1ccc(-c2cc3sc4cc(-c5ccccc5)sc4c3s2)cc1')
if user_input:
    st.write(f'You entered: {user_input}')
else:
    st.error('Please enter a valid SMILES.') 
    
# 用于存储每个选择框的用户选择
user_choices = []
user_choices.append(user_input)
# 使用循环为每组选项创建一个选择框
for i, options in enumerate(options_list, start=0):
    choice = st.selectbox(f'Choose an option for {column_name[i]}:', options, index = default_index[i])
    user_choices.append(choice)

# 选择完成后，显示所有用户的选择
# st.write("Your choices are:")
# st.write()
# for i, choice in enumerate(user_choices, start=0):
#     st.write(f"{column_name[i]}: {choice}")
# 转换最后一个为整数
user_choices[-1] = int(user_choices[-1])
st.write("Your choices are:")
st.write(user_choices)
df = pd.DataFrame([user_choices])


status_text = st.empty()


# encoder
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
from rdkit.Chem import MACCSkeys
from rdkit.Chem import Descriptors

def smiles2maccs(smiles):
    mol = Chem.MolFromSmiles(smiles)
    fp = MACCSkeys.GenMACCSKeys(mol)
    arr = np.zeros((1,))
    DataStructs.ConvertToNumpyArray(fp, arr)
    return arr

def smiles2morgan(smiles):
    mol = Chem.MolFromSmiles(smiles)
    info = {}
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 8, nBits=2048,bitInfo=info)
    arr = np.zeros((1,))
    DataStructs.ConvertToNumpyArray(fp, arr)
    return arr, info





# 当用户点击"Extract"按钮时执行
if st.button('Predict'):
    update_status("Program is running...")
    # update_status(f"{uploaded_file1} {uploaded_file2}")
    device_features = enc.transform(np.array(user_choices[1:],dtype=object).reshape(1,-1)).toarray()[0].tolist()

    # st.write(device_features)

    smiles = user_choices[0]
    morgan_fp, morgan_info = smiles2morgan(smiles)
    material_features = list(smiles2maccs(smiles))+list(morgan_fp)

    input_features = material_features + device_features
    
    input_features = np.array(input_features).reshape(1,-1)
    
    update_status('Material features has been featuried done...')
    # st.write(len(input_features))
    
    
    import joblib
    xgb_clf = joblib.load('maccs_morgan_xgb_clf.pkl')
    update_status('Machine learning model has been loaded...')

    # 预测
    y_pred = xgb_clf.predict(np.array(input_features))
    update_status('Prediction has been done...')
    
    if y_pred[0]==0:
        predict_label= "Low Mobility"
    else:
        predict_label= "High Mobility"

    
    output_information = f"""
    ### ⭐Predict Result:
        The predictited label is {predict_label}
    
    """
    
    st.write(output_information)
    # 显示程序已经运行完毕
    update_status('All done! 🎉🎉🎉')

    
    # 展示提取的表，标题为提取的表格
    st.markdown('### 📊 Feature Importance Analysis')
    
    with open("shap_explainer.pkl", "rb") as f:
        explainer = pickle.load(f)
    
    update_status('SHAP explainer is loaded...')

    # update_status(explainer.base_values)
    import shap
    import matplotlib.pyplot as plt
    st.set_option('deprecation.showPyplotGlobalUse', False)



    
    features_names = np.load('features_names.npy',allow_pickle=True)
    input_features_df = pd.DataFrame(input_features,columns=features_names)
    
    s_values = explainer(input_features_df)

    # impotances = explainer.shap_values(input_features)
    
    cat_shap_values = s_values[:,167+2048:]
    
    morgan_shap_values = s_values[:,167:167+2048][0].values
    # st.write('Morgan shap values:',morgan_shap_values.shape)

    morgan_shap_values = {bit: morgan_shap_values[bit] for bit in range(2048)}
    # st.write('Morgan shap values:',morgan_shap_values)

    # status_text(morgan_shap_values)
    # 确保将绘图指令定向到刚创建的Axes对象上
    # fig, ax = plt.subplots()
    

    st.write('##### 1. Material Morgan Features Importance:')
    from rdkit.Chem.Draw import SimilarityMaps
    mol = Chem.MolFromSmiles(smiles)
    # info = {}
    # fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=8, nBits=2048, bitInfo=info)
    atom_contributions = np.zeros((mol.GetNumAtoms(),), dtype=np.float32)
    for bit, contrib in morgan_shap_values.items():
        if bit in morgan_info:  # 检查该位是否在bitInfo中
            for atom_idx, _ in morgan_info[bit]:
                atom_contributions[atom_idx] += contrib  # 累加贡献度到相关的原子
    # 可视化原子贡献度
    # fig, ax = plt.subplots(figsize=(6, 6))
    SimilarityMaps.GetSimilarityMapFromWeights(mol, [float(x) for x in atom_contributions], colorMap='RdBu', 
                                            #    fig=fig,
                                               alpha=0.7
                                               )
    st.pyplot()

    st.write('##### 2. Device Features Importance:')
    shap.plots.force(cat_shap_values, features=input_features_df.iloc[:,167+2048:],matplotlib=True, show=False)
    st.pyplot()

    st.write('##### 3. All Features Importance:')
    shap.plots.bar(s_values[0], show=False)
    st.pyplot()

    # 现在，使用st.pyplot()时传入figure对象

    update_status('All done! 🎉🎉🎉')

    

     

