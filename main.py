from string import ascii_letters as alpha

alpha_tuple = tuple(alpha)

def caesar_cipher(data, key):
    try:
        output = ''
        for letters in data:
            if letters in alpha_tuple:
                offset = alpha_tuple.index(letters) + key
                if offset >= len(alpha_tuple):
                    offset = offset - len(alpha_tuple)
                output = output + alpha_tuple[offset]
            else:
                output = output + letters
        return output
    except:
        print('бля')



if __name__ == '__main__':
    text = input('Введите текст')
    key = input('Введите ключ')
    data = list(text)
    key = int(key)
    out = caesar_cipher(data, key)
    print(out)


