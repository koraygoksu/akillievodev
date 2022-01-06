###### gerekli kutuphaneler ######   Summer   #####
import pandas as pd
from pysolar import radiation
from pysolar.solar import *
import openpyxl
import datetime
import numpy as np
from matplotlib import pyplot as plt

#batarya kap. 6kwh
###### excel okuma ######

excel = pd.read_excel("degerler.xlsx", engine="openpyxl").iloc[:, 1:]

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
esarj = excel['esarj']
sarjaleti = excel['sarjaleti']

###### zaman ve yuk tanimlama ######
radyasyon= np.ones(30, dtype= np.float16)
zaman1 = np.arange(1,31)
h = np.ones(24, dtype= np.float16)
asabit=0

# a = np.ones((25), dtype=np.int16)
# b = np.zeros((25), dtype=np.int16)
# x=17
# y=20
# b[int(x):int(y)]=2
# totaltime=a+b
########## Solar Radyasyon Verisi Alma - SolarPy
for i in range(24):
    if asabit<10:
        latitude_deg = 41.114  # positive in the northern hemisphere
        longitude_deg = -29.109  # negative reckoning west from prime meridian in Antalya, Turkey
        date = datetime.datetime(2019, 7, 1, int(asabit), 30,
                                 tzinfo=datetime.timezone.utc)  ###01 Aralık 2019 icin solar radiation degeri
        altitude_deg = get_altitude(latitude_deg, longitude_deg, date)
        solarradyasyon = radiation.get_radiation_direct(date, altitude_deg)
        radyasyon[int(asabit)]=solarradyasyon
    elif asabit>=10 and asabit<20:
        latitude_deg = 41.114  # positive in the northern hemisphere
        longitude_deg = -29.109  # negative reckoning west from prime meridian in Antalya, Turkey
        date = datetime.datetime(2019, 7, 1, int(asabit), 30,
                                 tzinfo=datetime.timezone.utc)  ###01 Aralık 2019 icin solar radiation degeri
        altitude_deg = get_altitude(latitude_deg, longitude_deg, date)
        solarradyasyon = radiation.get_radiation_direct(date, altitude_deg)
        radyasyon[int(asabit)]=solarradyasyon
    else:
        latitude_deg = 41.114 # positive in the northern hemisphere
        longitude_deg = -29.109  # negative reckoning west from prime meridian in Antalya, Turkey
        date = datetime.datetime(2019, 7, 1, int(asabit), 30,
                                 tzinfo=datetime.timezone.utc)  ###01 Aralık 2019 icin solar radiation degeri
        altitude_deg = get_altitude(latitude_deg, longitude_deg, date)
        solarradyasyon = radiation.get_radiation_direct(date, altitude_deg)
        radyasyon[int(asabit)]=solarradyasyon
    asabit=asabit+1
########## Solar Radyasyon Verisi Alma - SolarPy

####Kutuphane verisi saat 10'dan sonra gunes verisi vermeye basladigindan kucuk bir ittirme yaptim burada
radyasyon[8]=110
radyasyon[7]=78.56
########### PV Panel Enerji Uretim Hesabi
#  E = A * r * H * PR
bsabit=0
#E = Energy (kWh)
#A = Total solar panel Area (m2)
#r = solar panel yield or efficiency(%)
#H = Annual average solar radiation on tilted panels (shadings not included)
#PR = Performance ratio, coefficient for losses (range between 0.5 and 0.9, default value = 0.75)
###########
pv_e=np.ones(24, dtype= np.float16)
for i in range(24):
    a = 80.584  # Boyut: 1956 × 992 × 40mm # Adet : 10
    r = 0.22
    h = radyasyon[int(bsabit)]
    pr = 0.8
    pv_ye = a * r * h * pr  ###Yıllık Üretim
    pv_e[bsabit] = pv_ye / (365 * 24)  ###Saatlik Üretim
    bsabit = bsabit + 1
