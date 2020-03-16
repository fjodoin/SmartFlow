import pandas as pd
import pickle
import joblib
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

training_dataset = pd.read_csv('combined_dataset.csv', index_col='Date Time')

reduced_pos_set = training_dataset[training_dataset['label'] == 0].sample(n=50)
reduced_neg_set = training_dataset[training_dataset['label'] == 1]

second_frames = [reduced_pos_set, reduced_neg_set]
reduced_result = pd.concat(second_frames)
reduced_result.sort_index(inplace=True)

knn = KNeighborsClassifier(n_neighbors=9)
temp_x = reduced_result.iloc[:, 0:8]
temp_y = reduced_result.iloc[:, 8]
X_train, X_test, y_train, y_test = train_test_split(temp_x, temp_y, random_state=0)
x = training_dataset.iloc[:, 0:8]
y = training_dataset.iloc[:, 8]
xtrain, xtest, ytrain, ytest = train_test_split(x, y, random_state=0)
knn.fit(X_train, y_train)

print('Test Set Score: {:.2f}'.format(knn.score(X_test, y_test)))
print('Full Test Set Score: {:.2f}'.format(knn.score(xtrain, ytrain)))

#Save model with pickle

pickle.dump(knn, open('pickel_saved_model', 'wb'))

#Save model with joblib

joblib.dump(knn, 'joblib_saved_model')



