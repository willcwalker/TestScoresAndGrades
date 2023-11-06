import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import font_manager

plt.style.use('ggplot')
rcParams['font.family'] = 'EB Garamond'
rcParams['font.size'] = 14  # You can adjust the global font size as needed

# Seed the random number generator for reproducibility
np.random.seed(42)


# Function to generate grades based on quadratic relationship with homework hours
def generate_grade(hours, a, b, c, noise_level):
    # Calculate the grades based on the quadratic equation
    grades = a * hours ** 2 + b * hours + c

    # Adding some random Gaussian noise to each grade
    noise = np.random.normal(0, noise_level, len(hours))
    grades += noise

    # Ensure grades are within the 0 - 100 range after adding noise
    grades = np.clip(grades, 0, 100)

    return grades


# Number of students
num_students = 1500

# Generate random homework hours (say 0 to 24 hours per week)
hours_spent = np.random.uniform(0, 24, num_students)

# Coefficients for the quadratic equation
h = 11.667  # Assuming maximum grade is achieved at 12 hours of study.
k = 100  # Assuming the maximum grade is 100.

a = -0.15  # Adjust this value as needed to control the curvature

# Recalculate 'b' and 'c' based on the new 'a' value
b = -2 * a * h  # Derived from the vertex form of a parabola
c = (a * h ** 2) + k  # Ensure that the vertex is at (h, k)

# Generate grades with reduced noise level
noise_level = 5  # Adjust the noise level as needed
grades = generate_grade(hours_spent, a, b, c, noise_level)

# Create a DataFrame
students_data = pd.DataFrame({
    'StudentID': np.arange(1, num_students + 1),
    'HoursHomework': hours_spent,
    'Grade': grades
})

# Display the first few rows of the DataFrame
print(students_data.head())

# Assuming 'x' is your independent variable and 'y' is your dependent variable
# Let's say you have a pandas DataFrame 'df' with 'HoursHomework' as x and 'Grade' as y
x = students_data['HoursHomework']
y = students_data['Grade']

# Choose the degree of your polynomial. For example, a degree of 2 means a quadratic curve.
degree = 2

# Perform the polynomial fit
coefficients = np.polyfit(x, y, degree)
polynomial = np.poly1d(coefficients)

# Generate enough x values to create a smooth line
x_poly = np.linspace(min(x), max(x), 100)
y_poly = polynomial(x_poly)

# Calculate R squared
y_hat = polynomial(x)  # Your regression model as a function of x
y_bar = np.mean(y)  # Mean value of y
ss_reg = np.sum((y_hat - y_bar) ** 2)  # Sum of squares of the model
ss_tot = np.sum((y - y_bar) ** 2)  # Total sum of squares
r_squared = ss_reg / ss_tot  # Calculation of R^2

# Create the scatter plot with a larger figure size
plt.figure(figsize=(10, 6))  # You can adjust the figure size to your preference

# Scatter plot with smaller dots
plt.scatter(x, y, s=10, color='#003781')  #

# remove gridlines
plt.grid(False)

# Add the polynomial line to the plot
plt.plot(x_poly, y_poly, color='darkred', linewidth=2, label=f'Polynomial fit (degree={degree})')

# Add the R-squared value to the plot in a more subtle place
plt.annotate(f'$R^2 = {r_squared:.3f}$', xy=(0.8, 0.1), xycoords='axes fraction',
             fontsize=12, bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))

# Set axes limits to make the curve less steep
plt.xlim(left=0, right=25)
plt.ylim(bottom=0, top=110)

# Add labels and title with increased font size
plt.title('Prediction of Performance as a Function of Weekly Time Spent on Homework', fontsize=18)
plt.xlabel('Total Weekly Hours Spent on Homework', fontsize=14)
plt.ylabel('Predicted Exam Grade', fontsize=14)

# Move the legend outside the plot
plt.legend(loc='upper right', bbox_to_anchor=(1, -.15), shadow=False, ncol=2)
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=2)

# Add a grid
# plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Improve the tick marks
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Show the plot
plt.tight_layout()  # Adjusts the plot to ensure everything fits without overlapping
plt.show()

# Save to a CSV file (optional)
students_data.to_excel('/Users/william/Desktop/Test Data/studentGradesData.xlsx', index=False)
