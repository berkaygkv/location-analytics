# **YAYILIM ALGOR�TMASI**

<details>
  <summary>��indekiler</summary>
  <ol>
    <li>
      <a href="#### **AMA�**">Ama�</a>
      </ul>
    </li>
    <li>
      <a href="#### **S�RE�**">S�re�</a>
      </ul>
    </li>
    <li><a href="#### **KULLANIM**">Kullan�m</a></li>
    <li><a href="#### **YOL HAR�TASI**">Yol Haritas�</a></li>
  </ol>
</details>

---


## **AMA�**
---
**Yay�l�m Algoritmas�**; halihaz�rda a��k ma�azalar�n **lokasyonlar�n�n**, **�llerin, il�elerin ve mahallelerin �zel durumlar�** dikkate al�narak, yeni a��lacak ma�azalar i�in **en uygun** alanlar� tespit etmek.

<p align="right">(<a href="#top">Tepeye ��k</a>)</p>

## **S�RE�**
---
�nce Vestel'in ve rakiplerinin ma�azalar�n�n **co�rafi konumlanmalar�** analiz edildi. Ma�azalar�n kapsam alanlar�n�n il�e veya mahalle s�n�rlar�yla belirlenmesi pek **a��klay�c� olmad�**. Bu sebeple ma�azalar�n gruplanmalar�na g�re, analizimizi anlamland�rmak ad�na suni "mahalleler", yani **cluster**'lar olu�turuldu. 

Buna ba�l� olarak potansiyeli olan b�lgeler farkl� parametrelerin de yard�m�yla tespit edildi ve puanland�. Cluster d��� outlier noktalar�n analizi de
tamamland�. Algoritma her g�n geli�tiriliyor ve daha sofistike hale getiriliyor.

<p align="right">(<a href="#top">Tepeye ��k</a>)</p>


---
## **KULLANIM**
Terminal Ekran� a��p Directory'i projenin path'i olarak de�i�tiriyoruz. Burada �nemli husus; ilgili virtual environment'�n aktif olmas�. 

```powershell
cd {PROJECT_PATH}
```

Bu noktada "Models" Klas�r�ne girerek iki �ekilde kodu �al��t�rabiliriz:
  - �l parametresini tekil olarak verebiliriz,
  - T�m illeri iteratif olarak �al��t�rabiliriz.

```powershell
cd models
```


__Tekil Kullan�m ��in:__
```powershell
python main.py �stanbul
```

__T�m �ller ��in:__
```powershell
python iterator.py
```
Kodlar�n� kullanarak uygulamay� ba�latabiliriz.

<p align="right">(<a href="#top">Tepeye ��k</a>)</p>



## **YOL HAR�TASI**

### **1. Harita bazl� yay�l�m �al��mas�na odaklan�ld�ktan sonra tamamlanan i�ler** : 
- [X] �stanbul �zelinde dbscan ile clustering yap�lmas�

- [X] Next Geo entegrasyonu

- [X] Patching yap�larak outlier noktalara ikinci �ans verilmesi

- [X] Ankara �zelinde clustering yap�lmas�

- [X] Rekabet ve b�y�me bazl� ma�aza ihtiya�lar�n�n ��kart�lmas� (Gap Analizi)

- [X] Gap Analizinin kodlanmas�

- [X] �stanbul ve Ankara�da kullan�lan parametreler de�erlendirilerek matematiksel model arac�l���yla parametrelerin dinamik hale getirilmesi 

- [X] �l i�erisinde a��lacak ma�azalar�n �nceliklendirilmesi (s�raland�r�lmas�)

- [X] Algoritman�n 81 ilde �al��acak �ekilde otomatize edilmesi

- [X] 81 il sonu�lar�n� geni� a��dan g�r�nt�leyebilmek/kontrol edebilmek i�in kokpit excelinin olu�turulmas� (B�y�k excel)

- [X] �l Bazl� Pazar Pay� �al��mas� i�in mahalle bazl� pazar k�r�l�m�n�n yap�lmas�

- [X] Kapanma algoritmas�n�n olu�turulmas�

- [X] Outlier nokta vs. clusterdaki nokta performans kar��la�t�rmas� 

- [X] Ma�aza tipine g�re performans kar��la�t�rmas� (Bayi vs. Ekspres vs. Kurumsal)

### **2. Mevcutta �zerinde �al���lan i�ler :** 
- [ ] Vestel Cirolar� ile il bazl� pazar k�yaslanarak il bazl� pazar pay� oranlar�n�n ��kart�lmas� 

- [ ] Mahalle ve Cluster aras�ndaki ili�kinin matematiksel olarak modellenmesi ve clusterdaki pazar�n b�y�kl���n�n tahminlenmesi 

- [ ] Kokpit exceli kullan�larak il bazl� durum tespiti ve al�nabilecek aksiyonlar �al��mas�n�n tamamlanmas� 

- [ ] Yay�l�m ��kt� excellerine �zet sayfa eklenecek

- [ ] 2 il problemi 
- [ ] D�k�mantasyon ve kod sadele�tirilmesi

### **3. Bir sonraki ad�mda yap�lacaklar :**
- [ ] Bir ma�azan�n performans�n�n �l��mlenmesi, sonras�nda da yeni a��lacak bir ma�azan�n cirosunun tahminlenmesi

- [ ] �l i�erisinde a��lacak ma�azalar�n �nceliklendirilmesi (s�raland�r�lmas�) // UPDATE 

- [ ] Vestel�i pozitif etkileyen markalar -> Ma�aza tipi k�r�l�ml� 

- [ ] Montaj datas�n�n analiz edilmesi

- [ ] Hangi tipte ma�aza a�aca��z sorusunun cevab�na ula�mak (T�m �al��malar� birle�tirerek verisel olarak bir ��kar�m yapabiliyor muyuz? E�er hay�r ise, kanal konumland�r�lmas�n�n tamamlanmas� beklenecek.)

- [ ] ��kt�lar�n nereden servis edilece�inin netle�tirilmesi 






<p align="right">(<a href="#top">Tepeye ��k</a>)</p>

---

