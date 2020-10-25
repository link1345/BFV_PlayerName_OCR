# BFV search
BFVと呼ばれるゲームにおいて、サーバに参加しているユーザ名を取得するツールです。
名前は、OCRで取得しています。

# install 

## python & pip
python vesion 3.8.6推奨

```
winget install Python.Python -v 3.8.6
py -m pip install --upgrade pip
py -m pip install Image pyocr opencv-python numpy pywinauto PyQt5
```

## tesseract
https://qiita.com/henjiganai/items/7a5e871f652b32b41a18
を参考。


https://tesseract-ocr.github.io/tessdoc/Home.html
の一番したにwindow用exeへのリンクがある。
https://github.com/UB-Mannheim/tesseract/wiki に行くと思うので、

「tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe (64 bit) resp.」とか
という感じで書いてあるので、クリックしてダウンロードする。

あとは、適当にインストール。
途中でAdditional langage dataとか聞かれる。
今回は英語のみ入れておく。


# 使い方
![image1](image1.png)

## 1.ソフト起動
run.pyを起動させる。
pythonをインストールした段階で、GUI上でrun.pyをクリックするだけで、使用できるようになっているはずです。

## 2.キャプチャ先ソフトを選択
ソフト上部に「対象ソフト:」という項目があるので、「Battlefield V」

 # License
English : This software is released under the MIT License, see LICENSE.  
日本語 : このソフトウェアは、MITライセンスの下でリリースされています。ライセンスを参照してください。  



