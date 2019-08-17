from selectolax.parser import HTMLParser
from typing import List


def parse_files(files: List[str], names: List[str]) -> List[str]:
    messages = []
    for file_name in files:
        with open(file_name) as file:
            body = file.read()

        messages += parse(body, names)

    return messages


def parse(body: str, names: List[str]) -> List[str]:
    messages = []
    for node in HTMLParser(body).css('div.msg_item'):
        if node.css_first('div.from').css_first('b').text() in names:
            subnode = node.css_first('div.msg_body')
            if subnode is None:
                continue

            text = subnode.text()
            print(text)
            messages.append(text)

    return messages


if __name__ == '__main__':
    files = ['history.html', 'history_ls.html', 'history_potok.html']
    names = ['Anton Morozov']

    messages = parse_files(files, names)
    print(len(messages))

    with open('quotes.txt', 'w') as output:
        for message in messages:
            output.write(message + '\n')
