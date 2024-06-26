import pandas as pd # Import Pandas library 
import numpy as np # Import Numpy library
 
# File name: bf_naive_bayes.py
# Author: Addison Sears-Collins
# Date created: 6/10/2019
# Python version: 3.7
# Description: Implementation of Naive Bayes which uses Back-Ward Elimination
# This code works for multi-class 
# classification problems (e.g. democrat/republican/independent)
# Calculate P(E1|CL0)P(E2|CL0)P(E3|CL0)...P(E#|CL0) * P(CL0) and
# P(E1|CL1)P(E2|CL1)P(E3|CL1)...P(E#|CL1) * P(CL1) and
# P(E1|CL2)P(E2|CL2)P(E3|CL2)...P(E#|CL2) * P(CL2), etc. and predict the
# class with the maximum result. 
# E is an attribute, and CL means class.
# Only need class prior probability and likelihoods to make a prediction
# (i.e. the numerator of Bayes formula) since denominators are same for both 
# the P(CL0|E1,E2,E3...)*P(CL0) and P(CL1|E1,E2,E3...)*P(CL1), etc. cases 
# where P means "probability of" and | means "given".
 
# Required Data Set Format:
# Columns (0 through N)
# 0: Instance ID
# 1: Attribute 1 
# 2: Attribute 2
# 3: Attribute 3 
# ...
# N: Actual Class 
 
# This program then adds 2 additional columns for the testing set.
# N + 1: Predicted Class
# N + 2: Prediction Correct? (1 if yes, 0 if no)
 
################ INPUT YOUR OWN VALUES IN THIS SECTION ######################
ALGORITHM_NAME = "BE-Wrapped Naive Bayes"
DATA_PATH = "/Users/omdariyans/Downloads/Backward Elimination/iris_dataset.txt"  # Directory where data set is located
TEST_STATS_FILE = "iris_dataset_naive_bayes_test_stats.txt"#Testing statistics
TEST_OUT_FILE = "iris_dataset_naive_bayes_test_out.txt" # Testing output
# Show functioning of the program
TRACE_RUNS_FILE  = "iris_dataset_naive_bayes_trace_runs.txt"
SEPARATOR = ","  # Separator for the data set (e.g. "\t" for tab data)
TRAINING_DATA_PRCT = 0.67 # % of data set used for training. Default 0.67
testing_data_prct = 1 - TRAINING_DATA_PRCT # % of data set used for testing
SEED = 99  # SEED for the random number generator. Default: 99
#############################################################################
 
# Open a new file to save trace runs
outfile3 = open(TRACE_RUNS_FILE,"w") 
 
