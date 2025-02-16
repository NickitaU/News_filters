from django import template


register = template.Library()


CURRENCIES_SYMBOLS = {
   'rub': 'Р',
   'usd': '$',
}


@register.filter()
def currency(value, code='rub'):
   """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   postfix = CURRENCIES_SYMBOLS[code]

   return f'{value} {postfix}'

@register.filter
def censor(text):
    bad_words_list = ["Редиска", "редиска"]
    for bad_word in bad_words_list:
        text = text.replace(bad_word, '*' * len(bad_word))
    return text

