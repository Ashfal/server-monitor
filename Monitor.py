#!/usr/bin/env python

# Displays system resource usage information on an Arduino 16x2 LCD
# DEPENDECNIES (python): pyserial psutil

import datetime, os, psutil, serial, time
from typing import Tuple
# Change to your harware setup
# file to send serial data to
file_descriptor = '/dev/ttyUSB0'
baud_rate = 9600

# time to wait until serial port is open after initializing the connection
serial_init_interval_seconds = 6
# time between updates to the serial port
serial_update_interval_seconds = 3


def format_float_as_string(number: float, integer_digits: int, decimal_digits: int) -> str:
    """ Converts a float into its string representation according to the arguments.

        The integer part of the resulting string will contain exactly 'integer_digits' number of
        characters. Excess space is padded with blank spaces. If 'number' is larger than the largest
        number that can be represented with 'integer_digits' number of digits, the largest number
        is used. This behaviour is analogous for negative numbers.

        The decimal part of the resulting string will contain exactly 'decimal_digits' number of
        characters. Excess space is padded with zeroes.

        For negative input numbers, '-' occupies one character in the integer part of the resulting
        string.

        Examples
        --------
        format_float_as_string(123.45, 4, 3) -> ' 123.450'
        format_float_as_string(123.45, 2, 1) ->   '99.4'
        format_float_as_string(-23.45, 2, 3) ->   '-9.450'

        Arguments
        ---------
        number : float
            The number to be formatted and converted into a string.

        integer_digits : int
            The number of digits which the integer part of the string representation will have.

        decimal_digits : int
            The number of digits which the decimal/fractional part of the string representation will have.

        Returns
        -------
        float_as_string : str
            A string representation of number, where the number of characters before the decimal point is exactly
            'integer_digits' and where the number of characters after the decimal point is exactly 'decimal_digits'.
    """
    # calculate smallest/largest possible integer for the given number of integer digits,
    # taking into account the '-' sign on negative numbers
    max_integer_size = pow(10, integer_digits) - 1
    min_integer_size = 0 - int(max_integer_size / 10)

    # split input number into integer part and decimal part
    integer_part = int(number)
    decimal_part = abs(number) - abs(integer_part)

    # max out integer part if number of digits is exceeded
    if number < min_integer_size:
        integer_part = min_integer_size
    if number > max_integer_size:
        integer_part = max_integer_size

    # round decimal part to 'decimal_digits' decimal places
    decimal_part = round(decimal_part, decimal_digits)
    # cast to integer
    decimal_part = int(decimal_part * pow(10, decimal_digits))

    # cast to string
    integer_part=str(integer_part)
    decimal_part=str(decimal_part)

    # pad integer_part with spaces on the left if necessary
    integer_part = integer_part.rjust(integer_digits, ' ')
    # pad decimal_part with zeroes on the right if necessary
    #decimal_part = decimal_part.rjust(decimal_digits, '0')

    return integer_part + '.' + decimal_part


def get_info():
    # each call returns a float

    cpu_percent = psutil.cpu_percent(interval=None)
    mem_percent = psutil.virtual_memory().percent
    cpu_temp = psutil.sensors_temperatures().get('scpi_sensors')[0].current

    output = (
        '   MEM  Usage   ',
        '{0}%,{1}%,{2}*'.format(
        round(cpu_percent),
        format_float_as_string(mem_percent, 2, 1),
        round(cpu_temp))
    )
    

    return output


def main():
    # open the serial port
    arduino = serial.Serial(port=file_descriptor, baudrate=baud_rate)
    # wait a while until it is ready to receive
    time.sleep(serial_init_interval_seconds)

    # functions displaying different system information in the same format
    sysinfo_functions = [
        get_info
    ]

    # begin continuous loop, wait between transmissions
    while True:
        # call each function and send its output to the serial connection
        for function in sysinfo_functions:
            display_output = function()
            print(bytes(display_output[1], 'utf-8'))
            arduino.write(bytes(display_output[1], 'utf-8'))
            time.sleep(serial_update_interval_seconds)

if __name__ == "__main__":
    main()