import math


def text2num(text):
    text = text.replace(
        u'壹', '1').replace(u'贰', '2').replace(u'叁', '3').replace(u'肆', '4').replace(u'伍', '5').replace(
        u'陆', '6').replace(u'柒', '7').replace(u'捌', '8').replace(u'玖', '9').replace(u'拾', u'十').replace(
        u'佰', u'百').replace(u'仟', u'千').replace(u'负', '-').replace(
        u'一', '1').replace(u'二', '2').replace(u'三', '3').replace(u'四', '4').replace(u'五', '5').replace(
        u'六', '6').replace(u'七', '7').replace(u'八', '8').replace(u'九', '9').replace(u'两', '2').replace(u'零', '0')
    num = 0
    shi, bai, qian, wan, yi = [1 for _ in range(5)]
    d = 1
    for i in text[::-1]:
        try:  # when i is int type
            num += int(i) * d * shi * bai * qian * wan * yi
            d *= 10
        except ValueError:  # when type is str type, eg: 十百千万亿点
            if i == u'十':
                shi *= 10
            if i == u'百':
                shi = 1
                bai *= 100
            if i == u'千':
                shi, bai = [1] * 2
                qian *= 1000
            if i == u'万':
                shi, bai, qian = [1] * 3
                wan *= int(1e4)
            if i == u'亿':
                shi, bai, qian, wan = [1] * 4
                yi *= int(1e8)
            if i == '.' or i == u'点':
                num /= d
            if i == '-':
                num = -num
                continue
            d = 1

    if d == 1:  # when d = 1, meaning that the last operation didn't be added, eg: 十1亿, operation u'十' will be ignored
        num += 1 * d * shi * bai * qian * wan * yi

    return str(num)


def num2text(num):
    num = float(num)
    text = ''

    # int type
    a = int(num)
    i = 0
    while a // 1 > 0:
        if i % 4 == 1:
            text += '十'
        elif i % 4 == 2:
            text += '百'
        elif i % 4 == 3:
            text += '千'
        elif i != 0 and i % 8 == 0:
            text += '亿'
        elif i != 0 and i % 4 == 0:
            text += '万'
        n = a % 10
        text += str(n)
        a //= 10
        i += 1
    if num < 0:
        if text == '':
            text += '零'
        text += '负'
    text = text[::-1]  # the text is reversed, we must reverse again
    while text != '' and text[-1] == '0':
        text = text[:-1]

    # float type
    a = str(num).split(str(int(num)) + '.')  # keep precision, only 7-bit precision, eg: 0.0123456789 -> 0.0123456
    if len(a) == 2:
        if text == '':
            text += '零'
        text += '点' + a[1]

    return text.replace('1', u'一').replace('2', u'二').replace('3', u'三').replace(
        '4', u'四').replace('5', u'五').replace('6', u'六').replace('7', u'七').replace(
        '8', u'八').replace('9', u'九').replace('0', u'零')


if __name__ == '__main__':
    num = '01234567890.0123456'
    text = num2text(num)
    print(text)
    print(text2num(text))

    num = '0.'
    text = num2text(num)
    print(text)
    print(text2num(text))

    num = '-0.1234'
    text = num2text(num)
    print(text)
    print(text2num(text))
