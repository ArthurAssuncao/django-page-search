from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.conf import settings
import os
import re


def search(request, quantity_characters=2, replace_text={}):
    try:
        search_words = request.GET['search']
        search_words = search_words.encode('utf-8')
    except KeyError:
        search_words = None
    search_result = []
    content = 'NO'
    arg = 'NO'
    q_c = 'NO'
    if search_words is not None:
        arg = 'OK'
        if len(search_words) > quantity_characters:
            q_c = 'OK'
            regex_search_words_str = r'>([^({{)({{%)(}})]*?{0}[^({{)(%}})(}})]*?)<';  # removi >< da primeira parte e <> da segunda parte
            for diretorio in settings.TEMPLATE_DIRS:
                for arquivo in os.listdir(diretorio):
                    with open(diretorio + '/' + arquivo) as arquivo_search_words:
                        content_arquivo_search_words = arquivo_search_words.read()
                        content_arquivo_search_words = replaces_constant_text(content_arquivo_search_words, replace_text)
                        regex_search_words = re.compile(regex_search_words_str.format(search_words), re.IGNORECASE)
                        resultados_search_words = re.search(regex_search_words, content_arquivo_search_words)
                        if resultados_search_words is not None and 'template' not in diretorio:
                            search_result.append( {'URL': arquivo.split(".html")[0], 'TEXT': resultados_search_words.groups()[0] })
                            content = 'OK'
    rq = RequestContext(request, {
        'search_result': search_result,
        'search_words': search_words,
        'argument_check': arg,
        'content_check': content,
        'quantity_characters': quantity_characters,
        'quantity_characters_check': q_c
    })
    return rq


def replaces_constant_text(text, replace_text):
    for key in replace_text:
        if key in text:
            text = text.replace(key, replace_text[key])
    return text