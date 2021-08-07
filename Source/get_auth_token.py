def get_token():
    print('Looking for auth_code.txt file...')

    try:
        TOKEN_FILE = open('./auth_token.txt')
        print('Reading...')
        contents = TOKEN_FILE.read()
        TOKEN_FILE.close()
        print('----------------')

        if contents == '':
            print('Empty file. Please fill it in with Genius token.')
            return None
            
        return contents
    
    except Exception as e:
        print('Error:')
        print(e)
        print('----------------')
        print('An error has occured, make sure you created "auth_code.txt".')
        return None