###### gerekli kutuphaneler ###### - LoadShifting + Winter
import pandas as pd
from pysolar import radiation
from pysolar.solar import *
import openpyxl
import datetime
import scipy
import numpy as np
from matplotlib import pyplot as plt

#ev gunluk tuketimi #12kwh
#batarya kap. 6kwh
###### excel okuma ######

excel = pd.read_excel("degerler.xlsx").iloc[:, 1:]

buzdolabi = excel['buzdolabi']
camasir = excel['camasir']
bulasik = excel['bulasik']
camasirkur = excel['camasirkur']
d_dondurucu = excel['d_dondurucu']
elksup = excel['elksup']
termosifon = excel['termosifon']
tv = excel['tv']
bilgisayar = excel['bilgisayar']
firin = excel['firin']
aydinlatma = excel['aydinlatma']
mikrodalga = excel['mikrodalga']
kettle = excel['kettle']
davlumbaz = excel['davlumbaz']
sackuru = excel['sackuru']
klima = excel['klima']


###### zaman ve yuk tanimlama ######
zaman1 = np.arange(1,25)
# a = np.ones((25), dtype=np.int16)
# b = np.zeros((25), dtype=np.int16)
# x=17
# y=20
# b[int(x):int(y)]=2
# totaltime=a+b

########## Solar Radyasyon Verisi Alma - SolarPy
latitude_deg = 36.884 # positive in the northern hemisphere
longitude_deg = -30.704 # negative reckoning west from prime meridian in Antalya, Turkey
date = datetime.datetime(2007, 2, 18, 15, 13, 1, 130320, tzinfo=datetime.timezone.utc)
altitude_deg = get_altitude(latitude_deg, longitude_deg, date)
solarradyasyon= radiation.get_radiation_direct(date, altitude_deg)
########### Solar Radyasyon Verisi Alma - SolarPy

########### PV Panel Enerji Uretim Hesabi
#  E = A * r * H * PR

#E = Energy (kWh)
#A = Total solar panel Area (m2)
#r = solar panel yield or efficiency(%)
#H = Annual average solar radiation on tilted panels (shadings not included)
#PR = Performance ratio, coefficient for losses (range between 0.5 and 0.9, default value = 0.75)
###########
a= 17.94  #Boyut: 1956 × 992 × 40mm # Adet : 10
r= 0.15
h= solarradyasyon
pr= 0.75
pv_ye= a*r*h*pr   ###Yıllık Üretim
pv_e = pv_ye/365  ###Günlük üretim

##Batarya Enerji Depolama
bat_time = np.ones(24, dtype = np.float16)
bat_time[0:8]=0
bat_time[8]=pv_e*(0.035)
bat_time[9]=pv_e*(0.0864)
bat_time[10]=pv_e*(0.108)
bat_time[11]=pv_e*(0.103)
bat_time[12]=pv_e*(0.126)
bat_time[13]=pv_e*(0.118)
bat_time[14]=pv_e*(0.110)
bat_time[15]=pv_e*(0.0960)
bat_time[16]=pv_e*(0.0930)
bat_time[17]=pv_e*(0.0819)
bat_time[18]=pv_e*(0.0351)
bat_time[18:24]=0
##Batarya Enerji Depolama
o=0
##Şebekeden Çekilen Enerji Miktarı
totaltime = np.zeros(24, dtype = np.float16)
for i in range(24):
    totaltime[o]= buzdolabi[o]+camasir[o]+bulasik[o]+camasirkur[o]+d_dondurucu[o]+elksup[o]+termosifon[o]+tv[o]+bilgisayar[o]+firin[o]+aydinlatma[o]+mikrodalga[o]+kettle[o]+davlumbaz[o]+sackuru[o]+klima[o]
    o=o+1


threshold=np.sum(totaltime)/12
##Şebekeden Çekilen Enerji Miktarı

###toplamyuk
pb= input("Tuketimin artmaya basladigi saati giriniz: ")
p_baslangic=int(pb)
p_surec=input("Bu tuketim kac saat suruyor?: ")
p_bitis=int(p_baslangic)+int(p_surec)  ###Tuketimin azaldigi saat (Uyku saati)
sayac=0
totaltime_s=totaltime
battery=1
enerjisatis=6
bsay=8
for i in range(10):
    battery = battery+(bat_time[bsay])
    bsay= bsay + 1
    if battery > 6:
        enerjisatis = battery-enerjisatis
        battery = 6
    elif battery == 6:
        battery = 6

bastuketim=totaltime

#for i in range(int(p_surec))
 #   if


if enerjisatis == 6:
    enerjisatis=0

a = np.ones(24, dtype=int)
#index olustur
for i in range(24):
    if totaltime[i] > threshold and i==18:





for i in range(int(p_surec)+1):
    index = totaltime[int(p_baslangic)+i:int(p_bitis)]
    # if not np.all(index == 1):   ##indexten çıkıp totaltime_s'imizi düz modüle eşitleyelim ve bir sayac ciktisi alalim
    if np.sum(index) != int(p_surec) - i:
        sayac = sayac + 1
        totaltime_s = a

########sayac 24'den büyük olma problemini matlabdeki 24den büyük olma durumunda
# direk 3 arkaya atması emrini vererek çözdüm # değilse de sayac ve 3 saatlik triple tariff arasında yazdırdm
x = int(p_baslangic)
y = int(p_bitis)

if sayac != 0:
    if y + sayac > 24:
        totaltime_s[y : y + 3] = 3
    else:
        totaltime_s[y + sayac : y + sayac + 3] = 3

plt.title("Enerji Uretim Grafigi")
plt.plot(zaman1, bat_time, color = 'royalblue', label= 'kwH')
plt.xlabel("Zaman")
plt.ylabel("Yük")
plt.legend()
plt.show()

aylikkar=enerjisatis*0.26*30
toplamtuketim=np.sum(totaltime)
shiftedtuketim=np.sum(totaltime_s)
pvuretim=np.sum(bat_time)


plt.title("LoadShifting Grafigi")
plt.bar(zaman1, totaltime_s, color = 'tab:red', align = 'center', label= 'Shifted')
plt.bar(zaman1, totaltime, color = 'tab:blue', align = 'center', label= 'Not Shifted')
plt.ylabel("Yük")
plt.legend()
plt.show()

print("Toplam kaydırılan yük: {}" .format(sayac))
print("Loadshifting uygulanmadan önce: {}".format(totaltime))
print("Loadshifting uygulandıktan sonra: {}".format(totaltime_s))





#####Koray Göksu 18012116
