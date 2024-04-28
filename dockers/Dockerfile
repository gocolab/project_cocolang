FROM python:3.11

RUN apt-get update && \
    apt-get install -y fonts-nanum wget unzip gnupg2 apt-transport-https

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /apps

ARG GIT_BRANCH_NAME
ARG APP_DIR_NAME
ARG GIT_URI

# Clone the Git repository. Here we dynamically specify the repository name using the variable defined earlier.
RUN git clone -b ${GIT_BRANCH_NAME} ${GIT_URI} ${APP_DIR_NAME}

# Changes the working directory to /apps/${REPO_NAME}. This uses the variable to dynamically set the directory path.
WORKDIR /apps/${APP_DIR_NAME}/app

# RUN pip install --no-cache-dir -r ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt