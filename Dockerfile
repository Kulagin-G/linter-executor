FROM python:3.10-slim as linter

FROM linter as distr
USER root
RUN apt-get update \
    && apt-get install git curl -y

FROM linter
USER root
ENV PYTHONUNBUFFERED true

ARG WORKDIR="/linter-executor"
ARG USER="python"
ARG GROUP="python"

RUN adduser ${USER} --shell /bin/bash --disabled-password \
    && adduser ${USER} ${GROUP} \
    && mkdir -p ${WORKDIR}

COPY . "${WORKDIR}"

RUN pip3.10 install -r "${WORKDIR}/requirements.txt" \
 && chmod -R +x "${WORKDIR}" \
 && chown -R "${USER}":"${GROUP}" "${WORKDIR}" \
 && ln -s /usr/local/bin/python3 /usr/bin/python3

COPY --from=distr /usr/bin/git /usr/bin/git

USER "${USER}"
WORKDIR "${WORKDIR}"
ENTRYPOINT ["./linter.py"]
