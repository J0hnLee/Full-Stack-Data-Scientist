FROM python:3.13-bullseye

WORKDIR /code

# 安裝 Playwright 所需的系統依賴
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxcb-render0 \
    libxcb-render-util0 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libxcb-randr0 \
    libxcb-glx0 \
    libxcb-shm0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-xtest0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxcb-dri2-0 \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

RUN crawl4ai-setup

# 安裝 Playwright 瀏覽器
#RUN playwright install chromium
# RUN playwright install-deps