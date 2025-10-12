#!/usr/bin/env python3
"""
CIFRADO DE HILL - Script de Consola Interactivo (CORREGIDO)
=============================================================
Implementación completa del cifrado de Hill usando álgebra lineal.
Alfabeto: A=0, B=1, ..., Z=25 (26 letras)

CORRECCIÓN: Matriz de cofactores ahora calcula correctamente [[d,-c],[-b,a]]
"""

import numpy as np
from math import gcd

ALFABETO = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def gcd_extendido(a, b):
    """
    Algoritmo de Euclides Extendido.
    Retorna (gcd, x, y) donde gcd = a*x + b*y
    """
    if a == 0:
        return b, 0, 1
    
    gcd_val, x1, y1 = gcd_extendido(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd_val, x, y


def inverso_modular(a, m):
    """
    Calcula el inverso modular de 'a' módulo 'm'.
    Retorna el inverso si existe, None si no existe.
    """
    gcd_val, x, _ = gcd_extendido(a, m)
    
    if gcd_val != 1:
        return None  # No existe inverso
    
    return (x % m + m) % m


def determinante_2x2(matriz):
    """
    Calcula el determinante de una matriz 2x2.
    det = a*d - b*c
    """
    return int(matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0])


def determinante_3x3(matriz):
    """
    Calcula el determinante de una matriz 3x3.
    Usa la regla de Sarrus.
    """
    a, b, c = matriz[0]
    d, e, f = matriz[1]
    g, h, i = matriz[2]
    
    det = (a*e*i + b*f*g + c*d*h) - (c*e*g + b*d*i + a*f*h)
    return int(det)


def matriz_cofactores_2x2(matriz):
    """
    Calcula la matriz de cofactores de una matriz 2x2.
    
    IMPORTANTE: Para matriz [[a,b],[c,d]], los cofactores son:
    [[d, -c],
     [-b, a]]
     
    NO confundir con [[d,-b],[-c,a]] que es incorrecto.
    """
    return np.array([
        [matriz[1][1], -matriz[1][0]],   # [d, -c]
        [-matriz[0][1], matriz[0][0]]    # [-b, a]
    ])


def matriz_cofactores_3x3(matriz):
    """
    Calcula la matriz de cofactores de una matriz 3x3.
    """
    cofactores = np.zeros((3, 3), dtype=int)
    
    for i in range(3):
        for j in range(3):
            # Crear submatriz 2x2 eliminando fila i y columna j
            submatriz = []
            for fila in range(3):
                if fila != i:
                    fila_temp = []
                    for col in range(3):
                        if col != j:
                            fila_temp.append(matriz[fila][col])
                    submatriz.append(fila_temp)
            
            # Calcular menor (determinante de la submatriz)
            menor = submatriz[0][0] * submatriz[1][1] - submatriz[0][1] * submatriz[1][0]
            
            # Aplicar signo alternado
            cofactores[i][j] = ((-1) ** (i + j)) * menor
    
    return cofactores


def matriz_inversa_modular(matriz, modulo=26):
    """
    Calcula la matriz inversa modular.
    
    Proceso:
    1. Calcular determinante
    2. Verificar que det sea coprimo con módulo
    3. Calcular inverso modular del determinante
    4. Calcular matriz de cofactores
    5. Transponer (matriz adjunta)
    6. Multiplicar por inverso del determinante (mod 26)
    """
    n = len(matriz)
    
    # Calcular determinante
    if n == 2:
        det = determinante_2x2(matriz)
    elif n == 3:
        det = determinante_3x3(matriz)
    else:
        raise ValueError("Solo matrices 2x2 o 3x3 soportadas")
    
    # Determinante módulo 26
    det = det % modulo
    
    # Verificar que sea coprimo con 26
    if gcd(det, modulo) != 1:
        raise ValueError(f"Determinante {det} no es coprimo con {modulo}")
    
    # Inverso modular del determinante
    det_inv = inverso_modular(det, modulo)
    
    # Matriz de cofactores
    if n == 2:
        cofactores = matriz_cofactores_2x2(matriz)
    else:
        cofactores = matriz_cofactores_3x3(matriz)
    
    # Adjunta (transpuesta de cofactores)
    adjunta = cofactores.T
    
    # Matriz inversa = det_inv * adjunta (mod 26)
    inversa = (det_inv * adjunta) % modulo
    
    return inversa.astype(int)


