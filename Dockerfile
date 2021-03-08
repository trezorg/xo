FROM python:3.9-slim

ENV USER=xo \
    USER_ID=1000 \
    APP_PORT=8080 \
    APP_HOST=0.0.0.0 \
    LOG_LEVEL="INFO" \
    DEBUG='False' \
    PROJECT_PATH="/var/app" \
    LANG="C.UTF-8" \
    LANGUAGE="C.UTF-8" \
    LC_ALL="C.UTF-8"

RUN echo "Creating user, installing applications..." && \
    pip install --no-cache-dir -U pipenv && \
    apt update -y && \
    apt install -y netcat && \
    useradd -m -o -u ${USER_ID} -d ${PROJECT_PATH} ${USER} && \
    rm -rf /var/lib/apt/lists/*

WORKDIR ${PROJECT_PATH}
EXPOSE ${PORT}
CMD ["/usr/local/bin/gunicorn", "-c", "gunicorn.py", "main:app"]

ADD Pipfile* ${PROJECT_PATH}/
ARG WITH_DEV_PACKAGES=no

RUN cd ${PROJECT_PATH} && \
    [ "${WITH_DEV_PACKAGES}" = "yes" ] && dev_packages_param="-d" || dev_packages_param="" && \
    echo "Installing python packages`[ "${WITH_DEV_PACKAGES}" = "yes" ] && echo " in dev mode"`..." && \
    pipenv install ${dev_packages_param} --deploy --system

ADD . ${PROJECT_PATH}

RUN echo "System commands..." && \
    cd ${PROJECT_PATH} && \
    [ "${WITH_DEV_PACKAGES}" != "yes" ] && rm -rf tests || true && \
    chown -R ${USER}:${USER} ${PROJECT_PATH}

USER ${USER_ID}
EXPOSE ${APP_PORT}
