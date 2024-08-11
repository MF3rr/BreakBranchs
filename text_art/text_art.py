from pyfiglet import Figlet


def art_text(text):
    f = Figlet(font='banner')
    return f.renderText(text)

# use example
text = str(input('Insira o texto a ser formatado aqui: '))
print(art_text(text))