def validar_matriz_clave(matriz):
    """
    Valida que una matriz sea válida como clave para Hill.
    
    Requisitos:
    1. Debe ser cuadrada (2x2 o 3x3)
    2. Determinante debe ser coprimo con 26
    """
    n = len(matriz)
    
    # Verificar que sea cuadrada
    if not all(len(fila) == n for fila in matriz):
        return False, "La matriz no es cuadrada"
    
    # Solo soportamos 2x2 o 3x3
    if n not in [2, 3]:
        return False, "Solo matrices 2x2 o 3x3 son soportadas"
    
    # Calcular determinante
    if n == 2:
        det = determinante_2x2(matriz)
    else:
        det = determinante_3x3(matriz)
    
    det = det % 26
    
    # Verificar coprimalidad
    if gcd(det, 26) != 1:
        return False, f"Determinante {det} no es coprimo con 26 (MCD = {gcd(det, 26)})"
    
    return True, f"✓ Matriz válida (det = {det})"


def texto_a_numeros(texto):
    """Convierte texto a lista de números (A=0...Z=25)."""
    texto_limpio = ''.join(c.upper() for c in texto if c.isalpha())
    return [ord(c) - ord('A') for c in texto_limpio]


def numeros_a_texto(numeros):
    """Convierte lista de números a texto."""
    return ''.join(chr(n + ord('A')) for n in numeros)


def cifrar_hill(texto, matriz_clave):
    """
    Cifra un texto usando el Cifrado de Hill.
    
    Proceso:
    1. Validar la matriz clave
    2. Convertir texto a números
    3. Agrupar en bloques del tamaño de la matriz
    4. Para cada bloque:
       - Multiplicar matriz_clave × vector_bloque
       - Aplicar módulo 26
    5. Convertir resultado a texto
    
    Parámetros:
        texto: mensaje a cifrar
        matriz_clave: matriz cuadrada (2x2 o 3x3)
    
    Retorna:
        Tupla (texto_cifrado, bloques_detallados)
    """
    # Validar matriz
    es_valida, mensaje = validar_matriz_clave(matriz_clave)
    if not es_valida:
        raise ValueError(f"Matriz inválida: {mensaje}")
    
    # Convertir a numpy array
    matriz = np.array(matriz_clave, dtype=int)
    n = len(matriz)
    
    # Convertir texto a números
    numeros = texto_a_numeros(texto)
    
    # Agregar padding si es necesario
    while len(numeros) % n != 0:
        numeros.append(23)  # Agregar 'X' como padding
    
    # Cifrar por bloques
    texto_cifrado = []
    bloques_detallados = []
    
    for i in range(0, len(numeros), n):
        # Extraer bloque
        bloque = numeros[i:i+n]
        vector = np.array(bloque).reshape(n, 1)
        
        # Multiplicar matriz × vector (mod 26)
        resultado = (matriz @ vector) % 26
        
        # Guardar resultado
        bloque_cifrado = resultado.flatten().tolist()
        texto_cifrado.extend(bloque_cifrado)
        
        # Guardar detalles
        bloques_detallados.append({
            'indice': i // n,
            'bloque_original': bloque,
            'texto_original': numeros_a_texto(bloque),
            'vector': vector.flatten().tolist(),
            'bloque_cifrado': bloque_cifrado,
            'texto_cifrado': numeros_a_texto(bloque_cifrado)
        })
    
    return numeros_a_texto(texto_cifrado), bloques_detallados


