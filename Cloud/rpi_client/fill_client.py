import argparse
import serial
import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', help="Microbit serial port", type=str)
    parser.add_argument(
        "--apihost", default='http://localhost:5000',
        help="Server hostname", type=str)
    args = parser.parse_args()

    # for testing only
    # r = requests.post(
    #     '{}/api/bin/update'.format(args.apihost), json={
    #         'bin_name': 'alpha',
    #         'microbit_name': 'vavet',
    #         'distance': 150
    #     })
    # print(r.text)

    try:
        ser = serial.Serial(port=args.port, baudrate=115200)
        print('Listening on {}...'.format(args.port))

        while True:
            msg = ser.readline().decode('utf-8').strip()

            msg_arr = msg.split('_')

            if (msg_arr[1] == 'FILL'):
                fill_info = {
                    'bin_name': msg_arr[0],
                    'distance': int(msg_arr[2])
                }

                r = requests.post(
                    '{}/api/bin/update'.format(args.apihost), data=fill_info)
                print(r.text)

    except serial.SerialException as err:
        print('SerialExceptionL {}'.format(err))
    except KeyboardInterrupt:
        print('Program Terminated')


if __name__ == "__main__":
    main()
