from ipaddress import ip_address
from re import findall
from sys import argv, exit
from os.path import isfile
from prettytable import PrettyTable


def array_to_ip(arr):
    return '.'.join([str(x) for x in arr])


def calculate_n(devices):
    n = 0
    while devices > 2**n - 2:
        n += 1
    return n


def calculate_mask(prefix):
    bin_prefix = ''.rjust(32, '0')
    for _ in range(prefix):
        bin_prefix = bin_prefix.replace('0', '1', 1)

    octs = [int(x, 2) for x in findall(r'.{8}', bin_prefix)]
    return octs


def calculate_prefix(n):
    return 32 - n


def get_file_info(path):
    with open(path) as f:
        lines = f.readlines()
        ipv4 = lines[0].replace('\n', '')
        redes = lines[1:]
        sub_redes = []
        total_ips = 0
        for x in redes:
            name = x.split('-')[0]
            size = int(x.split('-')[1].replace('\n', ''))
            n = calculate_n(size)
            capacity = 2**n
            sub_redes.append({'name': name, 'needed_size': size, 'allocated_size': capacity-2,
                              'capacity': capacity, 'n': n})
            total_ips += capacity
        sub_redes.sort(key=lambda x: x['needed_size'], reverse=True)
    return ipv4, sub_redes, total_ips


def main():
    redes = PrettyTable()
    path = argv[1]
    if not isfile(path):
        print("Ingrese un archivo como parametro para el programa")
        exit(1)
    ipv4, sub_redes, total_ips = get_file_info(path)
    n = calculate_n(total_ips)
    prefix = calculate_prefix(n)
    ip = [int(x) for x in ipv4.split('.')]
    print(f'{ipv4}/{prefix}')
    mask = calculate_mask(prefix)
    real_octs = []
    for i in range(len(mask)):
        real_octs.append(int(bin(ip[i] & mask[i]), 2))

    red = ip_address(array_to_ip(real_octs))
    redes.field_names = ["Nombre", "Tamaño necesitado", "Tamaño asignado", "Dirección de red", "Primera dirección asignable",
                         "Ultima dirección asignable", "Broadcast", "Prefijo", "Mascara de subred"]
    for sub_red in sub_redes:
        row = []
        hosts = sub_red['allocated_size']
        row.append(sub_red['name'])
        row.append(sub_red['needed_size'])
        row.append(sub_red['allocated_size'])
        # Dirección de red
        row.append(red)
        # Primera dirección asignable
        red += 1
        row.append(red)
        # Ultima dirección asignable
        red += hosts - 1
        row.append(red)
        # Broadcast
        broadcast = red
        broadcast += 1
        row.append(broadcast)
        # Prefijo de red
        n = sub_red['n']
        prefijo = calculate_prefix(n)
        row.append(f'/{prefijo}')
        # Mascara de subred
        row.append(array_to_ip(calculate_mask(prefijo)))

        redes.add_row(row)

        broadcast += 1
        red = broadcast

    print(redes)


if __name__ == '__main__':
    main()
