import numpy as np

def my_first_lambda_function(event, context):
    array = np.array([1, 2, 3, 4, 5])
    array2 = np.array([1, 2, 3, 4, 5])
    f_array = array + array2
    print(f"Received event: {str(event)}, result is {f_array}")
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }