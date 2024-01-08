import json
import qrcode, io

phone_number = "+25478963225452"  # Replace with the recipient's phone number
message = """Name: Yoni Limo.
Internship Center: Nazareth Hospital.
Serial Number: asidwq14as588aw7e."""

sms_data = f"SMSTO:{phone_number}:{message}"

json_data = json.dumps(sms_data)

# Create a QR code instance
qr = qrcode.QRCode(
    version=1,  # Controls the size of the QR Code
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Controls the error correction used for the QR Code
    box_size=10,  # Controls how many pixels each “box” of the QR code is
    border=4,  # Controls how many boxes to use for the border
)

# Data to be encoded in the QR code
data = "Hello, World!"

# Add data to the QR code instance
qr.add_data(sms_data)
qr.make(fit=True)

# Create an image from the QR code instance
img = qr.make_image(fill_color="black", back_color="white")
print(type(img))
# Save the image
img.save(r"C:\Users\limzy\OneDrive\Desktop\Projects\ballot\qrcodes\my_qrcode.png")
image_bin = io.BytesIO()
img.save(image_bin, format='PNG')

image_binary = image_bin.getvalue()
print(type(image_binary))



# # Generate a 12-character alphanumeric sequence
# generated_sequence = generate_alphanumeric_sequence(12)
# print(generated_sequence)
