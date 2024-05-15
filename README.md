# Backward Elimination-Wrapped Naive Bayes Classifier

## Overview
This Python script implements a Naive Bayes classifier with Backward Elimination, a feature selection technique, to improve classification accuracy by selecting the most relevant attributes. The script works for multi-class classification problems and is suitable for datasets with structured attribute-value pairs.

## Features
- Utilizes Pandas and NumPy libraries for efficient data handling and computation.
- Implements the Naive Bayes algorithm for classification.
- Incorporates Backward Elimination to iteratively select the optimal subset of attributes for classification.
- Provides detailed testing statistics and outputs the optimal attribute subset.

## Usage
1. Clone the repository:

   ```
   git clone https://github.com/your_username/be-naive-bayes.git
   ```
   
2. Navigate to the project directory:

   ```
   cd be-naive-bayes
   ```

3. Install the required dependencies:

   ```
   pip install pandas numpy
   ```

4. Edit the script and input your own values in the designated section:

   ```python
   # INPUT YOUR OWN VALUES IN THIS SECTION
   ALGORITHM_NAME = "BE-Wrapped Naive Bayes"
   DATA_PATH = "/path/to/your/dataset.txt"
   TEST_STATS_FILE = "naive_bayes_test_stats.txt"
   TEST_OUT_FILE = "naive_bayes_test_out.txt"
   ...
   ```

5. Run the main script:

   ```
   python bf_naive_bayes.py
   ```

6. View the generated output files for testing statistics and optimal attribute subset.

## File Structure
- `bf_naive_bayes.py`: Main Python script implementing the Naive Bayes classifier with Backward Elimination.
- `iris_dataset.txt`: Example dataset (can be replaced with your own dataset).
- `naive_bayes_test_stats.txt`: Output file containing testing statistics.
- `naive_bayes_test_out.txt`: Output file containing the optimal attribute subset.

## Requirements
- Python 3.x
- Pandas
- NumPy

## Author
- Chaudhari Dhairyansh Nathubhai

---

Feel free to customize it further to suit your project's specifics!
