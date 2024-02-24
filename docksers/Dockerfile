FROM python:3.11

RUN apt-get update && \
    apt-get install -y fonts-nanum wget unzip gnupg2 apt-transport-https

# Install Chrome and related dependencies
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
#     apt-get update && apt-get install -y google-chrome-stable && \

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

ARG BRANCH_NAME
ARG DIR_NAME
ARG GITHUB_URI

# Clone the Git repository. Here we dynamically specify the repository name using the variable defined earlier.
RUN git clone -b ${BRANCH_NAME} https://github.com/${GITHUB_URI} ${DIR_NAME}

# Changes the working directory to /app/${REPO_NAME}. This uses the variable to dynamically set the directory path.
WORKDIR /app/${DIR_NAME}

# RUN pip install --no-cache-dir -r ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt