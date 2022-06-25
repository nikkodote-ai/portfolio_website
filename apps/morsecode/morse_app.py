"""Convert user input to Morse Code and vice versa"""

import requests
#get morse code from web
class MorseCoder:
    def __init__(self):
        self.morse_code_link = 'https://math.hws.edu/eck/cs225/s03/code.txt'
        self.response = requests.get(self.morse_code_link).text.split('\n')
        self.morse_code_dict = {letter.split(' ')[0]: letter.strip().split(' ')[-1] for letter in self.response}
        #convert characters that can't be parse straight away
        self.morse_code_dict[' '] = '/'
        self.morse_code_dict["'"] = '.----.'
        self.morse_texts = ['-', '.', '/', ' ']


def translate(raw_input):
    morse_coder = MorseCoder()
    output = ''
    # automatically convert morse or not to it's counter code.
    # if the input is likely to be morse, encrypt as morse, else, decrypt.
    likely_normal = (sum([raw_input.count(i) for i in morse_coder.morse_texts]) / len(raw_input))

    #encrypt to morse because the input is likely to be normal text
    if  likely_normal < 0.9:
        for i in raw_input:
            try:
                output+= morse_coder.morse_code_dict[i.upper()] + ' '
            except KeyError:
                output = f'{i} Not Found'
        return output

    #else, decrypt because this is likely to be Morse code
    else:
        for i in raw_input.split(' '):
            for key,value in morse_coder.morse_code_dict.items():
                if value == i:
                    output+= key
        output = output.title()
        return output
