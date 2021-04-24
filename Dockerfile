# Import the environment-setter image.
FROM python:3.8.8-buster

# Add Django’s environment type.
ARG DJANGO_ENV

# Set up some environmental variables.
ENV DJANGO_ENV=${DJANGO_ENV} \
    LANG=C.UTF-8 \
    PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.5

# Set up the base working directory.
WORKDIR /app

# Install the OS’s package dependencies.
RUN apt-get update && \
    rm -rf /var/lib/apt/lists/* && \
    # Install poetry
    pip install "poetry==$POETRY_VERSION"

# Set up the virtual environment.
RUN python -m venv /venv

# Copy the project’s dependency files to the image.
COPY pyproject.toml poetry.lock ./

# Install the dependencies;
# export them as requirements.txt and install them using pip.
RUN poetry export -f requirements.txt $(test "$DJANGO_ENV" = development && echo "--dev") \
    | /venv/bin/pip install -r /dev/stdin

# --------------------------------------------------------

# Import the final image.
FROM python:3.8.8-slim-buster

# Add Django's secret key.
ARG DJANGO_SECRET_KEY

# Set up some environmental variables.
ENV LANG=C.UTF-8

# Set up the base working directory.
WORKDIR /app

# Go get the virtual environment from the environment-setter image.
COPY --from=0 /venv /venv

# Use the executables from the virtual environment.
ENV PATH="/venv/bin:$PATH"

# Copy all files to the this image.
COPY . .

# Move to the project’s root directory.
WORKDIR /app/steve

# Collect the assets.
RUN python manage.py collectstatic --no-input

# Add the script to be executed every time the container starts.
COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
EXPOSE 80 88 443 8000 8080 8443

# Run as a non-root user.
RUN useradd -m steveuser
USER steveuser

# Start the main process.
CMD ["/bin/bash", "./run.sh"]
