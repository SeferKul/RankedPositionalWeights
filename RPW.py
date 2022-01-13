import numpy as np                                        #numpy kütüphanesinin çağrılması

Cvalue=float(input("Lütfen bir 'C' değeri giriniz: "))    # Kullanıcıdan C değerinin alınması

#---------------DOSYADAN VERİNİN ÇEKİLMESİ---------
veri_file= open("veri.txt","r")                           # text dosyasının okunur modta açılması
veri= [(i.split("\n")[0]) for i in veri_file]             # text dosyasının satırlarının veri adındaki listeye çekilmesi


versay=int(veri[0])                       # Görev sayısı bilgisinin alınması
veri.pop(0)                               # Görev sayısı bilgisinin "veri" listesinden çıkarılması


time={}                                   # Görev süre bilgilerini tutan dictionary oluşturulması
for i in range((versay)):
    time[i+1]=(float(veri[i]))


prio=[]
for i in range(versay,len(veri)-1):       # Dosyadan çekilen öncelikler verisi
    prio.append(veri[i])

pr=[(i.split(",")) for i in prio]         # Dosyadan çekilen öncelikler verisinin listelenmesi

#-------VERİLERİN KULLANILABİLİRLİĞİNİN ARTTIRILMASI-------
zeros= np.zeros((versay,versay))          # Numpy array kullanarak 0'lardan oluşan bir öncelik matrix i oluşturur
for n in pr: 
    x=(int(n[0]))-1
    y=(int(n[1]))-1
    zeros[x][y]=1

cleanlist= np.zeros((versay,1))           # Nump array kullanarak Görev sayısı kadar liste açar
cleanlist=cleanlist.tolist()              # Arraydan Listeye dönüşüm


for rows in reversed(range(len(zeros))):  # Önceliklerin tersten başlanarak gruplandırılması
    for el in range(len(zeros[rows])):
        if zeros[rows][el]==1:
            cleanlist[rows].append(el+1)
            

for r in reversed(range(len(cleanlist))): # Öncelikler listelerinde tersten başlanarak gerekli işlemlerin yapılması
    cleanlist[r].pop(0)                   # Listelerdeki sıfırların atılması
    for elt in cleanlist[r]:              
        
            listforcu=cleanlist[elt-1]
            cleanlist[r]=(cleanlist[r])+(listforcu)  #Kümülatif olarak listelerin sondan başa doğru eklenerek oluşturulması
            
    cleanlist[r].insert(0,r+1)                        # Görevlerin kendi numaralarının listeye dahil edilmesi
lenght=len(cleanlist)
cleanlist[lenght-1].insert(0,lenght)       # Son elemanın son kümeye eklenişi
    
     
def duplicate(x):                          # Listedeki tekrarlayan görevler silinip 1 er tane bırakmak için fonksiyon tanımlanması 
  return list(dict.fromkeys(x))    


caltlist = cleanlist.copy()                # Hesaplamalar için cleanlist listesinin kopyası oluşturulur
caltlist = list(map(duplicate,caltlist))   # Listedeki tekrarlayan görevler silinir

copytime= time.copy()                      # Zamanların tutulduğu dictionary kopyalanır
 
for ls in range(len(caltlist)):            # Hesaplama listesindeki değerlerin üzerinde tek tek dolaşılarak-          
      for p in range(len(caltlist[ls])):        # time sözlüğünde denk gelen sürelerle eşleştirilmesi 
           caltlist[ls][p]=copytime[caltlist[ls][p]]

total= list(map(sum,caltlist))             # Hesaplama listesindeki verilerin toplanarak görev ağırlıklarının hesaplanması
                        

weight_dict={}                             # Göreve göre ağırlık verisinin tutulduğu dictionary'nin oluşturulması
for item in range(len(total)):            
    weight_dict[(item+1)]=total[item]

sorted_dict = sorted(weight_dict.items(), key=(lambda x: x[1]), reverse=True)    #görev ağırlıklarının büyükten küçüğe sıralanması
 

#--------------İSTASYONLARA ATANMA ----------------
stationNo=1                                # Değişkenlerin,listelerin ve dictionarylerin tanımlanması

remain= Cvalue                             # İstasyondaki boş süresinin hesaplanabilmesi için C değerinin alınması
Remain_Container={}                          #İstasyon boş sürelerinin tutulacağı sözlük

Stations={}                                # İstasyon atamalarının tutulacağı sözlük
Stations[stationNo]=[]                     # İlk istasyonun açılması

row=0

while row < len(sorted_dict):                 
    timeofitem=time[sorted_dict[row][0]]                    # Görevin süresi
    remain= remain - timeofitem
    if remain >= 0:                                         # İstasyon kalan süre kontrolü
        Stations[stationNo].append(sorted_dict[row][0])
        Remain_Container[stationNo]=remain
        row+=1 #görevin istasyona eklenmesi  
    else:
        stationNo+=1
        Stations[stationNo]=[]
        remain = Cvalue


       
#----------------Performans Hesaplamaları-----------
Station_Total={}                                           # İstasyon Bazında Süreler

for i in range(len(Remain_Container)):
    Station_Total[i+1]= Cvalue - Remain_Container[i+1]

#--------------DENGE GECİKMESİ ---------------------
DengeGecSum = sum(Station_Total.values())                  # Toplam İstasyon Süresi

DengeGecik=(((len(Station_Total))*Cvalue)-DengeGecSum)/((len(Station_Total))*Cvalue)  #Denge gecikmesi hesaplanması


#--------------HAT ETKİNLİĞİ---------------
HatEtkinlik = DengeGecSum/((len(Station_Total))*Cvalue)    # Hat Etkinliği hesaplanması


#--------------HAT DÜZGÜNLÜK İNDEKSİ--------------
Duzgunluk_Sum=[]                                           # Hat Düzgünlük İndeksi Hesaplaması 
MaxSTVal=max(Station_Total.values())

for  k in Station_Total:
        res=((MaxSTVal)-Station_Total[k])**2
        Duzgunluk_Sum.append(res)
DuzgunlukTotal=sum(Duzgunluk_Sum)
SI=DuzgunlukTotal**(1/2)
SIPercent= SI/(Cvalue*(len(Station_Total)))

totalIdle= sum(Remain_Container.values())

#--------------SONUÇ EKRANININ EKRANA YAZDIRILMASI-------------- 
print("\n")
print("* * * - - - - - - - - - - - - - - - - - SONUÇLAR - - - - - - - - - - - - - - - - - * * *")

print("Atanan Elaman Sayısı:",versay,"\n" )
print("Toplam İstasyon Sayısı:", len(Station_Total),"\n")
print("Toplam İstasyon Boş Süresi:",totalIdle)

print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
for k in Stations:
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
    text="{StName}. İstasyon :{StTask} // İstasyon Süresi: {StTime} // İstasyon Boş süresi: {StIDLE}"
    print(text.format(StName=k,StTask=Stations[k],StTime=Station_Total[k],StIDLE=Remain_Container[k]))
    

print("- - - - - - - - - - - -")
print("Denge Gecikmesi Değeri:","%",round(DengeGecik*100,4))
print("* * * * * * ")
print("Hat Etkinlik Değeri:","%",round(HatEtkinlik*100,4))
print("* * * * * * ")
print("Hat Düzgünlük İndeksi:",round(SI,4))
              