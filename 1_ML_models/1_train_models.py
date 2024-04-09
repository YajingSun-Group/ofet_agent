# 划分数据集

from models import run_all_test
import numpy as np

features1 = np.load('data/features1.npy')
features2 = np.load('data/features2.npy')
features3 = np.load('data/features3.npy')
features_cat_onehot = np.load('data/features_cat_onehot.npy')
train_index = np.load('data/under_sample_index.npy')
test_index = np.load('data/under_sample_index.npy')

labels = np.load('data/labels.npy')


# macss特征

scores_maccs = run_all_test(features1,labels, train_index, test_index,'maccs')

print(scores_maccs)

# moragn特征

scores_moargn = run_all_test(features2,labels, train_index, test_index,'morgan')
print(scores_moargn)

# macss和morgan特征

scores_maccs_morgan = run_all_test(features3,labels, train_index, test_index,'maccs_morgan')
print(scores_maccs_morgan)

# 只有类别特征

scores_cat = run_all_test(features_cat_onehot,labels, train_index, test_index,'cat')