# Naive Bayes algorithm. Accepts a Pandas dataframeas its parameter
def naive_bayes(pd_data):
    # Create a training dataframe by sampling random instances from original data.
    # random_state guarantees that the pseudo-random number generator generates 
    # the same sequence of random numbers each time.
    pd_training_data = pd_data.sample(frac=TRAINING_DATA_PRCT, random_state=SEED)
 
    # Create a testing dataframe. Dropping the training data from the original
    # dataframe ensures training and testing dataframes have different instances
    pd_testing_data = pd_data.drop(pd_training_data.index)
 
    ######COMMENT OUT THESE TWO LINES BEFORE RUNNING ################
    #pd_training_data = pd_data.iloc[:20] # Used for testing only, gets 1st 20 rows
    #pd_testing_data = pd_data.iloc[20:22,:] # Used for testing only, rows 20 & 21
 
    # Calculate the number of instances, columns, and attributes in the
    # training data set. Assumes 1 column for the instance ID and 1 column
    # for the class. Record the index of the column that contains 
    # the actual class
    no_of_instances_train = len(pd_training_data.index) # number of rows
    no_of_columns_train = len(pd_training_data.columns) # number of columns
    no_of_attributes = no_of_columns_train - 2
    actual_class_column = no_of_columns_train - 1
 
    # Store class values in a column, sort them, then create a list of unique
    # classes and store in a dataframe and a Numpy array
    unique_class_list_df = pd_training_data.iloc[:,actual_class_column]
    unique_class_list_df = unique_class_list_df.sort_values()
    unique_class_list_np = unique_class_list_df.unique() #Numpy array
    unique_class_list_df = unique_class_list_df.drop_duplicates()#Pandas df
 
    # Record the number of unique classes in the data set
    num_unique_classes = len(unique_class_list_df)
 
    # Record the frequency counts of each class in a Numpy array
    freq_cnt_class = pd_training_data.iloc[:,actual_class_column].value_counts(
        sort=True)
 
    # Record the frequency percentages of each class in a Numpy array
    # This is a list of the class prior probabilities
    class_prior_probs = pd_training_data.iloc[:,actual_class_column].value_counts(
        normalize=True, sort=True)
 
    # Add 2 additional columns to the testing dataframe
    pd_testing_data = pd_testing_data.reindex(
                      columns=[*pd_testing_data.columns.tolist(
                      ), 'Predicted Class', 'Prediction Correct?'])
 
    # Calculate the number of instances and columns in the
    # testing data set. Record the index of the column that contains the 
    # predicted class and prediction correctness (1 if yes; 0 if no)
    no_of_instances_test = len(pd_testing_data.index) # number of rows
    no_of_columns_test = len(pd_testing_data.columns) # number of columns
    predicted_class_column = no_of_columns_test - 2
    prediction_correct_column = no_of_columns_test - 1
 
    ######################### Training Phase of the Model ########################
    # Create a an empty dictionary
    my_dict = {}
 
    # Calculate the likelihood tables for each attribute. If an attribute has
    # four levels, there are (# of unique classes x 4) different probabilities 
    # that need to be calculated for that attribute.
    # Start on the first attribute and make your way through all the attributes
    for col in range(1, no_of_attributes + 1):
 
        # Record the name of this column 
        colname = pd_training_data.columns[col]
 
        # Create a dataframe containing the unique values in the column
        unique_attribute_values_df = pd_training_data[colname].drop_duplicates()
        # Create a Numpy array containing the unique values in the column
        unique_attribute_values_np = pd_training_data[colname].unique()
     
        # Calculate likelihood of the attribute given each unique class value
        for class_index in range (0, num_unique_classes):
         
            # For each unique attribute value, calculate the likelihoods 
            # for each class
            for attr_val in range (0, unique_attribute_values_np.size) :
                running_sum = 0
 
                # Calculate N(unique attribute value && class value)
                # Where N means "number of" and && means "and"
                # Go through each row of the training set
                for row in range(0, no_of_instances_train):
                    if (pd_training_data.iloc[row,col] == (
                        unique_attribute_values_df.iloc[attr_val])) and (
                        pd_training_data.iloc[row, actual_class_column] == (
                        unique_class_list_df.iloc[class_index])):
                            running_sum += 1
 
                # With N(unique attribute value && class value) as the numerator
                # we now need to divide by the total number of times the class
                # appeared in the data set
                try:
                    denominator = freq_cnt_class[class_index]
                except:
                    denominator = 1.0
             
                likelihood = running_sum / denominator
             
                # Add a new likelihood to the dictionary
                # Format of search key is 
                # <attribute_name><attribute_value><class_value>
                search_key = str(colname) + str(unique_attribute_values_df.iloc[
                             attr_val]) + str(unique_class_list_df.iloc[
                             class_index])
                my_dict[search_key] = likelihood
  
    # Print the likelihood table to the console
    # print(pd.DataFrame.from_dict(my_dict, orient='index'))
 
    ################# End of Training Phase of the Naive Bayes Model ########
 
    ################# Testing Phase of the Naive Bayes Model ################
 
    # Proceed one instance at a time and calculate the prediction
    for row in range(0, no_of_instances_test):
 
        # Initialize the prediction outcome
        predicted_class = unique_class_list_df.iloc[0]
        max_numerator_of_bayes = 0.0
 
        # Calculate the Bayes equation numerator for each test instance
        # That is: P(E1|CL0)P(E2|CL0)P(E3|CL0)...P(E#|CL0) * P(CL0),
        # P(E1|CL1)P(E2|CL1)P(E3|CL1)...P(E#|CL1) * P(CL1)...
        for class_index in range (0, num_unique_classes):
 
            # Reset the running product with the class
            # prior probability, P(CL)
            try:
                running_product = class_prior_probs[class_index]
            except:
                running_product = 0.0000001 # Class not found in data set
         
            # Calculation of P(CL) * P(E1|CL) * P(E2|CL) * P(E3|CL)...
            # Format of search key is 
            # <attribute_name><attribute_value><class_value>
            # Record each search key value
            for col in range(1, no_of_attributes + 1):
                attribute_name = pd_testing_data.columns[col]
                attribute_value = pd_testing_data.iloc[row,col]
                class_value = unique_class_list_df.iloc[class_index]
 
                # Set the search key
                key = str(attribute_name) + str(
                          attribute_value) + str(class_value)
 
                # Update the running product
                try:
                    running_product *= my_dict[key]
                except:
                    running_product *= 0
 
            # Record the prediction if we have a new max
            # Bayes numerator
            if running_product > max_numerator_of_bayes:
                max_numerator_of_bayes = running_product
                predicted_class = unique_class_list_df.iloc[
                             class_index] # New predicted class
 
        # Store the prediction in the dataframe
        pd_testing_data.iloc[row,predicted_class_column] = predicted_class
     
        # Store if the prediction was correct
        if predicted_class == pd_testing_data.iloc[row,actual_class_column]:
            pd_testing_data.iloc[row,prediction_correct_column] = 1
        else: 
            pd_testing_data.iloc[row,prediction_correct_column] = 0
 
    print("-------------------------------------------------------")
    print("Learned Model Predictions on Testing Data Set")
    print("-------------------------------------------------------")
 
    # Print the revamped dataframe
    print(pd_testing_data)
 
    # accuracy = (total correct predictions)/(total number of predictions)
    accuracy = (pd_testing_data.iloc[
        :,prediction_correct_column].sum())/no_of_instances_test
    # Return classification accuracy
    return accuracy
    ####################### End Testing Phase ######################################    
 
