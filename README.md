# DIY Face Tracking Turret (El Yapımı Yüz Takip Tareti)

![Proje Görseli](WhatsApp%20Image%202026-02-04%20at%2017.35.53.jpeg)
### 🎥 Proje Demosu
[Videoyu İzlemek İçin Tıklayın](WhatsApp%20Video%202026-02-04%20at%2017.36.02.mp4)

Bu proje, Python (OpenCV) ile görüntü işleme ve Arduino ile motor kontrolünü birleştiren bir savunma sanayi prototip çalışmasıdır. Bilgisayar kamerasından alınan görüntü işlenir ve taretin namlusu (lazer), algılanan yüzü otomatik olarak takip eder. Görünüm itibari ile doğada gizlenmiş bir gözetleme kulesi havası verildi.
## 🛠️ Kullanılan Teknolojiler ve Malzemeler
* **Yazılım**: Python 3.x, OpenCV, cvzone (MediaPipe tabanlı), Arduino C++
* **Donanım:** Arduino UNO, 2x Servo Motor (SG90), Lazer Modülü
* **Mekanik:** Doğal kütük taban, el yapımı mukavva zırh ve gerçekçi görüntü için doğadan yaprak ve ot.

## 🚀 Nasıl Çalışır?
1.  Python kodu, webcam üzerinden yüzü tespit eder.
2.  Yüzün X ve Y koordinatları hesaplanır.
3.  Bu koordinatlar USB (Seri Haberleşme) üzerinden Arduino'ya gönderilir.
4.  Arduino, gelen veriye göre Pan ve Tilt servolarını hareket ettirir.

## 👨‍💻 Geliştirici
Yusuf Ali Utğu - Sakarya Uygulamalı Bilimler Üniversitesi - Mekatronik Bölümü