def descifrar_hill(texto_cifrado, matriz_clave):
    """
    Descifra un texto usando el Cifrado de Hill.
    
    Proceso:
    1. Calcular la matriz inversa de la clave
    2. Convertir texto cifrado a números
    3. Agrupar en bloques
    4. Para cada bloque:
       - Multiplicar matriz_inversa × vector_bloque
       - Aplicar módulo 26
    5. Convertir resultado a texto
    
    Parámetros:
        texto_cifrado: mensaje cifrado
        matriz_clave: matriz usada en el cifrado
    
    Retorna:
        Tupla (texto_descifrado, bloques_detallados)
    """
    # Validar matriz
    es_valida, mensaje = validar_matriz_clave(matriz_clave)
    if not es_valida:
        raise ValueError(f"Matriz inválida: {mensaje}")
    
    # Calcular matriz inversa
    matriz = np.array(matriz_clave, dtype=int)
    matriz_inv = matriz_inversa_modular(matriz)
    n = len(matriz)
    
    # Convertir texto a números
    numeros = texto_a_numeros(texto_cifrado)
    
    # Descifrar por bloques
    texto_descifrado = []
    bloques_detallados = []
    
    for i in range(0, len(numeros), n):
        # Extraer bloque
        bloque = numeros[i:i+n]
        vector = np.array(bloque).reshape(n, 1)
        
        # Multiplicar matriz_inversa × vector (mod 26)
        resultado = (matriz_inv @ vector) % 26
        
        # Guardar resultado
        bloque_descifrado = resultado.flatten().tolist()
        texto_descifrado.extend(bloque_descifrado)
        
        # Guardar detalles
        bloques_detallados.append({
            'indice': i // n,
            'bloque_cifrado': bloque,
            'texto_cifrado': numeros_a_texto(bloque),
            'vector': vector.flatten().tolist(),
            'bloque_descifrado': bloque_descifrado,
            'texto_descifrado': numeros_a_texto(bloque_descifrado)
        })
    
    return numeros_a_texto(texto_descifrado), bloques_detallados


def mostrar_matriz(matriz, nombre="Matriz"):
    """Muestra una matriz de forma visual."""
    print(f"\n{nombre}:")
    n = len(matriz)
    for i in range(n):
        print("│ ", end="")
        for j in range(n):
            print(f"{matriz[i][j]:4d} ", end="")
        print("│")


def mostrar_detalles_cifrado(bloques, matriz):
    """Muestra los detalles del cifrado bloque por bloque."""
    print("\n" + "="*80)
    print("DETALLES DEL CIFRADO POR BLOQUES")
    print("="*80)
    
    for b in bloques:
        print(f"\nBloque {b['indice'] + 1}:")
        print("-"*80)
        print(f"Texto original:  {b['texto_original']} → {b['bloque_original']}")
        print(f"\nOperación matricial:")
        
        n = len(matriz)
        for i in range(n):
            print("│ ", end="")
            for j in range(n):
                print(f"{matriz[i][j]:3d} ", end="")
            print("│   │ ", end="")
            print(f"{b['vector'][i]:3d} ", end="")
            
            if i == n // 2:
                print("│ = │ ", end="")
            else:
                print("│   │ ", end="")
            
            print(f"{b['bloque_cifrado'][i]:3d} ", end="")
            print("│ (mod 26)")
        
        print(f"\nTexto cifrado:   {b['texto_cifrado']} → {b['bloque_cifrado']}")


def mostrar_detalles_descifrado(bloques, matriz_inv):
    """Muestra los detalles del descifrado bloque por bloque."""
    print("\n" + "="*80)
    print("DETALLES DEL DESCIFRADO POR BLOQUES")
    print("="*80)
    
    for b in bloques:
        print(f"\nBloque {b['indice'] + 1}:")
        print("-"*80)
        print(f"Texto cifrado:   {b['texto_cifrado']} → {b['bloque_cifrado']}")
        print(f"\nOperación matricial (con matriz inversa):")
        
        n = len(matriz_inv)
        for i in range(n):
            print("│ ", end="")
            for j in range(n):
                print(f"{matriz_inv[i][j]:3d} ", end="")
            print("│   │ ", end="")
            print(f"{b['vector'][i]:3d} ", end="")
            
            if i == n // 2:
                print("│ = │ ", end="")
            else:
                print("│   │ ", end="")
            
            print(f"{b['bloque_descifrado'][i]:3d} ", end="")
            print("│ (mod 26)")
        
        print(f"\nTexto original:  {b['texto_descifrado']} → {b['bloque_descifrado']}")


