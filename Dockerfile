# Use a lightweight Python base image.
# We choose Python 3.10 as it's compatible with Plone 6 and 'slim-bookworm' provides a good balance
# between size and necessary libraries.
FROM python:3.10-slim-bookworm

# Set environment variables for non-buffered Python output and define Plone's home directory,
# user, and group for better organization and security.
ENV PYTHONUNBUFFERED 1
ENV PLONE_HOME /app
ENV PLONE_USER plone
ENV PLONE_GROUP plone

# Install system dependencies required for compiling Python packages and Plone itself.
# `build-essential` for compilers, `libssl-dev`, `libffi-dev` for cryptography,
# `libjpeg-dev`, `zlib1g-dev` for image processing, and `libxml2-dev`, `libxslt1-dev` for XML/XSLT handling.
# `--no-install-recommends` keeps the image size down.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    libxml2-dev \
    libxslt1-dev \
    # Clean up apt cache to reduce image size
    && rm -rf /var/lib/apt/lists/*

# Install 'uv', a fast Python package installer and resolver, globally.
# This will be used to install Plone and its dependencies.
RUN pip install uv


RUN useradd --system -m -d /app -U -u 500 plone \
    && mkdir -p /data/filestorage /data/blobstorage /data/log /data/cache


WORKDIR ${PLONE_HOME}

# Create a virtual environment using 'uv' inside PLONE_HOME.
# This isolates Plone's dependencies and ensures scripts are found correctly.
RUN uv venv .venv


COPY skeleton/ /app
COPY constraints.txt /app
COPY requirements.txt /app

# Install Plone using 'uv'.
# We specify Plone version 6.0.9 for stability. You can change this version as needed.
# 'uv' will handle dependency resolution and installation efficiently.
#RUN uv pip install Plone==6.0.9 --system
RUN uv pip install Plone==6.0.9 --python ${PLONE_HOME}/.venv/bin/python

RUN uv pip install ZEO --python ${PLONE_HOME}/.venv/bin/python

#Install plone addon's in the requirements.txt
RUN uv pip install -r requirements.txt

RUN ln -s /data var \
    && find /data  -not -user plone -exec chown plone:plone {} \+ \
    && find /app -not -user plone -exec chown plone:plone {} \+


# Switch to the 'plone' user for the next steps.
# This ensures that the Plone instance is created with the correct ownership and permissions.
USER ${PLONE_USER}

# Set the PATH for the plone user to include the virtual environment's bin directory.
# This ensures that executables like 'mkwsgiinstance' are found.
ENV PATH="${PLONE_HOME}/.venv/bin:${PATH}"

# Create a Plone instance using `mkwsgiinstance` from the virtual environment.
# This command sets up the necessary directory structure and configuration files for a Zope/Plone instance.
# `--user=admin:admin` sets up an initial Zope administrator user (CHANGE THIS IN PRODUCTION!).
# We also append lines to `zope.conf` to disable debug mode and verbose security for a cleaner
# and slightly more production-like setup.
RUN set -ex \
    && whoami \
    && pwd \
    && ls -la ${PLONE_HOME} \
    && mkwsgiinstance -d ${PLONE_HOME}/ --user=admin:admin \
    && echo "debug-mode off" >> ${PLONE_HOME}/etc/zope.conf \
    && echo "verbose-security off" >> ${PLONE_HOME}/etc/zope.conf \
    && ls -l ${PLONE_HOME}/.venv/bin \
    && test -f ${PLONE_HOME}/.venv/bin/runwsgi # Verify runwsgi exists

EXPOSE 8080
VOLUME /data

USER plone
ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["start"]
