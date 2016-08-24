#! python3
'''
pnea.py - 
Finds Phone Numbers and Email Addresses on the clipboard
Writes the results in a .txt file, stored inside folder textFiles, in directory C (Windows/OS X) or in root directory (Linux)

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

import pyperclip, re, os, platform

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

print ('Copy the text you wish to extract Phone Numbers and Email Addresses from!')
input('Press Enter when ready: ')
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

# Create the folder to store the extracted data .txt to, if it doesn't exist
if platform.system() == 'Linux':
    ospath = '/textFiles'
    if not os.path.exists(ospath):
        os.makedirs(ospath)
else:
    ospath = 'C' + os.path.join(':', 'textFiles')
    if not os.path.exists(ospath):
        os.makedirs(ospath)
ospath = os.path.join(ospath, 'phonesandemailsoutput.txt')

# Writing the results
if len(matchesPhone) > 0 or len(matchesEmail) > 0:
    newTextFile = open(ospath, 'a')
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
if platform.system() == 'Linux':
    print ('Check phonesandemailsoutput.txt, inside folder textFiles, in root directory')
else:
    print ('Check phonesandemailsoutput.txt, inside folder textFiles, in directory C')
