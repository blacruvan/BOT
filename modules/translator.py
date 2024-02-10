def translate(texto):
    from translate import Translator
    translator = Translator(to_lang="es")
    translation = translator.translate(texto)
    return translation