gunluktoplam= np.sum(pv_e)

##Batarya Enerji Depolama
bat_time = np.ones(24, dtype = np.float16)
bat_time[0:24]=pv_e[0:24]
##Batarya Enerji Depolama
o=0
##Şebekeden Çekilen Enerji Miktarı
totaltime = np.zeros(30, dtype = np.float32)
totaltime_1 = np.zeros(30, dtype = np.float32)
totaltime_2 = np.zeros(30, dtype = np.float32)
j = np.zeros(30, dtype = np.float32)
for i in range(30):
    totaltime_1[o]= buzdolabi[o]+d_dondurucu[o]+elksup[o]+termosifon[o]+tv[o]+bilgisayar[o]+firin[o]+aydinlatma[o]+mikrodalga[o]+kettle[o]+davlumbaz[o]+sackuru[o]+klima[o]
    totaltime_2[o]= esarj[o]+sarjaleti[o]+camasir[o]+bulasik[o]+camasirkur[o]
    j[o] = esarj[o] + sarjaleti[o] + camasir[o] + bulasik[o] + camasirkur[o]
    o=o+1

totaltime= totaltime_1+totaltime_2
threshold=np.sum(totaltime)/12
##Şebekeden Çekilen Enerji Miktarı

###toplamyuk
pb= input("Tuketimin artmaya basladigi saati giriniz: ")
p_baslangic=int(pb)
p_surec=input("Bu tuketim kac saat suruyor?: ")
p_bitis=int(p_baslangic)+int(p_surec)  ###Tuketimin azaldigi saat (Uyku saati)
sayac=0
battery=1
enerjisbt=6
enerjisatis=0
bsay=8
for i in range(10):
    battery = battery+(bat_time[bsay])
    bsay= bsay + 1
    if battery > 6:
        enerjisatis = battery-enerjisbt
        battery = 6
    elif battery > 6 and enerjisatis>0:
        enerjisatis= enerjisatis+battery-enerjisbt
    elif battery == 6:
        battery = 6

a = np.ones(24, dtype=int)
#index olustur
for i in range(24):
    if totaltime[i] > threshold and i==18 or i==19 or i==20 or i==21 or i==22:
        sayac = sayac+1

#for i in range(int(p_surec)+1):
 #   index = totaltime[int(p_baslangic)+i:int(p_bitis)]
    # if not np.all(index == 1):   ##indexten çıkıp totaltime_s'imizi düz modüle eşitleyelim ve bir sayac ciktisi alalim
  #  if np.sum(index) != int(p_surec) - i:
   #     sayac = sayac + 1
    #    totaltime_s = a

########sayac 24'den büyük olma problemini matlabdeki 24den büyük olma durumunda
# direk 3 arkaya atması emrini vererek çözdüm # değilse de sayac ve 3 saatlik triple tariff arasında yazdırdm
x = int(p_baslangic)
y = int(p_bitis)
totaltime_3 = j
if sayac != 0:
    if y + sayac > 19:
        totaltime_3[x + sayac: x + sayac + int(p_surec) + 1] = totaltime_3[x-1 : y]
        totaltime_3[x:y] = totaltime_2[x + sayac: x + sayac + int(p_surec)]

shifted=totaltime_3+totaltime_1
bat_time[0]=0
plt.title("Enerji Uretim Grafigi")
plt.plot(zaman1[0:24], bat_time, color = 'royalblue', label= 'kwH')
plt.xlabel("Saat")
plt.ylabel("Yük")
plt.legend()
plt.show()
bat_time[0]=1


aylikkar=enerjisatis*1*30
toplamtuketim=np.sum(totaltime)
shiftedtuketim=np.sum(shifted)
pvuretim=np.sum(bat_time)

notshifted_kwh=totaltime/1000
shifted_kwh=shifted/1000
notshifted_kwhtotal=notshifted_kwh
shifted_kwhtotal=shifted_kwh
t=17
threshold2=threshold/1000

