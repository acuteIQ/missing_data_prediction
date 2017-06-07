def zip_to_int(zip_code):
    if type(zip_code) == type(1):
        return zip_code
    elif type(zip_code) == type(''):
        zip_code = zip_code.replace(' ', '')
        build_int=''
        for letter in zip_code:
            try:
                build_int += str( int( letter ) )
            except:
                build_int += str( ord( letter ) )

    else:
        raise Exception('unknown type ' + type(zip_code))
