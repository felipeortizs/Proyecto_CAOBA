# Validador de Datos

Este servicio valida los datos tipo vector y raster. Corre en un endpoint web donde recibe un tipo de dato como enum y la URI en s3.

## Poner authenticación de AWS
Ir al archivo app.py y cambiar estos campos
```python
session = boto3.Session(
    aws_access_key_id="",
    aws_secret_access_key="",
    aws_session_token="",
)
```
## Instalar Docker en Ubuntu

```bash
sh dockersetup.sh
```
Para instalar docker en otros sistemas operativos ve a esta [URL](https://docs.docker.com/engine/install/).

## Correr el proyecto
```bash
sudo docker build -t proyecto-maestria .
sudo docker run -p 8000:8000 proyecto-maestria
```
El proyecto queda corriendo en el puerto 8000 de tu maquina.
