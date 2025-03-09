FROM fedora:37 AS base
FROM base AS builder

ENV PIP_PARAMS=""
ENV PIP_VERSION=23.0.1
ENV PLONE_VERSION=6.0.8

RUN mkdir /wheelhouse

RUN dnf update -y \
    && buildDeps="gcc-c++ gcc kernel-devel python3.9 patch openssl-devel libjpeg-devel libxslt-devel readline-devel make which python3-devel wv poppler-utils python3-virtualenv git libffi-devel glibc-devel bzip2-devel libjpeg-turbo-devel openldap-devel python3-tox lcov openjpeg2-devel pcre2-devel libpq-devel libgsasl-devel openssl-devel libtiff-devel libxml2-devel wget zlib-devel"\
    && dnf install -y $buildDeps\
    && pip install -U "pip==${PIP_VERSION}"\
    && dnf clean all\
    && rm -Rf /usr/share/doc

RUN pip install wheel 
RUN pip wheel Plone plone.volto -c https://dist.plone.org/release/6.0.8/constraints.txt --wheel-dir=/wheelhouse

FROM base

ENV PIP_PARAMS=""
ENV PIP_VERSION=23.0.1
ENV PLONE_VERSION=6.0.8

LABEL maintainer="Andrew Himelstieb <admin@hoa-colors.com>" \
      org.label-schema.name="plone-backend" \
      org.label-schema.description="Plone backend image image using Python 3.9 and Fedora 38" \
      org.label-schema.vendor="DenverMesh.org"

COPY --from=builder /wheelhouse /wheelhouse

RUN useradd --system -m -d /app -U -u 500 plone \
    && dnf update -y \
    && dnf install -y git python3-virtualenv libpq libtiff libxml2 wget zlib openjpeg2 libjpeg-turbo glibc libffi wv poppler-utils python3.9 bzip2 which make busybox libxslt lynx netcat rsync \
    && dnf clean all\
    && mkdir -p /data/filestorage /data/blobstorage /data/log /data/cache

WORKDIR /app

COPY skeleton/ /app
COPY requirements.txt /app

RUN virtualenv . \
    && source bin/activate\ 
    && ./bin/pip install -U "pip==${PIP_VERSION}" \
    && ./bin/pip install --force-reinstall --no-index --no-deps /wheelhouse/* \
    && ./bin/pip install -r requirements.txt \
    && find . \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' + \
    && rm -Rf .cache


RUN ln -s /data var \
    && find /data  -not -user plone -exec chown plone:plone {} \+ \
    && find /app -not -user plone -exec chown plone:plone {} \+

EXPOSE 8080
VOLUME /data

USER plone
ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["start"]
