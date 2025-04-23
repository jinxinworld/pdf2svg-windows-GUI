from PIL import Image
import cairosvg
import io

# 将SVG转换为PNG
png_data = cairosvg.svg2png(url="app.ico", output_width=256, output_height=256)

# 从PNG数据创建PIL图像
img = Image.open(io.BytesIO(png_data))

# 创建不同尺寸的图标
sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
icons = [img.resize(size, Image.Resampling.LANCZOS) for size in sizes]

# 保存为ICO文件
icons[0].save(
    "app.ico",
    format="ICO",
    sizes=[(i.width, i.height) for i in icons],
    append_images=icons[1:]
)