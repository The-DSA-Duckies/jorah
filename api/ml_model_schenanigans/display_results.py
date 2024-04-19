import matplotlib.pyplot as plt

# Data
categories = ['TA Grades', 'Autograder Grades (Normalized)']
values = [21.545, 21.903]  # Adjusted your predicted grades for visual consistency

# Creating the bar chart
plt.figure(figsize=(10, 6))
bars = plt.bar(categories, values, color=['red', 'blue'])

# Adding a specific color to highlight the negative value
bars[0].set_color('red')  # Red color to emphasize the negative predicted grade

# Adding value labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 3), ha='center', va='bottom', fontsize=10)

# Title and labels
plt.title('Comparison of Grades')
plt.ylabel('Mean Grade Value')
plt.ylim(min(values) - 1, max(values) + 1)  # Setting y-limits for better visual display

# Adding grid
plt.grid(True, which='both', linestyle='--', linewidth=0.5, axis='y')  # Grid lines for the y-axis

# Show the plot
plt.show()
