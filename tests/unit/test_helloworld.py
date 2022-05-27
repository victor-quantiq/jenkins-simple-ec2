from tests.unit.utils import main_utils

HELLOWOLRD_PATH='hello_world/'

def test_setup_helloworld():
    
    print('\r\nCreating the lambda function...')
    main_utils.create_lambda(HELLOWOLRD_PATH + 'app.py', 'app')


# def test_invoke_helloworld():
#     print('\r\nInvoking the lambda function...')
#     payload = main_utils.invoke_function('lambda')
#     print(payload)
#     assert (payload['body'] == 'Hello User!')