#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WAR   RANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os
import urllib
from urllib.parse import urlparse
import urllib.request
import json
import time
from optparse import OptionParser

def _translate_apertium(text, pair):

    src_lang, tgt_lang = pair.split("-")

    # Request translation
    url = f"https://www.softcatala.org/apertium/json/translate?langpair={src_lang}|{tgt_lang}&markUnknown=no"
    url += "&q=" + urllib.parse.quote_plus(text.encode('utf-8'))
    #print("url->" + url)

    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        translated =  data['responseData']['translatedText']
        return translated

    except Exception as e:
        print("ERROR: calling _get_translation: " + str(e))
        time.sleep(5)
        return ""

def _translate_apertium_en_ca2(english):
    with open("input.txt", "w") as text_file:
        text_file.write(english)
        text_file.close()

    cmd = "apertium eng-cat -u input.txt output.txt"
    os.system(cmd)

    with open ("output.txt", "r") as myfile:
        line_list = myfile.readlines()
        translation = ' '.join([str(elem) for elem in line_list]) 
        translation = translation.replace('\n', '')
#        print("text->" + text)
#        print("cmd->" + cmd)
#        print("translation->" + translation)
#        print("translation raw->" + str(line_list))
        return translation

def _translate_text_yandex(text, key, pair):

    SERVER = "https://translate.yandex.net/api/v1.5/tr.json"
    url = "{0}/translate?lang={1}&format=plain&key={2}".format(SERVER, pair, key)
    url += "&text=" + urllib.parse.quote_plus(text.encode('utf-8'))
    response = urllib.request.urlopen(url)
    r = response.read().decode("utf-8")
    data = json.loads(r)
    all_text = ''

    texts = data['text']
    for text in texts:
        all_text += text
    return all_text.rstrip()

def _translate_text_google(text, key, pair):

    SERVER = "https://translation.googleapis.com/language/translate/v2"

    src_lang, tgt_lang = pair.split("-")

    url = f"{SERVER}/?key={key}&source={src_lang}&target={tgt_lang}"
    url += "&q=" + urllib.parse.quote_plus(text.encode('utf-8'))
    response = urllib.request.urlopen(url)
    r = response.read().decode("utf-8")
    data = json.loads(r)
    translated = data['data']['translations'][0]
    translated = translated['translatedText']
    translated = translated.replace("&#39;", "'")
    return translated.rstrip()


def apertium(source, target, pair):

    strings = 0
    with open(source, 'r') as tf_en, open(target, 'w') as tf_ca:
        en_strings = tf_en.readlines()
    
        for string in en_strings:
            translated = _translate_apertium(string, pair)
            tf_ca.write("{0}\n".format(translated))
            strings = strings + 1

        if strings % 100:
            print(strings)
            time.sleep(60)

    print("Translated {0} strings".format(strings))

def yandex(source, target, key, pair):

    print("Translating using Yandex")

    strings = 0
    with open(source, 'r') as tf_en, open(target, 'w') as tf_ca:
        en_strings = tf_en.readlines()
    
        cnt = 0
        for string in en_strings:
            cnt = cnt + 1
    
            translated = _translate_text_yandex(string, key, pair)
            tf_ca.write("{0}\n".format(translated))
            strings = strings + 1

    print("Translated {0} strings".format(strings))

def google(source, target, key, pair):

    print("Translating using Google")

    strings = 0
    with open(source, 'r') as tf_en, open(target, 'w') as tf_ca:
        en_strings = tf_en.readlines()
    
        cnt = 0
        for string in en_strings:
            cnt = cnt + 1
    
#            if cnt > 30:
#                break

            try:
                translated = _translate_text_google(string, key, pair)
                tf_ca.write("{0}\n".format(translated))
                strings = strings + 1

            except Exception as e:
                print(e)
                print(string)

                translated = 'Error'
                tf_ca.write("{0}\n".format(translated))
                strings = strings + 1

    print("Translated {0} strings".format(strings))


def read_parameters():
    parser = OptionParser()

    parser.add_option(
        '-e',
        '--engine',
        action='store',
        type='string',
        dest='engine',
        default='',
        help='Translation engine to use'
    )

    parser.add_option(
        '-k',
        '--key',
        action='store',
        type='string',
        dest='key',
        default='',
        help='API Key to use (if applies)'
    )

    parser.add_option(
        '-p',
        '--pair',
        action='store',
        type='string',
        dest='pair',
        default='',
        help='Language pair in format source-target'
    )

    parser.add_option(
        '-s',
        '--source',
        action='store',
        type='string',
        dest='source',
        default='',
        help='Source file to translate'
    )

    parser.add_option(
        '-t',
        '--target',
        action='store',
        type='string',
        dest='target',
        default='',
        help='Translated target file'
    )


    (options, args) = parser.parse_args()

    return options.engine, options.key, options.pair, options.source, options.target



def main():

    print("Translate text files for evaluation using different engines")

    engine, key, pair, source, target = read_parameters()

    engine = engine.lower()
    if engine == 'yandex':
        yandex(source, target, key, pair)
    elif engine == 'google':
        google(source, target, key, pair)
    elif engine == 'apertium':
        apertium(source, target, pair)
    else:
        print(f"Translation engine '{engine}' not supported")

    return

if __name__ == "__main__":
    main()
