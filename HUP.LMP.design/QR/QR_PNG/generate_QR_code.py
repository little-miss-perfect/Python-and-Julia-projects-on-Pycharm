import qrcode
from PIL import Image


# Data for the QR code (make sure this is your actual URL)
data = "https://www.instagram.com/p/DEoKj2wRFvf/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA=="

# Create the QR code
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(data)
qr.make(fit=True)

# Create the QR image
qr_img = qr.make_image(fill="black", back_color="white").convert("RGBA")

# Make the white background transparent
datas = qr_img.getdata()
new_data = []
for item in datas:
    # Convert white (255,255,255) to fully transparent (255,255,255,0)
    if item[:3] == (255, 255, 255):
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)  # Keep the QR code as is

# Apply the new transparent background
qr_img.putdata(new_data)

# Save the QR code with transparency
qr_img.save("qr_transparent.png")

# Show the QR code
qr_img.show()
