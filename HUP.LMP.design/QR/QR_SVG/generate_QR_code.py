import qrcode
import qrcode.image.svg

# Data for the QR code
data = "https://www.instagram.com/p/DEoKj2wRFvf/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA=="

# ✅ Use `SvgFillImage` for proper color application
factory = qrcode.image.svg.SvgFillImage  # Use this instead of SvgPathImage

# Create the QR code
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(data)
qr.make(fit=True)

# Generate the SVG QR code with custom colors
qr_svg = qr.make_image(
    fill_color="#4A2C6C",  # 🟣 Dark Purple
    back_color="none",      # Transparent background
    image_factory=factory   # ✅ Correct factory for colors
)

# Save the SVG file
qr_svg.save("LMP_QR.svg")
