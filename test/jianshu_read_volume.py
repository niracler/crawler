from selenium import webdriver
import time
import requests
import threading


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        visit(self.name, self.counter)
        print("退出线程：" + self.name)

def visit(name, counter):
    while counter:
        browser = webdriver.Chrome()
        browser.get('https://www.jianshu.com/p/fd2bdf5b0c43')
        # browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        # browser.execute_script('alert("To Bottom")')
        time.sleep(1)
        browser.close()
        counter -= 1

threads = []
for i in range(10):
    threads.append(myThread(1, "thread-{}".format(i), 15))

for i in range(len(threads)):
    threads[i].start()
for i in range(len(threads)):
    threads[i].join()
print('退出主线程')
