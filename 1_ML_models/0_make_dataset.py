import pandas as pd
import numpy as np
import seaborn as sns
import os
import time

data = pd.read_excel('./OFET-summary4.xlsx')

# 迁移率大于1的为高迁移率，小于1的为低迁移率
labels = []
for i in data['Highest Mobility']:
    if i >= 1:
        labels.append(1)
    else:
        labels.append(0)

data['labels'] = labels

# 计算smiles的Morgan指纹
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
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 8, nBits=2048)
    arr = np.zeros((1,))
    DataStructs.ConvertToNumpyArray(fp, arr)
    return arr

# 计算指纹

data['maccs'] = data['smiles'].apply(smiles2maccs)
data['morgan'] = data['smiles'].apply(smiles2morgan)

features = data[['smiles','maccs','morgan','major_category','Fabrication Category','Source Electrodes Category','Drain Electrodes Category','Gate Electrode Category','Dielectric Layer Category','Device Geometries Category','Conduction Type Category','Test Atmosphere Category','publication_year','labels','pdf','dir','Highest Mobility']]

# 去除空值
features = features.dropna(axis=0, how='any')


# 统计labels的数量
features['labels'].value_counts()

# 重置索引
features = features.reset_index(drop=True)

# 实行欠采样，使得两类样本数量相同
# 高迁移率的样本数量
n_high = features['labels'].value_counts()[1]
# 低迁移率的样本数量
n_low = features['labels'].value_counts()[0]

# 高迁移率的索引
high_index = features[features['labels'] == 1].index.tolist()
# 低迁移率的索引
low_index = features[features['labels'] == 0].index.tolist()

# 
# 设置随机种子
np.random.seed(1929)

# 随机选择低迁移率的样本
random_low_index = np.random.choice(low_index, n_high, replace=False)

# 合并索引
under_sample_index = np.concatenate([high_index, random_low_index])

# 根据索引获取数据
under_sample_data = features.loc[under_sample_index]

# 重置索引
under_sample_data = under_sample_data.reset_index(drop=True)

# 对除了smiles，maccs，morgan，labels以外的特征进行one-hot编码

# 获取除了smiles，maccs，morgan，labels以外的特征
features_cat = features.drop(['smiles','maccs','morgan','labels','pdf','dir','Highest Mobility'], axis=1)

# 对特征进行one-hot编码
from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder()
features_cat_onehot = enc.fit_transform(features_cat).toarray()


# 统计features_cat每一列的不同值的数量
n_values = []
for i in range(features_cat.shape[1]):
    n_values.append(len(features_cat.iloc[:,i].value_counts()))
print(n_values)


# 将maccs和morgan转换为array
features_maccs = np.array(features['maccs'].tolist())
features_morgan = np.array(features['morgan'].tolist())

# 将macss和其他特征合并
features1 = np.hstack((features_maccs, features_cat_onehot))

# 将morgan和其他特征合并
features2 = np.hstack((features_morgan, features_cat_onehot))

# 将macss和morgan和其他特征合并
features3 = np.hstack((features_maccs, features_morgan, features_cat_onehot))

# mkdir data
if not os.path.exists('./data'):
    os.mkdir('./data')
    
# save features
np.save('./data/features1.npy', features1)
np.save('./data/features2.npy', features2)
np.save('./data/features3.npy', features3)
np.save('./data/features_cat_onehot.npy', features_cat_onehot)

# save under_sample_index
np.save('./data/under_sample_index.npy', under_sample_index)

# 保存enc
import pickle
with open('enc.pkl', 'wb') as f:
    pickle.dump(enc, f)

# 划分数据集
from sklearn.model_selection import train_test_split

# 划分索引
train_index, test_index = train_test_split(under_sample_index, test_size=0.2, random_state=42,stratify=features.loc[under_sample_index]['labels'])

# save train_index, test_index
np.save('./data/train_index.npy', train_index)
np.save('./data/test_index.npy', test_index)


# save labels
np.save('./data/labels.npy', features['labels'].values)