def verificar_matrices():
    """Función de prueba para verificar la corrección."""
    print("\n" + "="*80)
    print(" "*25 + "VERIFICACIÓN DE CORRECCIÓN")
    print("="*80)
    
    # Ejemplo del enunciado: HI -> FW
    print("\n📝 Test 1: Mensaje 'HI' con matriz [[7,1],[2,1]]")
    print("-"*80)
    
    mensaje = "HI"
    matriz = np.array([[7, 1], [2, 1]])
    
    print(f"Mensaje: {mensaje}")
    print(f"Matriz clave:")
    mostrar_matriz(matriz, "K")
    
    # Calcular determinante
    det = determinante_2x2(matriz)
    print(f"\nDeterminante: {det}")
    print(f"det mod 26: {det % 26}")
    print(f"MCD({det % 26}, 26) = {gcd(det % 26, 26)}")
    
    # Calcular inversa
    matriz_inv = matriz_inversa_modular(matriz)
    mostrar_matriz(matriz_inv, "K⁻¹")
    
    # Verificar K × K⁻¹ = I
    verificacion = (matriz @ matriz_inv) % 26
    print(f"\nVerificación: K × K⁻¹ (mod 26) =")
    mostrar_matriz(verificacion, "Resultado")
    es_identidad = np.array_equal(verificacion, np.eye(2, dtype=int))
    if es_identidad:
        print("✅ Es la matriz identidad - ¡CORRECTO!")
    else:
        print("❌ NO es la matriz identidad - ERROR")
    
    # Cifrar
    cifrado, bloques_cif = cifrar_hill(mensaje, matriz)
    print(f"\n🔒 Cifrado: {mensaje} → {cifrado}")
    print(f"   Esperado: FW")
    if cifrado == "FW":
        print("   ✅ CORRECTO")
    else:
        print(f"   ❌ ERROR - Se obtuvo {cifrado}")
    
    # Descifrar
    descifrado, bloques_desc = descifrar_hill(cifrado, matriz)
    print(f"\n🔓 Descifrado: {cifrado} → {descifrado}")
    print(f"   Esperado: {mensaje}")
    if descifrado == mensaje:
        print("   ✅ CORRECTO")
    else:
        print(f"   ❌ ERROR - Se obtuvo {descifrado}")
    
    # Más pruebas
    print("\n" + "="*80)
    print("📝 Test 2: Mensaje 'HELP' con matriz [[3,3],[2,5]]")
    print("-"*80)
    
    mensaje2 = "HELP"
    matriz2 = np.array([[3, 3], [2, 5]])
    
    print(f"Mensaje: {mensaje2}")
    cifrado2, _ = cifrar_hill(mensaje2, matriz2)
    descifrado2, _ = descifrar_hill(cifrado2, matriz2)
    
    print(f"Cifrado: {cifrado2}")
    print(f"Descifrado: {descifrado2}")
    
    if descifrado2 == mensaje2:
        print("✅ CORRECTO - El descifrado coincide con el original")
    else:
        print(f"❌ ERROR - {descifrado2} != {mensaje2}")
    
    print("\n" + "="*80)


def menu_principal():
    """Menú interactivo principal."""
    print("\n" + "="*80)
    print(" "*26 + "CIFRADO DE HILL")
    print("="*80)
    print("\nCaracterísticas:")
    print("  • Cifrado por bloques usando álgebra lineal")
    print("  • Usa matrices como clave")
    print("  • La clave debe tener determinante coprimo con 26")
    print("  • Más seguro que cifrados letra por letra")
    print("\nAlfabeto: A=0, B=1, C=2, ..., Z=25")
    print("="*80)
    
    while True:
        print("\n┌─── MENÚ PRINCIPAL ────────────┐")
        print("│ 1. Cifrar mensaje             │")
        print("│ 2. Descifrar mensaje          │")
        print("│ 3. Validar matriz             │")
        print("│ 4. Verificar corrección       │")
        print("│ 5. Ver casos de uso           │")
        print("│ 6. Salir                      │")
        print("└───────────────────────────────┘")
        
        opcion = input("\nSeleccione una opción [1-6]: ").strip()
        
        if opcion == '1':
            cifrar_mensaje()
        elif opcion == '2':
            descifrar_mensaje()
        elif opcion == '3':
            validar_matriz_menu()
        elif opcion == '4':
            verificar_matrices()
        elif opcion == '5':
            mostrar_casos_uso()
        elif opcion == '6':
            print("\n¡Hasta pronto! 👋\n")
            break
        else:
            print("\n❌ Opción inválida.")


