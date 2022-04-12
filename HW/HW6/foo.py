import re
str1 = "Hello this is so and so calling from the hotline. from-you please call us back at 888-888-8888 for $800"
regex = re.compile(
    r'([A-Za-z$!]+)|[$ ]?([0-9]+)')
for line in regex.findall(str1):
    print(line[0])
