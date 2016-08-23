#! python3
'''
pnea.py - 
Finds phone numbers and email addresses in a .txt file or on the clipboard and writes the results in a .txt file

Successful Search for the following patterns of:
    Phone Numbers               Email Addresses

	000-000-0000                username@domainname.xx
	000 000 0000                username@domainname.xxx
	000.000.0000                username@domainname.xxxx

	(000)000-0000
	(000)000 0000
	(000)000.0000
	(000)0000000
	(000) 000 0000
	(000) 000.0000

	000-0000
	000 0000
	000.0000

	0000000
	0000000000
	(000)0000000
'''

import pyperclip, re

phoneRegex = re.compile(r'''(
    (\d{3})[-\.\s]?                     # area code and optional separator
    (\d{3})[-\.\s]?                     # first 3 digits and optional separator
    (\d{4})|                            # last 4 digits
    \((\d{3})\)\s*                      # (area code) and zero or more spaces
    (\d{3})[-\.\s]?                     # first 3 digits and optional separator
    (\d{4})|                            # last 4 digits
    (\d{3})[-\.\s]?                     # first 3 digits and optional separator
    (\d{4})                             # last 4 digits
    )''', re.VERBOSE)

emailRegex =  re.compile(r'''(
    [a-zA-Z0-9._%+-]+                   # username
    @                                   # 'at' symbol
    [a-zA-Z0-9.-]+                      # domain name
    (\.[a-zA-Z]{2,4})                   # dot - something
    )''', re.VERBOSE)

while True:
    prompt = input('Get data from a .txt File or from Clipboard? [f/c]: ')
    if prompt.lower() == 'f' or prompt.lower() == 'c':
        break
    else:
        print ('Please type \'f\' or \'c\' \n')

if prompt.lower() == 'f':
    # Opening .txt file
    textFile = input('Enter the name of the .txt file: ')
    text = open('C:\\textFiles\\' + textFile + '.txt')
    textContent = text.read()
    text.close()
else:
    textContent = str(pyperclip.paste())

# Matching with RegEx
matchesPhone = []
matchesEmail = []
for groups in phoneRegex.findall(textContent):
    if groups[1] == '':
        if groups[4] == '':
            phoneNum = '-'.join([groups[7], groups[8]])
        else:
            phoneNum = '-'.join([groups[4], groups[5], groups[6]])
    else:
        phoneNum = '-'.join([groups[1], groups[2], groups[3]])
    matchesPhone.append(phoneNum)
for groups in emailRegex.findall(textContent):
    matchesEmail.append(groups[0])

# Writing the results
if len(matchesPhone) > 0 or len(matchesEmail) > 0:
    newTextFile = open('C:\\textFiles\\phonesandemailsoutput.txt', 'a')
    newTextFile.write('PHONE NUMBERS & EMAIL ADDRESSES'.center(40, '-') + '\n')
    if len(matchesPhone) == 0:
        warning = 'No Phone Numbers in the ' + textFile + '.txt'
        newTextFile.write(warning.center(40, '*') + '\n')
    else:
        newTextFile.write(' ' * 11 + 'Phone Numbers'.center(17, '_') + ' ' * 12 + '\n')
        newTextFile.write('\n'.join(matchesPhone) + '\n')
    if len(matchesEmail) == 0:
        warning = 'No Email Addresses in the ' + textFile + '.txt'
        newTextFile.write(warning.center(40, '*') + '\n\n')
    else:
        newTextFile.write(' ' * 10 + 'Email Addresses'.center(19, '_') + ' ' * 11 + '\n')
        newTextFile.write('\n'.join(matchesEmail) + '\n\n')
    newTextFile.close()

print ('\nSuccessful Search for Phone Numbers and Email Addresses')
print ('Check phonesandemailsoutput.txt in directory C')
