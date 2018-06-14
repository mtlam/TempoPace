#Michael Lam 1/10/2012

class Time:
    def __init__(self,string):
        if type(string) == type(0.0) or type(string) == type(0): #You have been given Time(seconds)
            self.hour = int(string) / 3600
            string -= self.hour*3600
            self.minute = int(string) / 60
            string -= self.minute*60
            self.second = string
            return
        tup=string.split(':')
        if len(tup)==3:
            self.hour=int(tup[0])
            self.minute=int(tup[1])
            self.second=float(tup[2])
        else:
            self.hour=0
            self.minute=int(tup[0])
            self.second=float(tup[1])
    def __add__(self,other): # Number of seconds
        return Time(self.getseconds() + other.getseconds())
    def __sub__(self,other):
        return Time(self.getseconds() - other.getseconds())
    def __mul__(self,other):
        return Time(self.getseconds() * other.getseconds())
    def __div__(self,other):
        return Time(self.getseconds() / other.getseconds())
    def __cmp__(self,other):
        return self.getseconds() - other.getseconds()
    def __repr__(self):
        if self.second < 10:
            second = "0" + str(self.second)
        else:
            second = str(self.second)
        minute = str(self.minute)
        if self.hour == 0:
            return "%s:%s" % (minute,second)
        if self.minute < 10:
            minute = "0" + str(self.minute)
        else:
            minute = str(self.minute)
        hour=str(self.hour)
        return "%s:%s:%s" % (hour,minute,second)
    def getseconds(self):
        return self.hour*60*60 + self.minute*60 + self.second
    def addSeconds(self,other):
        return Time(self.getseconds() + other)
   
       

#Instead of solving for f(x,y), solve for y
def bilinearinterpolation(x,y):
    #Solve for x1,y1,x2,y2
    f=fixchart()
    if x in totaltimes:
        x1=totaltimes[totaltimes.index(x)]
        x2=x1
    else:
        for i in range(len(totaltimes)-1):
            if x<totaltimes[i+1] and x>totaltimes[i]:
                x1=totaltimes[i]
                x2=totaltimes[i+1]
    if x>=totaltimes[-1] or x<=totaltimes[0] or x2==x1: #End of the chart!
        if x>=totaltimes[-1]:
            index=-1
            print "Warning: End of chart. Using maximum values given."
        elif x<=totaltimes[0]:
            index=0
            print "Warning: End of chart. Using minimum values given."
        else:
            index=totaltimes.index(x1)
        for i in range(len(twentymark)-1):
            y1=f[i][index]
            y2=f[i+1][index]
            if y <= y1 and y >= y2:
                yi1=i
                yi2=i+1
                break
        ypercent=(y.getseconds()-y2.getseconds())/(y1.getseconds()-y2.getseconds())
        vdot = (vdots[yi1]-vdots[yi2])*ypercent + vdots[yi2]
        return vdot

    xi1=totaltimes.index(x1)
    xi2=totaltimes.index(x2)
    for i in range(len(twentymark)-1):
        y11 = f[i][xi1]
        y12 = f[i][xi2]
        y21 = f[i+1][xi1]
        y22 = f[i+1][xi2]
        if y <= y11 and y >= y22: #Equalities?
            yi1=i
            yi2=i+1
            break
    xpercent=(x.getseconds()-x1.getseconds())/(x2.getseconds()-x1.getseconds())
    y1 = Time((y12.getseconds()-y11.getseconds())*xpercent + y11.getseconds())
    y2 = Time((y22.getseconds()-y21.getseconds())*xpercent + y21.getseconds())
    ypercent=(y.getseconds()-y2.getseconds())/(y1.getseconds()-y2.getseconds())
    vdot = (vdots[yi1]-vdots[yi2])*ypercent + vdots[yi2]
    return vdot
     
       


def fixchart():
    newchart = []
    for i in range(len(chart)):
        newchart.append(map(lambda x: twentymark[i].addSeconds(x),chart[i]))
    return newchart

#20:00-25-30-35-40-45-50-55-60 minutes
chart=[[0,7,13,16,19,22,25,28,32], #vdot=30
 [0,6,12,15,18,21,24,27,30], #35
 [0,6,11,14,17,20,22,24,26], #40
 [0,6,10,13,15,17,19,21,23], #45
 [0,5,9,12,14,16,18,20,22], #50
 [0,5,8,11,13,15,17,19,21], #55
 [0,5,7,10,12,14,16,18,21], #60
 [0,5,7,9,11,13,16,18,20], #65
 [0,4,6,8,10,12,15,18,19], #70
 [0,4,6,8,10,12,14,15,17], #75
 [0,3,5,7,9,11,12,14,16], #80
 [0,3,5,7,9,11,12,14,15]] #85

vdots=[30,35,40,45,50,55,60,65,70,75,80,85]
twentymark=[Time('10:18'),Time('9:07'),Time('8:12'),Time('7:25'),Time('6:51'),
            Time('6:20'),Time('5:54'),Time('5:32'),Time('5:13'),Time('4:56'),
            Time('4:41'),Time('4:27')]

totaltimes=[Time('20:00'),Time('25:00'),Time('30:00'),Time('35:00'),Time('40:00'),
            Time('45:00'),Time('50:00'),Time('55:00'),Time('60:00')]

##for row in fixchart():
##    print row
##bilinearinterpolation(Time('24:19'),Time('6:04.75'))

def main():
    print "Jack Daniels' Tempo Pace Utility"
    print "Determine your VDOT for extended tempo runs\n"
    while True:
        x=raw_input("Total run time (mm:ss or hh:mm:ss): ")
        y=input("Miles: ")
        x=Time(x)
        pace=Time(x.getseconds()/y)
        print "Pace: "+str(pace)
        print "VDOT: %0.2f" % (bilinearinterpolation(x,pace))
        wait=raw_input('Do you want to calculate another? (y/n) ')
        if wait.lower()=='y' or wait.lower()=='yes':
            continue
        else:
            break
main()
