<br />
<div align="center">
<h3 align="center">gemastik</h3>

  <p align="center">
    Repositori untuk keperluan gemastik. Versi Raspberry Pi 4
  </p>
</div>

### Struktur File
Struktur folder dari repositori:
```
. 
├── datasets
|    ├── raw
|    └── send
├── src
├── .gitignore
├── app.py
├── README.md
├── requirements.txt
└── setup.json
```

### Cara Instalasi Repositori
1. Klon repo dari github.
  ```git
   git clone -b raspberry-pi-4 https://github.com/Dhaboav/gemastik.git
  ```
2. Melakukan instalasi library python dengan `pip install -r requirements.txt` pada terminal.
3. Membuat file `setup.json` pada folder repositori.
4. Membuat file `basisData.csv` pada folder datasets.
5. Jalankan file `app.py`.