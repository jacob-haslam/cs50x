from cs50 import get_string

text = get_string("Text: ")

letters = 0
words = 1
sentences = 0

for i in range(len(text)):
    if text[i] >= 'A' and text[i] <= 'z':
        letters += 1
    elif text[i] == ' ':
        words += 1
    elif text[i] == '.' or text[i] == '?' or text[i] == '!':
        sentences += 1

    l = (letters / words) * 100
    s = (sentences / words) * 100

    index = 0.0588 * l - 0.296 * s - 15.8

if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print("Grade ", round(index))

