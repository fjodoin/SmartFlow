The contents of this folder include:
- README -> This file!
- Two Machine Learning(ML) Models:
	- joblib_saved_model
	- pickle_saved_model
- model_test.py
- aruba.jpg

The "saved_model" files (i.e. joblib_saved_model and pickle_saved_model) reference the
same ML model, they are just saved and loaded using two different serialization formats;
One uses pickle, the other uses joblib. I am primarily using joblib because I've found
that it is faster at loading the model and processing input data. However, if there are
issues with porting this file to the pi, feel free to try the pickle version and see if
it works better.

model_test.py contains a short script that initializes two example input samples. One of
a non-anomalous and one of an anomalous sample. They're there to show how each input from
the sensors should be structured before inserting them into the model. The script also has
a comment that maps the input to the sensors that have been modeled. Finally, boiler-plate
code is provided to show how the models can be loaded into the script and run to produce
an output.

Output can be:
- 0 -> Non-Anomalous
- 1 -> Anomalous

aruba.jpg is a photo that illustrates the distribution of sensors from the study whose
dataset we've trained our models on.

If you feel the README is missing any information, feel free to contact me ;).
