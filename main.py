
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi 45, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


import pandas as pd

# Step 1: Create sample student data
data = {
    "Student_ID": [101, 102, 103, 104, 105],
    "First_Name": ["Alice", "Bob", "Charlie", "Diana", "Ethan"],
    "Last_Name": ["Smith", "Brown", "Johnson", "White", "Clark"],
    "Age": [20, 21, 19, 22, 20],
    "Gender": ["F", "M", "M", "F", "M"],
    "Department": ["Physics", "Chemistry", "Math", "Biology", "Computer Science"],
    "GPA": [3.5, 3.7, 3.9, 3.2, 3.8]
}

# Step 2: Create DataFrame
df = pd.DataFrame(data)

# Step 3: Save as CSV
df.to_csv("nikky_dumpy.csv", index=False)

print("CSV file 'students.csv' created successfully!")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm test45333')

