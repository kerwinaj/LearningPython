#!/usr/bin/python
# coding:utf-8

__author__ = 'kerwinaj'

# Hello World!
print ("hello world");


# 基本数据类型
a = 10;
print a;
print type(a);

a = 1.3
print a, type(a);

a = True;
print a, type(a);

a = 'hello world !';
print a, type(a);

s = '''This is a multi-line string.
This is the second line.'''
print s, type(s);

s = 'This is a "string". \
This continues the string.'
print s, type(s);

s = "This is a 'string'. \
This continues the string."
print s, type(s);

s = "This is a \"string\". \
This continues the string."
print s, type(s);

a = r'你好，中国';
print a, type(a);
print(a, type(a));

# 序列

# 控制语句
number = 23
running = True
while running:
    guess = int(raw_input('Enter an integer : '))
    if guess == number:
        print 'Congratulations, you guessed it.' # New block starts here
        print "(but you do not win any prizes!)" # New block ends here
        running = False;
    elif 1 == guess:
        break;
    elif 0 == guess:
        continue;
    elif guess < number:
        print 'No, it is a little higher than that' # Another block
    else:
        print 'No, it is a little lower than that'
        # you must have guess > number to reach here
print ('while Done')

# for..in循环对于任何序列都适用
print (range(1, 5)); # [1, 2, 3, 4]
for i in range(1, 5):
    print i
print ('for done')

for i in [1,2,3,4]:
    if i == 2:
        continue;
    print i
    if i == 3:
        print ("i will be out")
        break;
print ('for done')



# function
def sayHello():
    print ("hello world by sayHello")

sayHello();

def printMax(a, b):
    if a>b :
        print (a, "a is maximum")
        print a, "a is maximum"
    else:
        print (b, "b is maximum")
        print b, "b is maxmium"
    a =100;
    print(a)

a= 3;
printMax(a,5);
print(a)
