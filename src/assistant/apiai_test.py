import os.path
import sys

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '<client_access_token>'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'kr'  # optional, default value equal 'en'

    #request.session_id = "ninevis"

    request.query ="오늘 밥 뭐야"

    response = request.getresponse()

    print (response.read().decode("utf-8"))


if __name__ == '__main__':
    main()
