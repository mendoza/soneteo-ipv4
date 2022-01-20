# Soneteo ipv4

## Como usar
Instalar las dependencias usando pipenv o ver el `Pipfile` para instalar una por una

### Instalando con pipenv

```cmd
# dependencias
> pipenv sync
> pipenv shell # este solo si no estas ya en la consola de pipenv
```

### Corriendo
```cmd
> python ./main.py ./entrada.txt
```

## Entrada
un archivo de texto con el siguiente formato:
- ipv4
- una red por linea, con el formato de `nombre-capacidad`

Ejemplo:
```
172.14.14.14
RRHH-16
IT-32
Gerencia-10
Contabilidad-21
WAN1-2
WAN2-2
WAN3-2
WAN4-2
```

## Salida
El ipv4 con su prefijo y una tabla con las siguientes columnas:

- Nombre
- Tamaño necesitado
- Tamaño asignado
- Dirección de red
- Primera dirección asignable
- Ultima dirección asignable
- Broadcast
- Prefijo
- Mascara de subred 