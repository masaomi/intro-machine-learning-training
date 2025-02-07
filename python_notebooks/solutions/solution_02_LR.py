logi_r=LogisticRegression(class_weight='balanced')

pipeline_lr=Pipeline([('scalar',StandardScaler()),
                     ('model',logi_r)])

from sklearn.model_selection import GridSearchCV

# define the hyperparameters you want to test
# with the range over which you want it to be tested.
grid_values = {'model__C': np.logspace(-2,1,50),
               'model__penalty':['l1','l2'],
               'model__solver':['liblinear']}

#Feed it to the GridSearchCV with the right
#score(here accuracy) over which the decision should be taken
grid_lr_roc_auc = GridSearchCV(pipeline_lr, 
                           param_grid = grid_values, 
                           scoring='roc_auc',n_jobs=-1)

grid_lr_roc_auc.fit(X_cancer_train, y_cancer_train)

y_decision_fn_scores_roc_auc=grid_lr_roc_auc.score(X_cancer_test,y_cancer_test)

print('Grid best parameter (max. roc_auc):')
print( '\t' + '\n\t'.join([str(x) for x in grid_lr_roc_auc.best_params_.items()]))
print('Grid best score (roc_auc): ', grid_lr_roc_auc.best_score_)
print('Grid best parameter (max. roc_auc) model on test: ', y_decision_fn_scores_roc_auc)

## predicting the labels on the test set    
y_pred_test_c=grid_lr_roc_auc.predict(X_cancer_test)

bestP = grid_lr_roc_auc.best_params_['model__penalty']
bestC = grid_lr_roc_auc.best_params_['model__C']
testAcc = accuracy_score(y_cancer_test,y_pred_test_c)
    
plotTitle = 'LR penalty: {}, C: {:.3f}\n Accuracy: {:.3f}'.format( bestP,
                                                               bestC,
                                                               testAcc)

plotConfusionMatrix( y_cancer_test, y_pred_test_c, 
                    ['Benign','Malignant'] , plotTitle , 
                    ax = None)

plot_roc_curve(grid_lr_roc_auc,X_cancer_test, y_cancer_test)
    
