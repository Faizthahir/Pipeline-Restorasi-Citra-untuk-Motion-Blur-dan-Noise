📷 Pipeline Restorasi Citra untuk Motion Blur dan Noise

Proyek ini merupakan implementasi pipeline restorasi citra digital untuk mengatasi degradasi berupa motion blur dan noise.<br><br>

Citra asli didegradasi menggunakan motion blur dengan sudut 30° dan panjang 15 piksel, kemudian dikombinasikan dengan dua jenis noise:<br>

Gaussian noise (σ = 20)<br>
Salt-and-pepper noise (5%)<br><br>

Selanjutnya, dilakukan proses restorasi menggunakan beberapa metode untuk mengembalikan kualitas citra mendekati kondisi aslinya.<br><br>

🔧 Metode yang Digunakan

Pipeline ini mengimplementasikan beberapa metode restorasi citra:<br><br>

Inverse Filtering<br>
Metode dasar berbasis domain frekuensi, namun sensitif terhadap noise.<br><br>
Wiener Filter<br>
Pengembangan dari inverse filtering yang mempertimbangkan noise untuk hasil yang lebih stabil.<br><br>
Lucy-Richardson Deconvolution<br>
Metode iteratif yang mampu menghasilkan kualitas restorasi lebih tajam dan detail.<br><br>
📊 Evaluasi Kinerja

Kualitas hasil restorasi dievaluasi menggunakan metrik berikut:<br><br>

MSE (Mean Squared Error)<br>
PSNR (Peak Signal-to-Noise Ratio)<br>
SSIM (Structural Similarity Index)<br><br>

Selain itu juga dianalisis:<br>

Kualitas visual (ketajaman, detail, artefak)<br>
Waktu komputasi tiap metode<br><br>
🧪 Skenario Pengujian

Terdapat tiga skenario degradasi yang diuji:<br><br>

Motion blur saja<br>
Gaussian noise + motion blur<br>
Salt-and-pepper noise + motion blur<br><br>
📈 Hasil Utama
Lucy-Richardson memberikan kualitas restorasi terbaik (PSNR & SSIM tertinggi)<br>
Wiener Filter memberikan hasil paling stabil dengan waktu komputasi cepat<br>
Inverse Filtering hanya efektif pada citra tanpa noise<br><br>

Terdapat trade-off antara kualitas dan efisiensi, di mana metode dengan kualitas tinggi membutuhkan waktu komputasi lebih besar.<br><br>
