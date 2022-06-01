# **YAYILIM ALGORÝTMASI**

<details>
  <summary>Ýçindekiler</summary>
  <ol>
    <li>
      <a href="#### **AMAÇ**">Amaç</a>
      </ul>
    </li>
    <li>
      <a href="#### **SÜREÇ**">Süreç</a>
      </ul>
    </li>
    <li><a href="#### **KULLANIM**">Kullaným</a></li>
    <li><a href="#### **YOL HARÝTASI**">Yol Haritasý</a></li>
  </ol>
</details>

---


## **AMAÇ**
---
**Yayýlým Algoritmasý**; halihazýrda açýk maðazalarýn **lokasyonlarýnýn**, **Ýllerin, ilçelerin ve mahallelerin özel durumlarý** dikkate alýnarak, yeni açýlacak maðazalar için **en uygun** alanlarý tespit etmek.

<p align="right">(<a href="#top">Tepeye çýk</a>)</p>

## **SÜREÇ**
---
Önce Vestel'in ve rakiplerinin maðazalarýnýn **coðrafi konumlanmalarý** analiz edildi. Maðazalarýn kapsam alanlarýnýn ilçe veya mahalle sýnýrlarýyla belirlenmesi pek **açýklayýcý olmadý**. Bu sebeple maðazalarýn gruplanmalarýna göre, analizimizi anlamlandýrmak adýna suni "mahalleler", yani **cluster**'lar oluþturuldu. 

Buna baðlý olarak potansiyeli olan bölgeler farklý parametrelerin de yardýmýyla tespit edildi ve puanlandý. Cluster dýþý outlier noktalarýn analizi de
tamamlandý. Algoritma her gün geliþtiriliyor ve daha sofistike hale getiriliyor.

<p align="right">(<a href="#top">Tepeye çýk</a>)</p>


---
## **KULLANIM**
Terminal Ekraný açýp Directory'i projenin path'i olarak deðiþtiriyoruz. Burada önemli husus; ilgili virtual environment'ýn aktif olmasý. 

```powershell
cd {PROJECT_PATH}
```

Bu noktada "Models" Klasörüne girerek iki þekilde kodu çalýþtýrabiliriz:
  - Ýl parametresini tekil olarak verebiliriz,
  - Tüm illeri iteratif olarak çalýþtýrabiliriz.

```powershell
cd models
```


__Tekil Kullaným Ýçin:__
```powershell
python main.py Ýstanbul
```

__Tüm Ýller Ýçin:__
```powershell
python iterator.py
```
Kodlarýný kullanarak uygulamayý baþlatabiliriz.

<p align="right">(<a href="#top">Tepeye çýk</a>)</p>



## **YOL HARÝTASI**

### **1. Harita bazlý yayýlým çalýþmasýna odaklanýldýktan sonra tamamlanan iþler** : 
- [X] Ýstanbul özelinde dbscan ile clustering yapýlmasý

- [X] Next Geo entegrasyonu

- [X] Patching yapýlarak outlier noktalara ikinci þans verilmesi

- [X] Ankara özelinde clustering yapýlmasý

- [X] Rekabet ve büyüme bazlý maðaza ihtiyaçlarýnýn çýkartýlmasý (Gap Analizi)

- [X] Gap Analizinin kodlanmasý

- [X] Ýstanbul ve Ankara’da kullanýlan parametreler deðerlendirilerek matematiksel model aracýlýðýyla parametrelerin dinamik hale getirilmesi 

- [X] Ýl içerisinde açýlacak maðazalarýn önceliklendirilmesi (sýralandýrýlmasý)

- [X] Algoritmanýn 81 ilde çalýþacak þekilde otomatize edilmesi

- [X] 81 il sonuçlarýný geniþ açýdan görüntüleyebilmek/kontrol edebilmek için kokpit excelinin oluþturulmasý (Büyük excel)

- [X] Ýl Bazlý Pazar Payý çalýþmasý için mahalle bazlý pazar kýrýlýmýnýn yapýlmasý

- [X] Kapanma algoritmasýnýn oluþturulmasý

- [X] Outlier nokta vs. clusterdaki nokta performans karþýlaþtýrmasý 

- [X] Maðaza tipine göre performans karþýlaþtýrmasý (Bayi vs. Ekspres vs. Kurumsal)

### **2. Mevcutta üzerinde çalýþýlan iþler :** 
- [ ] Vestel Cirolarý ile il bazlý pazar kýyaslanarak il bazlý pazar payý oranlarýnýn çýkartýlmasý 

- [ ] Mahalle ve Cluster arasýndaki iliþkinin matematiksel olarak modellenmesi ve clusterdaki pazarýn büyüklüðünün tahminlenmesi 

- [ ] Kokpit exceli kullanýlarak il bazlý durum tespiti ve alýnabilecek aksiyonlar çalýþmasýnýn tamamlanmasý 

- [ ] Yayýlým Çýktý excellerine Özet sayfa eklenecek

- [ ] 2 il problemi 
- [ ] Dökümantasyon ve kod sadeleþtirilmesi

### **3. Bir sonraki adýmda yapýlacaklar :**
- [ ] Bir maðazanýn performansýnýn ölçümlenmesi, sonrasýnda da yeni açýlacak bir maðazanýn cirosunun tahminlenmesi

- [ ] Ýl içerisinde açýlacak maðazalarýn önceliklendirilmesi (sýralandýrýlmasý) // UPDATE 

- [ ] Vestel’i pozitif etkileyen markalar -> Maðaza tipi kýrýlýmlý 

- [ ] Montaj datasýnýn analiz edilmesi

- [ ] Hangi tipte maðaza açacaðýz sorusunun cevabýna ulaþmak (Tüm çalýþmalarý birleþtirerek verisel olarak bir çýkarým yapabiliyor muyuz? Eðer hayýr ise, kanal konumlandýrýlmasýnýn tamamlanmasý beklenecek.)

- [ ] Çýktýlarýn nereden servis edileceðinin netleþtirilmesi 






<p align="right">(<a href="#top">Tepeye çýk</a>)</p>

---

