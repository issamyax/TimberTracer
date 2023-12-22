import math
from scipy.stats import weibull_min
import numpy as np
import pandas as pd

def dendrometer(scale, shape, total_population, class_width, DBH):

    # Compute location
    location =  DBH - scale * math.gamma(1 + (1 / shape))

    # Initialize the lower bound of the first class as lambda
    lower_bound = location

    # Initialize the class number
    class_number = 1

    # Initialize an empty list to store height_center values
    height_centers = []

    # Initialize an empty dictionary to store class information
    class_info = {}

    while True:
        # Calculate the upper bound of the current class
        upper_bound = lower_bound + class_width

        # Calculate the class center
        class_center = round((lower_bound + upper_bound) / 2, 1)

        # Calculate the probability that an individual falls within the current class
        prob_class = weibull_min.cdf(upper_bound, c=shape, loc=location, scale=scale) - weibull_min.cdf(lower_bound, c=shape, loc=location, scale=scale)

        # Calculate the number of individuals in the current class, ensuring it's at least 1
        individuals_in_class = max(1, round(prob_class * total_population))

        # Check if the number of individuals is 5 or more
        if individuals_in_class >= 5:
            # Apply a quadratic polynomial function to the class center and round it to 2 decimal places
            height_center = round(1.052 + 0.5510 * class_center - 0.002570 * (class_center ** 2), 2)  # Specification of the diameter to height function

            # Append height_center to the list for quartile calculation
            height_centers.append(height_center)

            # Apply another polynomial function to the quadratic result and round it to 2 decimal places
            cbh_center = round(0.8 * (height_center ** 1), 2)  # Specification of the height to CBH function
            basal_area = round(np.pi/4*(class_center**2)*0.0001,3)
            class_info[class_number] = {
                "Diameter_Center": class_center,
                "Individuals": individuals_in_class,
                "Height_Center": height_center,
                "CBH": cbh_center,  # Add the result of the second polynomial
                "BA": basal_area
            }

        # Move to the next class
        class_number += 1
        lower_bound = upper_bound

        # Exit the loop if the upper bound goes beyond a practical limit
        if upper_bound > 1000:  # Adjust this limit based on your application
            break

    # Calculate the 95th height center quartile
    quartile_95 = np.percentile(height_centers, 95)

    # Calculate the mean(CBH)
    mean_cbh = np.mean([class_info[key]["CBH"] for key in class_info])

    # Update the "SC" key based on the specified conditions
    for key, value in class_info.items():
        if value["Height_Center"] > quartile_95:
            value["SC"] = 1
        elif value["Height_Center"] > (0.5 * (mean_cbh + quartile_95)) and value["Height_Center"] <= quartile_95:
            value["SC"] = 2
        elif value["Height_Center"] > mean_cbh and value["Height_Center"] <= (0.5 * (mean_cbh + quartile_95)):
            value["SC"] = 3
        elif value["Height_Center"] < mean_cbh:
            value["SC"] = 4

    # Print the results as a dictionary with rounded values and the "SC" key
    print(class_info)

    df = pd.DataFrame.from_dict(class_info, orient = 'index')
    df.reset_index(drop= True, inplace=True)

    expanded_rows = []

    for idx, row in df.iterrows():
        for _ in range(int(row['Individuals'])):
            expanded_rows.append([None, row['Diameter_Center'], row['Height_Center'], row['CBH'], row['SC'],row['BA']])

    expanded_df = pd.DataFrame(expanded_rows, columns=['ID', 'Diameter_Center', 'Height_Center', 'CBH', 'SC','BA'])

    # Assign simple numeric IDs starting from 1
    expanded_df['ID'] = range(1, len(expanded_df) + 1)

    return expanded_df