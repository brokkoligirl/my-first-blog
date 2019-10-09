from configparser import ConfigParser


def get_client_ip(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_recaptcha_key():

    try:

        config = ConfigParser()
        config.read('config.ini')
        key = config['GOOGLE']['RECAPTCHA_SECRET_KEY']

        return key

    except FileNotFoundError:

        print("no config file found.")
        # TODO: create config file
