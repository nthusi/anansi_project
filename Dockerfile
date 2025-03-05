# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies & TailwindCSS globally
RUN npm install -g tailwindcss

# Copy the rest of the application code
COPY . .

# Install project-specific Node.js dependencies
RUN npm install

# Build TailwindCSS styles
RUN npm run build

# Ensure Bootstrap & frontend dependencies are installed
RUN npm install bootstrap

# Rebuild Bootstrap to ensure source maps exist
RUN npm rebuild bootstrap

# Ensure `build/js/` directory exists before running `find`
RUN mkdir -p build/js/ && find build/js/ -type f -name "*.js" -exec sed -i '/sourceMappingURL/d' {} + || true

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose necessary ports
EXPOSE 8000 3000

# Run the application
CMD ["sh", "-c", "npm run start & gunicorn --bind 0.0.0.0:8000 anansi_app.wsgi:application"]