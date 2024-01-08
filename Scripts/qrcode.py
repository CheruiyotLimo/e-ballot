from PIL import Image
import io
import qrcode


def qrcode_generator(name, centre, serial):
    
    phone_number = "+254789632254" 
    
    message = f"""Name: {name}
    Internship Center: {centre}
    Serial Number: {serial}"""

    sms_data = f"SMSTO:{phone_number}:{message}"

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=10,  
        border=4,  
    )

    # Add data to the QR code instance
    qr.add_data(sms_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to binary
    image_bin = io.BytesIO()
    img.save(image_bin, format='PNG')

    image_binary = image_bin.getvalue()
    
    return image_binary
    
    # Create an image from the QR code instance
    # img = qr.make_image(fill_color="black", back_color="white")
    
    
    # Save the image
    # img.save(r"C:\Users\limzy\OneDrive\Desktop\Projects\ballot\qrcodes\my_qrcode.png")