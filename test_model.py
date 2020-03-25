import joblib

filename = 'finalized_model.sav'
loaded_model = joblib.load(filename)

test = [[3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

print(loaded_model.predict(test))