def cifrar_mensaje():
    """Interfaz para cifrar un mensaje."""
    print("\n" + "─"*80)
    print("CIFRADO DE MENSAJE")
    print("─"*80)
    
    mensaje = input("Ingrese el mensaje a cifrar: ").strip()
    if not mensaje:
        print("❌ El mensaje no puede estar vacío.")
        return
    
    print("\nTamaño de matriz:")
    print("1. Matriz 2x2")
    print("2. Matriz 3x3")
    
    opcion = input("Seleccione [1-2]: ").strip()
    
    try:
        if opcion == '1':
            print("\nIngrese matriz 2x2 (4 números):")
            print("Formato: a b c d  (para matriz [[a,b],[c,d]])")
            valores = input("Valores: ").strip().split()
            if len(valores) != 4:
                print("❌ Debe ingresar 4 valores.")
                return
            matriz = [[int(valores[0]), int(valores[1])],
                     [int(valores[2]), int(valores[3])]]
        elif opcion == '2':
            print("\nIngrese matriz 3x3 (9 números):")
            print("Formato: a b c d e f g h i")
            valores = input("Valores: ").strip().split()
            if len(valores) != 9:
                print("❌ Debe ingresar 9 valores.")
                return
            matriz = [[int(valores[0]), int(valores[1]), int(valores[2])],
                     [int(valores[3]), int(valores[4]), int(valores[5])],
                     [int(valores[6]), int(valores[7]), int(valores[8])]]
        else:
            print("❌ Opción inválida.")
            return
        
        print(f"\n📝 Mensaje: {mensaje}")
        mostrar_matriz(matriz, "Matriz clave")
        
        # Validar
        es_valida, msg = validar_matriz_clave(matriz)
        print(f"\n{msg}")
        
        if not es_valida:
            return
        
        # Cifrar
        texto_cifrado, bloques = cifrar_hill(mensaje, matriz)
        
        mostrar_detalles_cifrado(bloques, matriz)
        
        print("\n" + "="*80)
        print(f"🔒 MENSAJE CIFRADO: {texto_cifrado}")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def descifrar_mensaje():
    """Interfaz para descifrar un mensaje."""
    print("\n" + "─"*80)
    print("DESCIFRADO DE MENSAJE")
    print("─"*80)
    
    mensaje_cifrado = input("Ingrese el mensaje cifrado: ").strip()
    if not mensaje_cifrado:
        print("❌ El mensaje no puede estar vacío.")
        return
    
    print("\nTamaño de matriz:")
    print("1. Matriz 2x2")
    print("2. Matriz 3x3")
    
    opcion = input("Seleccione [1-2]: ").strip()
    
    try:
        if opcion == '1':
            print("\nIngrese matriz 2x2 usada en el cifrado:")
            valores = input("Valores (a b c d): ").strip().split()
            if len(valores) != 4:
                print("❌ Debe ingresar 4 valores.")
                return
            matriz = [[int(valores[0]), int(valores[1])],
                     [int(valores[2]), int(valores[3])]]
        elif opcion == '2':
            print("\nIngrese matriz 3x3 usada en el cifrado:")
            valores = input("Valores (a b c d e f g h i): ").strip().split()
            if len(valores) != 9:
                print("❌ Debe ingresar 9 valores.")
                return
            matriz = [[int(valores[0]), int(valores[1]), int(valores[2])],
                     [int(valores[3]), int(valores[4]), int(valores[5])],
                     [int(valores[6]), int(valores[7]), int(valores[8])]]
        else:
            print("❌ Opción inválida.")
            return
        
        print(f"\n🔒 Mensaje cifrado: {mensaje_cifrado}")
        mostrar_matriz(matriz, "Matriz clave")
        
        # Calcular matriz inversa
        matriz_np = np.array(matriz)
        matriz_inv = matriz_inversa_modular(matriz_np)
        mostrar_matriz(matriz_inv, "Matriz inversa (mod 26)")
        
        # Descifrar
        texto_descifrado, bloques = descifrar_hill(mensaje_cifrado, matriz)
        
        mostrar_detalles_descifrado(bloques, matriz_inv)
        
        print("\n" + "="*80)
        print(f"🔓 MENSAJE DESCIFRADO: {texto_descifrado}")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def validar_matriz_menu():
    """Interfaz para validar una matriz."""
    print("\n" + "─"*80)
    print("VALIDAR MATRIZ")
    print("─"*80)
    
    print("\nTamaño de matriz:")
    print("1. Matriz 2x2")
    print("2. Matriz 3x3")
    
    opcion = input("Seleccione [1-2]: ").strip()
    
    try:
        if opcion == '1':
            print("\nIngrese matriz 2x2:")
            valores = input("Valores (a b c d): ").strip().split()
            if len(valores) != 4:
                print("❌ Debe ingresar 4 valores.")
                return
            matriz = [[int(valores[0]), int(valores[1])],
                     [int(valores[2]), int(valores[3])]]
            det = determinante_2x2(matriz)
        elif opcion == '2':
            print("\nIngrese matriz 3x3:")
            valores = input("Valores (a b c d e f g h i): ").strip().split()
            if len(valores) != 9:
                print("❌ Debe ingresar 9 valores.")
                return
            matriz = [[int(valores[0]), int(valores[1]), int(valores[2])],
                     [int(valores[3]), int(valores[4]), int(valores[5])],
                     [int(valores[6]), int(valores[7]), int(valores[8])]]
            det = determinante_3x3(matriz)
        else:
            print("❌ Opción inválida.")
            return
        
        mostrar_matriz(matriz, "Matriz ingresada")
        
        print(f"\nDeterminante: {det}")
        print(f"Determinante mod 26: {det % 26}")
        print(f"MCD(det, 26): {gcd(det % 26, 26)}")
        
        es_valida, mensaje = validar_matriz_clave(matriz)
        print(f"\n{mensaje}")
        
        if es_valida:
            matriz_np = np.array(matriz)
            matriz_inv = matriz_inversa_modular(matriz_np)
            mostrar_matriz(matriz_inv, "Matriz inversa (mod 26)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def mostrar_casos_uso():
    """Muestra casos de uso predefinidos."""
    print("\n" + "="*80)
    print(" "*28 + "CASOS DE USO")
    print("="*80)
    
    casos = [
        {
            'nombre': 'Caso 1: HI (del enunciado)',
            'mensaje': 'HI',
            'matriz': [[7, 1], [2, 1]]
        },
        {
            'nombre': 'Caso 2: HELP con matriz simple',
            'mensaje': 'HELP',
            'matriz': [[3, 3], [2, 5]]
        },
        {
            'nombre': 'Caso 3: ATTACK',
            'mensaje': 'ATTACK',
            'matriz': [[5, 8], [17, 3]]
        }
    ]
    
    for caso in casos:
        print(f"\n{'─'*80}")
        print(f"{caso['nombre']}")
        print(f"{'─'*80}")
        print(f"Mensaje: {caso['mensaje']}")
        mostrar_matriz(caso['matriz'], "Matriz")
        
        try:
            es_valida, msg = validar_matriz_clave(caso['matriz'])
            print(f"\n{msg}")
            
            if es_valida:
                cifrado, _ = cifrar_hill(caso['mensaje'], caso['matriz'])
                descifrado, _ = descifrar_hill(cifrado, caso['matriz'])
                print(f"Cifrado:    {cifrado}")
                print(f"Descifrado: {descifrado}")
                if descifrado == caso['mensaje']:
                    print("✅ Verificación exitosa")
                else:
                    print("❌ Error en descifrado")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    menu_principal()