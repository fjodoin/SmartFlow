import pickle
import joblib

###
# index[0]: Time of day
# index[1]: Kitchen(M019)
# index[2]: Living(M020)
# index[3]: Master Bedroom(M007)
# index[4]: Office(M027)
# index[5]: Bedroom(M024)
# index[6]: Front Door(D001)
# index[7]: Back Door(D002)
###

good_sample = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
bad_sample = [[0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]

joblib_model = joblib.load('joblib_saved_model')
print(f'This should be zero: {joblib_model.predict(good_sample)}')
print(f'This should be one: {joblib_model.predict(bad_sample)}')

# Using pickle, alternative method
# pickle_model = pickle.load(open('pickel_saved_model', 'rb'))
# print(pickle_model.predict(good_sample))