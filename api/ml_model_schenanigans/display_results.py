import matplotlib.pyplot as plt

# Data
categories = ['Our Grades (Predicted)', 'TA Reports', 'Autograder (Normalized)']
values = [-0.365, 21.545, 21.903]  # Adjusted your predicted grades for visual consistency

# Creating the bar chart
plt.figure(figsize=(10, 6))
bars = plt.bar(categories, values, color=['red', 'blue', 'green'])

# Adding a specific color to highlight the negative value
bars[0].set_color('red')  # Red color to emphasize the negative predicted grade

# Adding value labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 3), ha='center', va='bottom', fontsize=10)

# Title and labels
plt.title('Comparison of Grades')
plt.ylabel('Grade Value')
plt.ylim(min(values) - 1, max(values) + 1)  # Setting y-limits for better visual display

# Show the plot
plt.show()
