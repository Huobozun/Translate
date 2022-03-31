from googletrans import Translator

translator = Translator(service_urls=['translate.google.cn'])
text='Locally advanced'
print(translator.translate(text, dest='zh-cn', src='auto'))