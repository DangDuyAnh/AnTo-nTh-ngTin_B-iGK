from PIL import Image
import numpy as np
from QRcode import sl, QR_area, QR_fromtext

def encrypt(input_image, share_size):               # Mã hóa ảnh màu với xor
    image = np.asarray(input_image)
    (row, column, depth) = image.shape
    shares = np.random.randint(0, 256, size=(row, column, depth, share_size))
    shares[:,:,:,-1] = image.copy()
    for i in range(share_size-1):
        shares[:,:,:,-1] = shares[:,:,:,-1] ^ shares[:,:,:,i]
    return shares

def decrypt(shares, share_size):                   # giải mã ảnh màu với xor
    for i in range(share_size - 1):
        shares[-1] = shares[-1][:,:,:] ^ shares[i][:,:,:]
    final_output = shares[-1]
    return final_output

def encrypt_with_QR(input_image, messages):         # Mã hóa ảnh màu với QR, các ảnh sẽ được lưu vào thư mục output_colour
    # crop thành ảnh vuông
    input_image = input_image.convert('RGB')
    img_size = input_image.size[0]
    if (input_image.size[0] > input_image.size[1]):
        img_size = input_image.size[1]
    width, height = input_image.size
    left = (width - img_size) / 2
    top = (height - img_size) / 2
    right = (width + img_size) / 2
    bottom = (height + img_size) / 2
    square_img = input_image.crop((left, top, right, bottom))

    share_size = len(messages)
    images = []
    pos = []
    for i in range(share_size):
        s = messages[i]
        if (len(s) > sl):
            s = s[0:sl]
            s = s[:(sl - 3)] + '.' + s[(sl - 2):]
            s = s[:(sl - 2)] + '.' + s[(sl - 1):]
            s = s[:(sl - 1)] + '.' + s[sl:]
        s = s.ljust(sl)
        image_temp, pos_temp = QR_fromtext(s)
        images.append(image_temp.convert('RGB'))             # chuyển ảnh QR thành RGB
        pos.append(pos_temp)
    const_size = images[0].size[0]
    square_img = square_img.resize((const_size,const_size), Image.NEAREST)
    shares = encrypt(square_img, share_size)
    results = []
    for i in range(share_size):
        QR_image = np.asarray(images[i]).astype(np.uint8)
        temp = np.random.randint(0, 256, size=(const_size, const_size, 3))
        QR_area0 = QR_area(images[i], pos[i])
        image = shares[:,:,:,i]
        for a in range(const_size):
            for b in range(const_size):
                if QR_area0[a][b] == 1:
                    temp[a][b] = QR_image[a][b]
                else:
                    temp[a][b] = image[a][b]
        temp = Image.fromarray(temp.astype(np.uint8))
        results.append(temp)
    for i in range(share_size):
        name = "output_colour/XOR_Share_" + str(i + 1) + ".png"
        results[i].save(name)


def decrypt_with_QR(shares, message):                      # giải mã các ảnh QR, và ghi thêm tên bệnh nhân
    share_size = len(shares)
    const_size = shares[0].size[0]
    if (len(message) > sl):
        message = message[0:sl]
        message = message[:(sl - 3)] + '.' + message[(sl - 2):]
        message = message[:(sl - 2)] + '.' + message[(sl - 1):]
        message = message[:(sl - 1)] + '.' + message[sl:]
    message = message.ljust(sl)
    image_temp, pos_temp = QR_fromtext(message)
    QR_area2 = QR_area(image_temp, pos_temp)
    QR_image = np.asarray(image_temp.convert('RGB')).astype(np.uint8)
    temps = []
    for i in range(share_size):
        temp = np.asarray(shares[i]).astype(np.uint8)
        temps.append(temp)
    final_output = decrypt(temps, share_size)
    for i in range(const_size):
        for j in range(const_size):
            if QR_area2[i][j] == 1:
                final_output[i][j] = QR_image[i][j]
    output_image = Image.fromarray(final_output.astype(np.uint8))
    output_image.save("output_colour/output.png")
    return output_image, final_output


# Test thử chương trình

# Mã hóa
# '''
messages = []
messages.append("The city of stars")
messages.append("The fools who dreams")
messages.append("Từ Hoàng Giang")
input_image = Image.open('Jennie_colour.jpg')
encrypt_with_QR(input_image, messages)
# '''

# Giải mã
'''
images = []
input_image = Image.open('output_colour/XOR_Share_1.png')
images.append(input_image)
input_image = Image.open('output_colour/XOR_Share_2.png')
images.append(input_image)
input_image = Image.open('output_colour/XOR_Share_3.png')
images.append(input_image)
decrypt_with_QR(images, "Jennie Kim")
'''
