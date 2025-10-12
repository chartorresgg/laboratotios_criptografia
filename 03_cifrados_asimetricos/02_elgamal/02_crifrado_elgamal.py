#!/usr/bin/env python3
"""
CIFRADO ELGAMAL - Script de Consola Interactivo
================================================
Implementación educativa del cifrado ElGamal (criptografía asimétrica).
Alfabeto: A=0, B=1, ..., Z=25

ElGamal es un sistema de clave pública basado en el problema del logaritmo discreto.
Usa tres claves: clave pública (p, g, h) y clave privada (x)
"""

import random


def es_primo(n, k=5):
    """
    Test de primalidad de Miller-Rabin.
    
    Determina si un número es probablemente primo con k rondas de prueba.
    
    Parámetros:
        n: número a probar
        k: número de rondas (más rondas = más confianza)
    
    Retorna:
        True si n es probablemente primo, False si es compuesto
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Escribir n-1 como 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Test de Miller-Rabin
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True


def generar_primo(bits=16):
    """
    Genera un número primo aleatorio de aproximadamente 'bits' bits.
    
    Para fines educativos, usamos números pequeños (16 bits ≈ 4-5 dígitos).
    En producción se usan primos de 2048+ bits.
    
    Parámetros:
        bits: tamaño aproximado en bits del primo
    
    Retorna:
        Un número primo
    """
    while True:
        candidato = random.randrange(2**(bits-1), 2**bits)
        if es_primo(candidato):
            return candidato


def generar_generador(p):
    """
    Encuentra un generador del grupo multiplicativo módulo p.
    
    Un generador g es un elemento tal que g^i mod p genera todos
    los elementos del grupo para i = 1, 2, ..., p-1.
    
    Para simplificar, usamos un generador común pequeño (2, 3, 5, etc.)
    que funcione para el primo dado.
    
    Parámetros:
        p: número primo
    
    Retorna:
        Un generador del grupo
    """
    # Para fines educativos, probamos generadores pequeños comunes
    for g in [2, 3, 5, 7, 11]:
        if pow(g, (p-1)//2, p) != 1:  # Test rápido
            return g
    
    # Si no encuentra uno pequeño, busca aleatoriamente
    for _ in range(100):
        g = random.randrange(2, p)
        if pow(g, (p-1)//2, p) != 1:
            return g
    
    return 2  # Fallback


def generar_claves(tamano_bits=16):
    """
    Genera un par de claves ElGamal (pública y privada).
    
    Proceso:
    1. Generar un primo grande p
    2. Encontrar un generador g del grupo multiplicativo mod p
    3. Elegir clave privada x aleatoria (1 < x < p-1)
    4. Calcular clave pública h = g^x mod p
    
    Parámetros:
        tamano_bits: tamaño del primo en bits (16 para educación)
    
    Retorna:
        Tupla ((p, g, h), x) donde:
        - (p, g, h): clave pública
        - x: clave privada
    """
    print(f"\n🔑 Generando claves ElGamal ({tamano_bits} bits)...")
    
    # 1. Generar primo p
    p = generar_primo(tamano_bits)
    print(f"   ✓ Primo p = {p}")
    
    # 2. Encontrar generador g
    g = generar_generador(p)
    print(f"   ✓ Generador g = {g}")
    
    # 3. Elegir clave privada x
    x = random.randrange(2, p - 1)
    print(f"   ✓ Clave privada x = {x}")
    
    # 4. Calcular clave pública h = g^x mod p
    h = pow(g, x, p)
    print(f"   ✓ Clave pública h = g^x mod p = {g}^{x} mod {p} = {h}")
    
    clave_publica = (p, g, h)
    clave_privada = x
    
    return clave_publica, clave_privada


def texto_a_numeros(texto):
    """
    Convierte texto a lista de números (A=0, B=1, ..., Z=25).
    
    Parámetros:
        texto: cadena de texto
    
    Retorna:
        Lista de números [0-25]
    """
    texto_limpio = ''.join(c.upper() for c in texto if c.isalpha())
    return [ord(c) - ord('A') for c in texto_limpio]


def numeros_a_texto(numeros):
    """
    Convierte lista de números a texto (0=A, 1=B, ..., 25=Z).
    
    Parámetros:
        numeros: lista de números [0-25]
    
    Retorna:
        Cadena de texto
    """
    return ''.join(chr(n + ord('A')) for n in numeros)


def cifrar_elgamal(mensaje_num, clave_publica):
    """
    Cifra un número usando ElGamal.
    
    Proceso:
    1. Extraer p, g, h de la clave pública
    2. Elegir k aleatorio (1 < k < p-1)
    3. Calcular c1 = g^k mod p
    4. Calcular s = h^k mod p (secreto compartido)
    5. Calcular c2 = (m * s) mod p
    
    Parámetros:
        mensaje_num: número del mensaje (debe ser < p)
        clave_publica: tupla (p, g, h)
    
    Retorna:
        Tupla (c1, c2, k, s) donde:
        - (c1, c2): mensaje cifrado
        - k: efímero usado (para mostrar en detalles)
        - s: secreto compartido (para mostrar en detalles)
    """
    p, g, h = clave_publica
    
    # Validar que el mensaje sea menor que p
    if mensaje_num >= p:
        raise ValueError(f"Mensaje ({mensaje_num}) debe ser menor que p ({p})")
    
    # 1. Elegir k aleatorio
    k = random.randrange(2, p - 1)
    
    # 2. Calcular c1 = g^k mod p
    c1 = pow(g, k, p)
    
    # 3. Calcular secreto compartido s = h^k mod p
    s = pow(h, k, p)
    
    # 4. Calcular c2 = (m * s) mod p
    c2 = (mensaje_num * s) % p
    
    return (c1, c2), k, s


def descifrar_elgamal(mensaje_cifrado, clave_publica, clave_privada):
    """
    Descifra un mensaje ElGamal.
    
    Proceso:
    1. Extraer c1, c2 del mensaje cifrado
    2. Calcular s = c1^x mod p (secreto compartido)
    3. Calcular inverso s^(-1) mod p
    4. Recuperar mensaje: m = (c2 * s^(-1)) mod p
    
    Parámetros:
        mensaje_cifrado: tupla (c1, c2)
        clave_publica: tupla (p, g, h)
        clave_privada: número x
    
    Retorna:
        Tupla (mensaje_descifrado, s, s_inv) donde:
        - mensaje_descifrado: número original
        - s: secreto compartido (para detalles)
        - s_inv: inverso de s (para detalles)
    """
    c1, c2 = mensaje_cifrado
    p, g, h = clave_publica
    x = clave_privada
    
    # 1. Calcular secreto compartido s = c1^x mod p
    s = pow(c1, x, p)
    
    # 2. Calcular inverso modular de s
    # s^(-1) = s^(p-2) mod p (usando el pequeño teorema de Fermat)
    s_inv = pow(s, p - 2, p)
    
    # 3. Recuperar mensaje m = (c2 * s^(-1)) mod p
    m = (c2 * s_inv) % p
    
    return m, s, s_inv


def cifrar_texto(texto, clave_publica):
    """
    Cifra un texto completo letra por letra.
    
    Convierte cada letra a número, cifra con ElGamal y guarda detalles.
    
    Parámetros:
        texto: mensaje en texto
        clave_publica: tupla (p, g, h)
    
    Retorna:
        Tupla (mensajes_cifrados, detalles)
    """
    numeros = texto_a_numeros(texto)
    mensajes_cifrados = []
    detalles = []
    
    for i, m in enumerate(numeros):
        cifrado, k, s = cifrar_elgamal(m, clave_publica)
        mensajes_cifrados.append(cifrado)
        
        p, g, h = clave_publica
        c1, c2 = cifrado
        
        detalles.append({
            'posicion': i,
            'letra': chr(m + ord('A')),
            'm': m,
            'k': k,
            'c1': c1,
            'c1_calculo': f"{g}^{k} mod {p}",
            's': s,
            's_calculo': f"{h}^{k} mod {p}",
            'c2': c2,
            'c2_calculo': f"({m} × {s}) mod {p}"
        })
    
    return mensajes_cifrados, detalles


def descifrar_texto(mensajes_cifrados, clave_publica, clave_privada):
    """
    Descifra una lista de mensajes cifrados.
    
    Parámetros:
        mensajes_cifrados: lista de tuplas (c1, c2)
        clave_publica: tupla (p, g, h)
        clave_privada: número x
    
    Retorna:
        Tupla (texto_descifrado, detalles)
    """
    numeros_descifrados = []
    detalles = []
    
    p, g, h = clave_publica
    
    for i, cifrado in enumerate(mensajes_cifrados):
        c1, c2 = cifrado
        m, s, s_inv = descifrar_elgamal(cifrado, clave_publica, clave_privada)
        numeros_descifrados.append(m)
        
        detalles.append({
            'posicion': i,
            'c1': c1,
            'c2': c2,
            's': s,
            's_calculo': f"{c1}^{clave_privada} mod {p}",
            's_inv': s_inv,
            's_inv_calculo': f"{s}^-1 mod {p}",
            'm': m,
            'm_calculo': f"({c2} × {s_inv}) mod {p}",
            'letra': chr(m + ord('A'))
        })
    
    texto_descifrado = numeros_a_texto(numeros_descifrados)
    return texto_descifrado, detalles


def mostrar_detalles_cifrado(detalles, clave_publica):
    """Muestra los detalles del proceso de cifrado."""
    p, g, h = clave_publica
    
    print("\n" + "="*100)
    print("DETALLES DEL PROCESO DE CIFRADO")
    print("="*100)
    print(f"Clave pública: p={p}, g={g}, h={h}")
    print("\n" + "-"*100)
    print(f"{'Pos':<4} {'Letra':<6} {'m':<6} {'k':<6} {'c1':<10} {'s':<10} {'c2':<10}")
    print("-"*100)
    
    for d in detalles:
        print(f"{d['posicion']:<4} {d['letra']:<6} {d['m']:<6} {d['k']:<6} "
              f"{d['c1']:<10} {d['s']:<10} {d['c2']:<10}")
    
    print("\n💡 Fórmulas usadas:")
    print(f"   c1 = g^k mod p = {g}^k mod {p}")
    print(f"   s = h^k mod p = {h}^k mod {p}")
    print(f"   c2 = (m × s) mod p")


def mostrar_detalles_descifrado(detalles, clave_privada):
    """Muestra los detalles del proceso de descifrado."""
    print("\n" + "="*100)
    print("DETALLES DEL PROCESO DE DESCIFRADO")
    print("="*100)
    print(f"Clave privada: x={clave_privada}")
    print("\n" + "-"*100)
    print(f"{'Pos':<4} {'c1':<10} {'c2':<10} {'s':<10} {'s⁻¹':<10} {'m':<6} {'Letra':<6}")
    print("-"*100)
    
    for d in detalles:
        print(f"{d['posicion']:<4} {d['c1']:<10} {d['c2']:<10} {d['s']:<10} "
              f"{d['s_inv']:<10} {d['m']:<6} {d['letra']:<6}")
    
    print("\n💡 Fórmulas usadas:")
    print(f"   s = c1^x mod p")
    print(f"   s⁻¹ = inverso modular de s")
    print(f"   m = (c2 × s⁻¹) mod p")


def menu_principal():
    """Menú interactivo principal del programa."""
    print("\n" + "="*100)
    print(" "*35 + "CIFRADO ELGAMAL")
    print("="*100)
    print("\nElGamal es un sistema de criptografía asimétrica (clave pública/privada)")
    print("basado en el problema del logaritmo discreto.")
    print("\nComponentes:")
    print("  • Clave pública:  (p, g, h) donde p=primo, g=generador, h=g^x mod p")
    print("  • Clave privada:  x (número secreto)")
    print("\nCifrado:  (c1, c2) = (g^k mod p, m·h^k mod p)")
    print("Descifrado: m = c2·(c1^x)^-1 mod p")
    print("="*100)
    
    clave_publica = None
    clave_privada = None
    
    while True:
        print("\n┌─── MENÚ PRINCIPAL ───┐")
        print("│ 1. Generar claves    │")
        print("│ 2. Cifrar mensaje    │")
        print("│ 3. Descifrar mensaje │")
        print("│ 4. Ver casos de uso  │")
        print("│ 5. Salir             │")
        print("└──────────────────────┘")
        
        opcion = input("\nSeleccione una opción [1-5]: ").strip()
        
        if opcion == '1':
            clave_publica, clave_privada = generar_claves(16)
            print(f"\n✅ Claves generadas exitosamente")
            print(f"   Clave pública:  p={clave_publica[0]}, g={clave_publica[1]}, h={clave_publica[2]}")
            print(f"   Clave privada:  x={clave_privada}")
        
        elif opcion == '2':
            if clave_publica is None:
                print("\n❌ Primero debe generar claves (opción 1)")
                continue
            cifrar_mensaje_menu(clave_publica)
        
        elif opcion == '3':
            if clave_publica is None or clave_privada is None:
                print("\n❌ Primero debe generar claves (opción 1)")
                continue
            descifrar_mensaje_menu(clave_publica, clave_privada)
        
        elif opcion == '4':
            mostrar_casos_uso()
        
        elif opcion == '5':
            print("\n¡Hasta pronto! 👋\n")
            break
        
        else:
            print("\n❌ Opción inválida. Intente nuevamente.")


def cifrar_mensaje_menu(clave_publica):
    """Interfaz para cifrar un mensaje."""
    print("\n" + "─"*100)
    print("CIFRADO DE MENSAJE")
    print("─"*100)
    
    mensaje = input("Ingrese el mensaje a cifrar: ").strip()
    
    if not mensaje:
        print("❌ El mensaje no puede estar vacío.")
        return
    
    try:
        p, g, h = clave_publica
        print(f"\n📝 Mensaje original: {mensaje}")
        print(f"🔑 Usando clave pública: p={p}, g={g}, h={h}")
        
        mensajes_cifrados, detalles = cifrar_texto(mensaje, clave_publica)
        
        mostrar_detalles_cifrado(detalles, clave_publica)
        
        print("\n" + "="*100)
        print("🔒 MENSAJE CIFRADO:")
        print("="*100)
        for i, (c1, c2) in enumerate(mensajes_cifrados):
            letra = detalles[i]['letra']
            print(f"   {letra}: (c1={c1}, c2={c2})")
        print("="*100)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def descifrar_mensaje_menu(clave_publica, clave_privada):
    """Interfaz para descifrar un mensaje."""
    print("\n" + "─"*100)
    print("DESCIFRADO DE MENSAJE")
    print("─"*100)
    print("\nNota: En este menú, primero cifra un mensaje y luego lo descifra automáticamente")
    print("      para demostrar el proceso completo.")
    
    mensaje = input("\nIngrese el mensaje a cifrar y descifrar: ").strip()
    
    if not mensaje:
        print("❌ El mensaje no puede estar vacío.")
        return
    
    try:
        # Cifrar primero
        print(f"\n📝 Mensaje original: {mensaje}")
        mensajes_cifrados, detalles_c = cifrar_texto(mensaje, clave_publica)
        
        print("\n🔒 Mensaje cifrado:")
        for i, (c1, c2) in enumerate(mensajes_cifrados):
            letra = detalles_c[i]['letra']
            print(f"   {letra}: (c1={c1}, c2={c2})")
        
        # Descifrar
        texto_descifrado, detalles_d = descifrar_texto(mensajes_cifrados, clave_publica, clave_privada)
        
        mostrar_detalles_descifrado(detalles_d, clave_privada)
        
        print("\n" + "="*100)
        print(f"🔓 MENSAJE DESCIFRADO: {texto_descifrado}")
        print("="*100)
        
        # Verificación
        original_limpio = ''.join(c.upper() for c in mensaje if c.isalpha())
        print(f"\n✅ Verificación: {original_limpio} == {texto_descifrado} → {original_limpio == texto_descifrado}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def mostrar_casos_uso():
    """Muestra casos de uso de ejemplo."""
    print("\n" + "="*100)
    print(" "*35 + "CASOS DE USO")
    print("="*100)
    
    print("\n📚 EJEMPLO COMPLETO: Cifrado y Descifrado de 'HELLO'")
    print("─"*100)
    
    # Generar claves pequeñas para el ejemplo
    p, g = 23, 5  # Primo pequeño y generador
    x = 6  # Clave privada
    h = pow(g, x, p)  # h = 5^6 mod 23 = 8
    
    clave_pub = (p, g, h)
    clave_priv = x
    
    print(f"Claves generadas:")
    print(f"  • Clave pública:  p={p}, g={g}, h={h}")
    print(f"  • Clave privada:  x={x}")
    
    mensaje = "HELLO"
    print(f"\nMensaje a cifrar: {mensaje}")
    
    # Cifrar
    cifrados, det_c = cifrar_texto(mensaje, clave_pub)
    print(f"\nCifrado:")
    for i, (c1, c2) in enumerate(cifrados):
        print(f"  {det_c[i]['letra']}: ({c1}, {c2})")
    
    # Descifrar
    descifrado, det_d = descifrar_texto(cifrados, clave_pub, clave_priv)
    print(f"\nDescifrado: {descifrado}")
    print(f"✓ Correcto: {mensaje == descifrado}")
    
    print("\n" + "="*100)
    print("\n💡 Propiedades de ElGamal:")
    print("   • Seguridad basada en el problema del logaritmo discreto")
    print("   • Cifrado probabilístico (mismo mensaje → diferentes cifrados)")
    print("   • Tamaño del cifrado: 2× el tamaño del mensaje")
    print("   • Usado en PGP y otras aplicaciones de seguridad")


if __name__ == "__main__":
    menu_principal()