# Backward Elimination method accepts a Pandas dataframe as a parameter
# and then returns the optimal dataframe from that dataframe.

def backward_elimination(pd_data):
    
    instance_id_colname = pd_data.columns[0]
    no_of_columns = len(pd_data.columns) # number of columns
    class_column_index = no_of_columns - 1
    class_column_colname = pd_data.columns[class_column_index]
    
    # Start with the full set of attributes for Backward Elimination
    current_feature_set_df = pd_data.drop(columns=[instance_id_colname, class_column_colname])
    
    base_performance = naive_bayes(pd_data)
    
    while len(current_feature_set_df.columns) > 1:
        best_performance = -9999.0
        feature_to_remove = ""
        
        # Try removing each feature and see the performance
        for feature in current_feature_set_df.columns:
            temp_df = current_feature_set_df.drop(columns=[feature])
            temp_df[instance_id_colname] = pd_data[instance_id_colname]
            temp_df[class_column_colname] = pd_data[class_column_colname]
            
            current_performance = naive_bayes(temp_df)
            
            if current_performance > best_performance:
                best_performance = current_performance
                feature_to_remove = feature
        
        # If removing the best feature improves performance, remove it permanently
        if best_performance > base_performance:
            current_feature_set_df = current_feature_set_df.drop(columns=[feature_to_remove])
            base_performance = best_performance
            outfile3.write(str(feature_to_remove) + " removed from the feature set" + "\n")
            print(str(feature_to_remove) + " removed from the feature set")
        else:
            outfile3.write("Performance did not improve this round." + "\n")
            outfile3.write("End of Backward Elimination." + "\n")
            break

    return current_feature_set_df
    
 
 
def main():
    # Read the full text file and store records in a Pandas dataframe
    pd_full_data_set = pd.read_csv(DATA_PATH, sep=SEPARATOR)
 
    #pd_full_data_set = pd_full_data_set.sample(frac=0.10, random_state=SEED)
     
    # Runs Backward Elimination on the full data set to find the optimal attribute data frame
    optimal_attribute_set = backward_elimination(pd_full_data_set)
 
    # Write dataframe to a file
    optimal_attribute_set.to_csv(TEST_OUT_FILE, sep=",", header=True)
 
    # Open a new file to save the summary statistics
    outfile2 = open(TEST_STATS_FILE,"w") 
 
    # Write to a file
    outfile2.write("----------------------------------------------------------\n")
    outfile2.write(ALGORITHM_NAME + " Summary Statistics (Testing)\n")
    outfile2.write("----------------------------------------------------------\n")
    outfile2.write("Data Set : " + DATA_PATH + "\n")
 
    # Write the relevant stats to a file
    outfile2.write("\n")
    outfile2.write("Number of Test Instances : " +
        str(round(len(optimal_attribute_set.index) * testing_data_prct)) + "\n")
        
    # Run Naive Bayes on the optimal attribute set
    accuracy = naive_bayes(optimal_attribute_set)
    accuracy *= 100
 
    # Write accuracy to the file
    outfile2.write("Accuracy : " + str(accuracy) + "%\n")
 
    # Print statistics to console
    print()
    print()
    print("-------------------------------------------------------")
    print(ALGORITHM_NAME + " Summary Statistics (Testing)")
    print("-------------------------------------------------------")
    print("Data Set : " + DATA_PATH)
 
    # Print the relevant stats to the console
    print()
    print("Number of Test Instances : " +
        str(round(len(optimal_attribute_set.index) * testing_data_prct)))
 
    # Print accuracy to the console
    print()
    print("Accuracy : " + str(accuracy) + "%")
    print()
 
    # Create a dataframe containing the optimal attributes by removing
    # the Instance and the Class Column
    instance_id_colname = optimal_attribute_set.columns[0]
    no_of_columns = len(optimal_attribute_set.columns) # number of columns
    class_column_index = no_of_columns - 1
    class_column_colname = optimal_attribute_set.columns[class_column_index]
    optimal_attribute_set = optimal_attribute_set.drop(columns = [
        instance_id_colname, class_column_colname]) 
 
    # Write a list of the optimal attribute set to a file
    outfile2.write("Optimal Attribute Subset : " + str(list(
        optimal_attribute_set)))
 
    # Print a list of the optimal attribute set
    print("Optimal Attribute Subset : " + str(list(optimal_attribute_set)))
    print()
    print()   
     
    # Close the files
    outfile2.close()
    outfile3.close()
 
main() # Call the main function