for i in range(8):
    if shifted_kwhtotal[t] > threshold2 and float(battery) > 3:
        shifted_kwhtotal[t] = shifted_kwhtotal[t] - float(battery)/3
        battery= battery-battery/3
    elif shifted_kwhtotal[t] > threshold2 and float(battery) <= 2:
        shifted_kwhtotal[t] = shifted_kwhtotal[t] - float(battery)
        battery = 0
    t=t+1
plt.title("LoadShifting Grafigi (GES sistemi ile)")
plt.bar(zaman1, shifted_kwhtotal, color = 'tab:red', align = 'center', label= 'Shifted')
plt.bar(zaman1, notshifted_kwhtotal, color = 'tab:blue', align = 'center', label= 'Not Shifted')
plt.ylabel("Yük (kwH)")
plt.legend()
plt.show()

plt.title("LoadShiftingden Önce")
plt.bar(zaman1, notshifted_kwhtotal, color = 'tab:blue', align = 'center', label= 'Not Shifted')
plt.ylabel("Yük (kwH)")
plt.legend()
plt.show()

plt.title("LoadShiftingden Sonra (GES sistemi ile)")
plt.bar(zaman1, shifted_kwhtotal, color = 'tab:red', align = 'center', label= 'Shifted')
plt.ylabel("Yük (kwH)")
plt.legend()
plt.show()

bat_time[0]=0
plt.title("Uretim/Tuketim")
plt.plot(zaman1[0:24], bat_time, color = 'royalblue', label= 'kwH')
plt.plot(zaman1, notshifted_kwhtotal, color = 'tab:red', label= 'kwH')
plt.xlabel("Saat")
plt.ylabel("Yük (kwH)")
plt.legend()
plt.show()
bat_time[0]=1

#Elektrik Birim Fiyatı [kWh/tl]
#Gündüz(6-17)	1.3046
#Puant (17-22)	2.06
#Gece(22-6)	0.829

enerjimaaliyeti= np.ones(24, dtype = np.float16)
enerjimaaliyeti[6:18]=enerjimaaliyeti[6:18]*1.3046
enerjimaaliyeti[18:22]=enerjimaaliyeti[18:22]*2.06
enerjimaaliyeti[22:24]=enerjimaaliyeti[22:24]*0.829
enerjimaaliyeti[0:6]=enerjimaaliyeti[0:6]*0.829


plt.title("Saatlik Enerji Maaliyeti")
plt.plot(zaman1[0:24], shifted_kwhtotal[0:24]*enerjimaaliyeti[0:24], color = 'royalblue', label= 'GES + LoadShifting')
plt.plot(zaman1[0:24], notshifted_kwhtotal[0:24]*enerjimaaliyeti[0:24], color = 'tab:red', label= 'GES YOK SHIFTING YOK')
plt.xlabel("Saat")
plt.ylabel("Turk Lirasi")
plt.legend()
plt.show()

ucret_nshifted=np.sum(notshifted_kwhtotal[0:24]*enerjimaaliyeti[0:24]) ## GES YOK SHIFTING YOK
ucret_shifted=np.sum(shifted_kwhtotal[0:24]*enerjimaaliyeti[0:24])  ## GES ile birlikte


kaydirilanyuk= np.sum(j[0:30])/1000
print("LoadShifting + GES Fatura: {}TL" .format(ucret_shifted*30))
print("Normal ödenmesi gereken fatura: {}TL" .format(ucret_nshifted*30))

print("Toplam kaydırılan yük: {}kwH" .format(kaydirilanyuk))
print("Loadshifting uygulanmadan önce: {}".format(notshifted_kwhtotal))
print("Loadshifting uygulandıktan sonra: {}".format(shifted_kwhtotal))
print("Fazla uretilen enerjinin satisindan kazanilan para: {}TL" .format(aylikkar))





#####Koray Göksu 18012116
#####Süleyman Furkan KAYA 17012097