

import pickle
class A(): 
    def __init__(self, x, y): 
        self.x = x 
        self.y = y 
    
    def sum(self): 
        return self.x + self.y


A_lst = [(i+20, A(i, i), 30) for i in range(10)]

with open('A_lst.pkl', 'wb') as f:
    pickle.dump(A_lst, f)

# Load the pickled data back into a list
with open('A_lst.pkl', 'rb') as f:
    loaded_A_lst = pickle.load(f)

# Display the loaded data
for obj in loaded_A_lst:
    print(obj[0]) 
    print(obj[1].sum())
    print(obj[2])
  