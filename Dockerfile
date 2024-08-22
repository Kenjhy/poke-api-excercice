# Etapa de construcción
FROM python:3.10 AS builder
WORKDIR /var/app/staging
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Etapa final
FROM python:3.10-slim
WORKDIR /var/app/current
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH

# Agrega esta línea para exponer el puerto 8000
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]