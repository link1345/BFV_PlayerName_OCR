import settings

# BAN対象者のマッチ処理の類似度
SearchMatchNumber = 75

# Tessractのパス
Tesseract_path = 'C:\\Program Files\\Tesseract-OCR'
# Tessractのtessdataパス
Tesseract_tesspath = 'C:\\Program Files\\Tesseract-OCR\\tessdata'

# 画像切り取りポイントとサイズ
## 0 = StartPointX , 1 = StartPointY , 2 = SizeX , 3 = SizeY
## 注意 : 1ドットでもミスると、うまく取れません。
Team1_ImageCrop = [330, 212 , 315, 23]
Team2_ImageCrop = [1210, 212 , 315, 23]

