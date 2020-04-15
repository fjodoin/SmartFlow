These are the test cases that I tested with and the model predicted accurately:

Order: 'Time_Of_Day', 'Kitchen(M015-L)', 'Kitchen(M019-M)', 'Living(M020-M)','Bedroom(M007-M)', 'Office(M027-M)', 'Front Door(D001-D)',
       'Back Door(D002-W)', 'Living(M013-L)', 'Office(M026-L)',
       'Bedroom(M005-L)'

Input:

kitchen = [[0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
living = [[0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]]
bedroom = [[0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
office = [[0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0]]

doors_open_night = [[3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0]]
more_than_one_motion_sensor = [[0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

Output:

# Must be 0
print(knn.predict(kitchen))
print(knn.predict(living))
print(knn.predict(bedroom))
print(knn.predict(office))

#Must be 1
print(knn.predict(doors_open_night))
print(knn.predict(more_than_one_motion))

result:

[0]
[0]
[0]
[0]
[1]
[1]