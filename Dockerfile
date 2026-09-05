# Gunakan base image Python versi slim agar ukurannya kecil
FROM python:3.11-slim

# Mencegah Python membuat file .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Memastikan output Python langsung dikirim ke terminal (berguna untuk melihat log bot)
ENV PYTHONUNBUFFERED=1

# Set direktori kerja di dalam container
WORKDIR /app

# Salin requirements.txt terlebih dahulu untuk efisiensi caching Docker
COPY requirements.txt .

# Install dependencies yang dibutuhkan (discord.py)
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh file kode (bot.py) ke dalam container
COPY . .

# Perintah default untuk menjalankan bot
CMD ["python", "bot.py"]