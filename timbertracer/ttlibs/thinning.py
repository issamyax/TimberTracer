def perform_thinning(trees_df, thinning_type, target_sum, tolerance):

    df_copy = trees_df.copy()

    # Define your target sum and tolerance (positive and negative; meaning more or less)
    #target_sum = 8.68
    #tolerance = 0.3

    # Initialize an empty list to store selected tree IDs
    selected_tree_ids = []

    # Initialize variables to keep track of the current sum and number of iterations
    current_sum = 0
    iterations = 0


    if thinning_type == 'above':

        # Loop until the current sum falls within the tolerance range or exceed a maximum number of iterations
        while not (target_sum - tolerance <= current_sum <= target_sum + tolerance) and iterations < 1200:
            # Create masks to filter trees from classes 1, 2, and 3 on each iteration
            class_1_mask = df_copy['SC'] == 1
            class_2_mask = df_copy['SC'] == 2
            class_3_mask = df_copy['SC'] == 3

            # Randomly select a tree from classes 1 and 2 and add their "g" value to the current sum
            if current_sum < (target_sum - tolerance) and (class_1_mask.sum() + class_2_mask.sum()) > 0:
                class_1_or_2 = df_copy[class_1_mask | class_2_mask].sample(n=1)
                current_sum += class_1_or_2['BA'].values[0]  # Sum the "BA" value
                selected_tree_ids.append(class_1_or_2['ID'].values[0])
                df_copy = df_copy.drop(class_1_or_2.index)  # Remove the selected row from the DataFrame

            # If target sum is not reached yet, randomly select a tree from class 3 and add their "g" value to the current sum
            elif current_sum < (target_sum - tolerance) and class_3_mask.sum() > 0:
                class_3 = df_copy[class_3_mask].sample(n=1)
                current_sum += class_3['BA'].values[0]  # Sum the "BA" value
                selected_tree_ids.append(class_3['ID'].values[0])
                df_copy = df_copy.drop(class_3.index)  # Remove the selected row from the DataFrame

            # Increment the number of iterations
            iterations += 1

    elif thinning_type == 'bottom':
        # Loop until the current sum falls within the tolerance range or exceed a maximum number of iterations
        while not (target_sum - tolerance <= current_sum <= target_sum + tolerance) and iterations < 1200:
            # Create masks to filter trees from classes 1, 2, and 3 on each iteration
            class_4_mask = df_copy['SC'] == 4
            class_3_mask = df_copy['SC'] == 3
            class_2_mask = df_copy['SC'] == 2

            # Randomly select a tree from classes 4 and 3 and add their "g" value to the current sum
            if current_sum < (target_sum - tolerance) and (class_4_mask.sum() + class_3_mask.sum()) > 0:
                class_4_or_3 = df_copy[class_4_mask | class_3_mask].sample(n=1)
                current_sum += class_4_or_3['BA'].values[0]  # Sum the "g" value
                selected_tree_ids.append(class_4_or_3['ID'].values[0])
                df_copy = df_copy.drop(class_4_or_3.index)  # Remove the selected row from the DataFrame

            # If target sum is not reached yet, randomly select a tree from class 2 and add their "g" value to the current sum
            elif current_sum < (target_sum - tolerance) and class_2_mask.sum() > 0:
                class_2 = df_copy[class_2_mask].sample(n=1)
                current_sum += class_2['BA'].values[0]  # Sum the "g" value
                selected_tree_ids.append(class_2['ID'].values[0])
                df_copy = df_copy.drop(class_2.index)  # Remove the selected row from the DataFrame

            # Increment the number of iterations
            iterations += 1

    elif thinning_type == 'neutral':
        # Loop until the current sum falls within the tolerance range or exceed a maximum number of iterations
        while not (target_sum - tolerance <= current_sum <= target_sum + tolerance) and iterations < 1000:
        # Randomly select a tree from the entire DataFrame and add their "g" value to the current sum
            if df_copy.shape[0] > 0:
                selected_tree = df_copy.sample(n=1)
                current_sum += selected_tree['BA'].values[0]  # Sum the "g" value
                selected_tree_ids.append(selected_tree['ID'].values[0])
                df_copy = df_copy.drop(selected_tree.index)  # Remove the selected row from the DataFrame

            # Increment the number of iterations
            iterations += 1

    return selected_tree_ids