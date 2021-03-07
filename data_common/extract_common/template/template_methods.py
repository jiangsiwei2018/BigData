# encoding=utf-8

class TemplateMethods:

    @staticmethod
    def process_text(text, *args, **kwargs):
        print(f'title: {text}')