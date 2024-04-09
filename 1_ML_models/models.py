import time
import os
import pandas as pd
# 构造打印的函数
from sklearn.metrics import accuracy_score, precision_recall_curve, precision_score, recall_score, f1_score, roc_auc_score, classification_report, roc_curve
import numpy as np

def print_result(y_test, y_pred):
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    print('accuracy_score:', accuracy_score(y_test, y_pred))
    print('precision_score:', precision_score(y_test, y_pred))
    print('recall_score:', recall_score(y_test, y_pred))
    print('f1_score:', f1_score(y_test, y_pred))
    print('roc_auc_score:', roc_auc_score(y_test, y_pred))

# 打印混淆矩阵
def print_confusion_matrix(y_test, y_pred):
    from sklearn.metrics import confusion_matrix
    print(confusion_matrix(y_test, y_pred))

# 打印分类报告
def print_classification_report(y_test, y_pred):
    from sklearn.metrics import classification_report
    print(classification_report(y_test, y_pred))

def get_scores(y_test,y_pred,y_pred_prob):
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    scores = []
    scores.append(accuracy_score(y_test, y_pred))
    scores.append(precision_score(y_test, y_pred))
    scores.append(recall_score(y_test, y_pred))
    scores.append(f1_score(y_test, y_pred))
    try:
        scores.append(roc_auc_score(y_test, y_pred_prob[:,1]))
    except:
        scores.append(roc_auc_score(y_test, y_pred))
    return scores


def test_xgboost(X_train, X_test, y_train, y_test,sign):
    import xgboost as xgb
    
    xgb_clf = xgb.XGBClassifier()
    xgb_clf.fit(X_train, y_train)
    y_pred = xgb_clf.predict(X_test)
    y_pred_prob = xgb_clf.predict_proba(X_test)
    scores = get_scores(y_test,y_pred,y_pred_prob)
    
    return xgb_clf, y_pred,scores

def test_random_forest(X_train, X_test, y_train, y_test,sign):
    from sklearn.ensemble import RandomForestClassifier
    rf_clf = RandomForestClassifier(n_estimators=100, random_state=42,n_jobs=-1)
    rf_clf.fit(X_train, y_train)
    y_pred = rf_clf.predict(X_test)
    y_pred_prob = rf_clf.predict_proba(X_test)
    scores = get_scores(y_test,y_pred,y_pred_prob)
    
    return rf_clf, y_pred,scores

def test_MLP(X_train, X_test, y_train, y_test,sign):
    from sklearn.neural_network import MLPClassifier
    mlp_clf = MLPClassifier(random_state=42)
    mlp_clf.fit(X_train, y_train)
    y_pred = mlp_clf.predict(X_test)
    y_pred_prob = mlp_clf.predict_proba(X_test)
    scores = get_scores(y_test,y_pred,y_pred_prob)

    return mlp_clf, y_pred,scores

def test_SVM(X_train, X_test, y_train, y_test,sign):
    from sklearn.svm import SVC
    svm_clf = SVC(random_state=42)
    svm_clf.fit(X_train, y_train)
    y_pred = svm_clf.predict(X_test)
    y_pred_prob = svm_clf.decision_function(X_test)
    scores = get_scores(y_test,y_pred,y_pred_prob)
    return svm_clf, y_pred, scores

def test_logistic_regression(X_train, X_test, y_train, y_test,sign):
    from sklearn.linear_model import LogisticRegression
    lr_clf = LogisticRegression(random_state=42)
    lr_clf.fit(X_train, y_train)
    y_pred = lr_clf.predict(X_test)
    y_pred_prob = lr_clf.predict_proba(X_test)
    scores = get_scores(y_test,y_pred,y_pred_prob)
    
    return lr_clf, y_pred, scores



def run_all_test(features_i,labels_all, train_index, test_index,sign):
    X_train = features_i[train_index]
    X_test = features_i[test_index]
    y_train = labels_all[train_index]
    y_test = labels_all[test_index]
    
    xgb_clf, y_pred_xgb,scores_xgb = test_xgboost(X_train, X_test, y_train, y_test,sign)
    rf_clf, y_pred_rf,scores_rf = test_random_forest(X_train, X_test, y_train, y_test,sign)
    mlp_clf, y_pred_mlp,scores_mlp = test_MLP(X_train, X_test, y_train, y_test,sign)
    svm_clf, y_pred_svm,scores_svm = test_SVM(X_train, X_test, y_train, y_test,sign)
    lr_clf, y_pred_lr,scores_lr = test_logistic_regression(X_train, X_test, y_train, y_test,sign)
    
    scores = pd.DataFrame([scores_xgb, scores_rf, scores_mlp, scores_svm, scores_lr], columns=['accuracy_score', 'precision_score', 'recall_score', 'f1_score', 'roc_auc_score'], index=['xgboost', 'random_forest', 'MLP', 'SVM', 'logistic_regression'])
    
    # 以当前时间戳为文件名
    t = time.time()
    t = int(t)
    
    test_dir = './'+sign+'_'+str(t)

    os.makedirs(test_dir, exist_ok=True)
    
    
    # 保存模型与y_pred,y_test
    import joblib
    joblib.dump(xgb_clf, test_dir + '/' + sign+'_xgb_clf.pkl')
    joblib.dump(rf_clf, test_dir + '/' + sign+'_rf_clf.pkl')
    joblib.dump(mlp_clf, test_dir + '/' + sign+'_mlp_clf.pkl')
    joblib.dump(svm_clf, test_dir + '/' + sign+'_svm_clf.pkl')
    joblib.dump(lr_clf, test_dir + '/' + sign+'_lr_clf.pkl')
    
    np.save(test_dir + '/' + sign+'_y_pred_xgb.npy', y_pred_xgb)
    np.save(test_dir + '/' + sign+'_y_pred_rf.npy', y_pred_rf)
    np.save(test_dir + '/' + sign+'_y_pred_mlp.npy', y_pred_mlp)
    np.save(test_dir + '/' + sign+'_y_pred_svm.npy', y_pred_svm)
    np.save(test_dir + '/' + sign+'_y_pred_lr.npy', y_pred_lr)
    
    np.save(test_dir + '/' + sign+'_y_test.npy', y_test)
    
    # 保存X_train, X_test, y_train, y_test
    np.save(test_dir + '/' + sign+'_X_train.npy', X_train)
    np.save(test_dir + '/' + sign+'_X_test.npy', X_test)
    np.save(test_dir + '/' + sign+'_y_train.npy', y_train)
    np.save(test_dir + '/' + sign+'_y_test.npy', y_test)
    
    
    scores.to_csv(test_dir + '/' + sign+'_scores.csv')
    
    return scores
