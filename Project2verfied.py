import sys
import numpy as np
import matplotlib.pyplot as plt


m0 = 9450 #MeV
s0 = 54 #MeV

m1 = 10023
s1 = 25


def h0(sigdetector):
        mu = np.random.normal(m0, s0) #true measurements
        x0 = np.random.normal(mu,sigdetector) #detector measurements
        return x0 

def h1(sigdetector):
        mu1 = np.random.normal(m1, s1) 
        x1 = np.random.normal(mu1,sigdetector) 
        return x1


# import our Random class from python/Random.py file
sys.path.append(".")





# main function for our coin toss Python code
if __name__ == "__main__":
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [-seed number]" % sys.argv[0])
        print
        sys.exit(1)

    # default seed
    # default number of coin tosses (per experiment)
    Nmeas = 1

    # default number of experiments
    Nexp = 1

    #default sigma detector
    sigdetect = 2000

    # output file defaults
    doOutputFile = False

    # read the user-provided seed from the command line (if there)
    if '-Nmeas' in sys.argv:
        p = sys.argv.index('-Ntoss')
        Nt = int(sys.argv[p+1])
        if Nt > 0:
            Ntoss = Nt
    if '-Nexp' in sys.argv:
        p = sys.argv.index('-Nexp')
        Ne = int(sys.argv[p+1])
        if Ne > 0:
            Nexp = Ne
    if '-output' in sys.argv:
        p = sys.argv.index('-output')
        OutputFileName = sys.argv[p+1]
        doOutputFile = True
    if '-sigdetect' in sys.argv:
        p = sys.argv.index('sigdetect')
        sd = int(sys.argv[p+1])

    x0list = [] #generating random x cooridantes for H0
    for i in range(1, Nexp):
            y0 = h0(sigdetect)
            x0list.append(y0)


    x1list = [] #generating random x cooridnate for H1
    for i in range(1, Nexp): 
            y1 = h1(sigdetect) 
            x1list.append(y1)

    
    n0, bin0, _ = plt.hist(x0list, bins= 50, density = True)
    n1, bin1, _ = plt.hist(x1list, bins= 50, density = True)

#gets the probability from the bin
    def bincontent(bin, value, list):
            for j in range(len(bin)):
                    if bin[j-1] <= value < bin[j]:
                            return list[j-1]


    LLR1 = []
    for i in range(1, Nexp):
            LLR = 0 
            for m in range(1,Nmeas):
                    y = h0(sigdetect) 
                    p1 = bincontent(bin1, y, n1)
                    p0 = bincontent(bin0, y, n0)
                    if p1 is None:   #This is to correct for any values of 0 or none because you can't add an interger to none or arrays
                            p1 = 0.000001
                    if p0 is None:
                            p0 = 0.000001
                    if p0 == 0:          #avoid any divisions by zero
                            p0 = 0.000001
                    if p1 == 0:
                            p1 = 0.000001
                    LLR += np.log(p0/p1)
            LLR1.append(LLR)

print(LLR1)
