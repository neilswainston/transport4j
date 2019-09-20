FROM python

# Make current directory visible inside Docker container:
COPY . /transport4j
WORKDIR /transport4j

# Install requirements:
RUN pip install --upgrade pip \
	&& pip install -r requirements.txt

# Update paths:
ENV PYTHONPATH $PYTHONPATH:.

# Run:
ENTRYPOINT ["python", "-u", "transport4j/parser.py", "data", "neo4j/input"]