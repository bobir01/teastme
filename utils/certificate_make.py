from PIL import Image, ImageDraw, ImageFont #pip install Pillow

def certify(name, score, user_id):

    img = Image.open('./11.jpg') #ceritifcate template 
    d1 = ImageDraw.Draw(img)
    W, H = (740,440)
    G, J = (1225, 800)
    score = f"Natija {score}"
    myFont = ImageFont.truetype('sh.ttf', 40) # yozuvni shrifti
    w,h = myFont.getsize("img")
    d1.text(xy=((W-w)/2.8,(H-h)/2), text=name, font=myFont, fill =(0,0,0))
    d1.text(xy=((G-w)/2.3,(J-h)/1.9), text=score, font=myFont, fill =(1,1,1))
    photo_name = f"./res_certificats/{user_id}_result.jpg"
    img.save(photo_name)
    return photo_name
    
