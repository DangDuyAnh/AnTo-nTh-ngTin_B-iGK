from PIL import Image
import qrcode

sl = 100
def QR_area(image, pos):                       # tìm các pixel ở đó chứa mã QR
    size = image.size[0]
    QR_area = []
    for i in range(size):
        QR_area.append([])
        for j in range(size):
            QR_area[i].append(0)
    for i in range(size):
        for j in range(size):
            if (i < 120) or (i >= (size - 120)) or (j < 120) or (j >= (size - 120)):
                QR_area[i][j] = 1
                continue
            if (i >= 120 and j >= 120 and i < 360 and j < 360):
                QR_area[i][j] = 1
                continue
            if (i >= (size - 360) and j >= 120 and i < (size - 120) and j < 360):
                QR_area[i][j] = 1
                continue
            if (i >= 120 and j >= (size - 360) and i < 360 and j < (size - 120)):
                QR_area[i][j] = 1
                continue
            if (i % 30 == 10 and j % 30 == 10):
                for a in range(10):
                    for b in range(10):
                        QR_area[i + a][j + b] = 1

    for i in pos:
        for j in pos:
            if (i == 6 and j == pos[-1]) or (j == 6 and i == pos[-1])\
                or (i == 6 and j == 6):
                continue
            else:
                for a in range(150):
                    for b in range(150):
                        QR_area[10*(3*(i-2)+12)+a][10*(3*(j-2)+12)+b] = 1
    return QR_area

def QR_fromtext(txt,ver=5,err_crt = qrcode.constants.ERROR_CORRECT_H):         # Sinh ảnh QR nhị phân từ text
    qr = qrcode.QRCode(version = ver,error_correction = err_crt,box_size=3)
    qr.add_data(txt)
    qr.make(fit=True)
    img_qr = qr.make_image()
    img_size = img_qr.size[0] - 24

    img_frame = img_qr
    for x in range(0,img_size):
        for y in range(0,img_size):
            if x < 24 and (y < 24 or y > img_size-25):
                continue
            if x > img_size-25 and (y < 24 ):
                continue
            if (x%3 ==1 and  y%3 == 1):
                if (img_frame.getpixel((x+12,y+12)) == 0):
                    continue
            img_frame.putpixel((x+12,y+12),(255))
    pos = qrcode.util.pattern_position(qr.version)
    img_qr2 = qr.make_image()
    for i in pos:
        for j in pos:
            if (i == 6 and j == pos[-1]) or (j == 6 and i == pos[-1])\
                or (i == 6 and j == 6):
                continue
            else:
                rect = (3*(i-2)+12,3*(j-2)+12,3*(i+3)+12,3*(j+3)+12)
                img_tmp = img_qr2.crop(rect)
                img_frame.paste(img_tmp,rect)

    img_res = Image.new("RGBA",(img_frame.size[0]*10,img_frame.size[1]*10),(0,0,0,0))
    img_res = img_res.convert('1')
    img_frame = img_frame.resize((img_frame.size[0]*10,img_frame.size[1]*10), Image.NEAREST)
    img_res.paste(img_frame,(0,0),img_frame)
    return img_res, pos