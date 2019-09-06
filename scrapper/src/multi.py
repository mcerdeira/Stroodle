from multiprocessing import Process, Pool

def AA(name):
    print("AA" + name)

def BB(name):
    print('hello', name)
    AA(name)

if __name__ == '__main__':
    p = []
    for i in range(12):
        p.append(Process(target=BB, args=('bob' + str(i),)))
        p[i].start()

    for i in range(12):
        p[i].join()
    
    print ("DONE")