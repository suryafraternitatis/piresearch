import networkx as nx
import matplotlib.pyplot as plt


def is_repdigit_binary(numero):
    numero_binario = bin(int(numero))[2:]
    return len(set(numero_binario)) == 1


def find_repdigit_binary_substrings(cadena):
    repdigits = {}  # Diccionario de tuplas (digito, [posiciones])
    for i in range(len(cadena)):
        for j in range(i+1, len(cadena)+1):
            subcadena = cadena[i:j]
            if is_repdigit_binary(int(subcadena)):
                if subcadena not in repdigits:
                    repdigits[subcadena] = 0
                repdigits[subcadena] += 1
    return repdigits

def analyze_non_repdigit_influence(cadena):
    repdigits = find_repdigit_binary_substrings(cadena)
    non_repdigits = {}
    for repdigit, count in repdigits.items():
        non_repdigits[repdigit] = []
        for i in range(count):
            for pos in [m.start() for m in re.finditer(repdigit, cadena)]:
                if pos > 0:
                    num_antecesor = int(cadena[pos-1])
                    num_antecesor_bin = bin(num_antecesor)[2:]
                    if not is_repdigit_binary(num_antecesor_bin):
                        non_repdigits[repdigit].append((num_antecesor, -1, pos-1))
                if pos < len(cadena)-len(repdigit):
                    num_sucesor = int(cadena[pos+len(repdigit)])
                    num_sucesor_bin = bin(num_sucesor)[2:]
                    if not is_repdigit_binary(num_sucesor_bin):
                        non_repdigits[repdigit].append((num_sucesor, 1, pos+len(repdigit)))
        non_repdigits[repdigit].sort(key=lambda x: x[2])
    return non_repdigits

def analyze_stats_non_repdigit_influence(cadena):
    repdigits = find_repdigit_binary_substrings(cadena)
    non_repdigits = {}

    for repdigit in repdigits.keys():
        non_repdigits[repdigit] = {}
        non_repdigits[repdigit]['positions'] = [m.start() for m in re.finditer(repdigit, cadena)]
        non_repdigits[repdigit]['total_digits'] = len(repdigit)
        non_repdigits[repdigit]['non_repdigit_neighbors'] = {'antecesor': 0, 'sucesor': 0}
        non_repdigits[repdigit]['repdigit_neighbors'] = {'antecesor': 0, 'sucesor': 0}
        non_repdigits[repdigit]['same_digit_neighbors'] = {'antecesor': 0, 'sucesor': 0}

        for i in range(len(non_repdigits[repdigit]['positions'])):
            pos = non_repdigits[repdigit]['positions'][i]
            if pos > 0:
                prev_digit = cadena[pos - 1]
                if prev_digit == repdigit[0]:
                    non_repdigits[repdigit]['same_digit_neighbors']['antecesor'] += 1
                elif prev_digit not in repdigits:
                    non_repdigits[repdigit]['non_repdigit_neighbors']['antecesor'] += 1
                else:
                    non_repdigits[repdigit]['repdigit_neighbors']['antecesor'] += 1

            if pos < len(cadena) - non_repdigits[repdigit]['total_digits']:
                next_digit = cadena[pos + non_repdigits[repdigit]['total_digits']]
                if next_digit == repdigit[-1]:
                    non_repdigits[repdigit]['same_digit_neighbors']['sucesor'] += 1
                elif next_digit not in repdigits:
                    non_repdigits[repdigit]['non_repdigit_neighbors']['sucesor'] += 1
                else:
                    non_repdigits[repdigit]['repdigit_neighbors']['sucesor'] += 1

    return non_repdigits


cadena = "411"
influence = analyze_non_repdigit_influence(cadena)
stats = analyze_stats_non_repdigit_influence(cadena)

print(influence)
print(stats)