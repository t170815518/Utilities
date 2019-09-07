def to_decimal(integerPart, radix):
    # integerPart is string, radix is integer
    decimal = 0
    length = len(integerPart)

    for i in range(length):
        if (radix == 16) and not(integerPart[i].isdigit()):  # str.isnumber() is valid
            decimal = decimal + (ord(integerPart[i])-55) * radix ** (length-1-i)  # power operation is not ^
        else:
            decimal = decimal + int(integerPart[i]) * radix ** (length-1-i)
    return str(decimal)


def decimal_to(integerPart, radix):
    # integerPart is string, radix is integer
    decimal = int(integerPart)
    converted = ''
    quotient = decimal//radix
    while quotient != 0:
        remainder = decimal % radix
        if (radix == 16) and (remainder >= 10):
            converted = chr(remainder + 55) + converted
        else:
            converted = str(remainder)+converted
        decimal = quotient
        quotient = decimal//radix
    if (radix == 16) and (decimal >= 10):
        converted = chr(decimal + 55) + converted
    else:
        converted = str(decimal) + converted
    return converted


def fraction(fractionPart, radix1, radix2):
    # fractionPart is string
    converted = ''
    fractionValue = 0
    counter = 0
    for i in range(len(fractionPart)):
        if (radix1 == 16) and not(fractionPart[i].isdigit()):
            fractionValue = fractionValue + (ord(fractionPart[i])-55) * radix1 ** (-i-1)
        else:
            fractionValue = fractionValue + int(fractionPart[i]) * radix1 ** (-i-1)
    fractionValue = fractionValue*radix2
    while (fractionValue % 1 != 0) and (counter <= 10):
        if (radix2 == 16) and (fractionValue // 1 >= 10):
            converted = converted + chr(fractionValue//1 + 55)
        else:
            converted = converted + str(fractionValue // 1)
        fractionValue = fractionValue % 1 * radix2
        counter = counter + 1
    if (radix2 == 16) and (fractionValue // 1 >= 10):
        converted = converted + chr(fractionValue // 1 + 55)
    else:
        converted = converted + str(int(fractionValue // 1))  # //：float
    return '.'+converted


while True:
    numberToConvert = input("Please type the number to convert with prefix (e.g.0b101010111, 0xAB4): ")
    # decomposition
    if numberToConvert.__contains__('0b'):
        prefix = 2
    else:
        if numberToConvert.__contains__('0o'):
            prefix = 8
        else:
            if numberToConvert.__contains__('0x'):
                prefix = 16
            else:
                prefix = 10
    # delete the prefix
    if prefix != 10:
        numberToConvert = numberToConvert[2:]
    ifFraction = False

    if numberToConvert.__contains__('.'):
        # numberToConvert.split(sep='.') cannot change the value of numberToConvert
        numberToConvert = numberToConvert.split(sep='.')
        integer = numberToConvert[0]
        fractionValue = numberToConvert[1]
        ifFraction = True
    else:
        integer = numberToConvert

    # process and print
    if prefix == 10:
        if ifFraction:
            print('=0b'+decimal_to(integer, 2)+fraction(fractionValue, 10, 2))
            print('=0o' + decimal_to(integer, 8) + fraction(fractionValue, 10, 8))
            print('=0x' + decimal_to(integer, 16) + fraction(fractionValue, 10, 16))
        else:
            print('=0b' + decimal_to(integer, 2))
            print('=0o' + decimal_to(integer, 8))
            print('=0x' + decimal_to(integer, 16))
    if prefix == 16:
        decimalValue = to_decimal(integer, 16)
        if ifFraction:
            print('='+decimalValue+fraction(fractionValue, 16, 10))
            print('=0b'+decimal_to(decimalValue, 2)+fraction(fractionValue, 16, 2))
            print('=0o', decimal_to(decimalValue, 8)+fraction(fractionValue, 16, 8))
        else:
            print('='+decimalValue)
            print('=0b'+decimal_to(decimalValue, 2))
            print('=0o',decimal_to(decimalValue, 8))
    if prefix == 8:
        decimalValue = to_decimal(integer, 8)
        if ifFraction:
            print('='+decimalValue+fraction(fractionValue, 8, 10))
            print('=0b'+decimal_to(decimalValue, 2)+fraction(fractionValue, 8, 2))
            print('=0x', decimal_to(decimalValue, 16)+fraction(fractionValue, 8, 16))
        else:
            print('='+decimalValue)
            print('=0b'+decimal_to(decimalValue, 2))
            print('=0x', decimal_to(decimalValue, 16))
    if prefix == 2:
        decimalValue = to_decimal(integer, 2)
        if ifFraction:
            print('='+decimalValue+fraction(fractionValue, 2, 10))
            print('=0x'+decimal_to(decimalValue, 16)+fraction(fractionValue, 2, 16))
            print('=0o', decimal_to(decimalValue, 8)+fraction(fractionValue, 2, 8))
        else:
            print('='+decimalValue)
            print('=0x'+decimal_to(decimalValue, 16))
            print('=0o'+decimal_to(decimalValue, 8))  # using ',' leads to a blank space between prefix and number
    if input('Type t to terminate the programme, and type others to continue the programme') == 't':
        break