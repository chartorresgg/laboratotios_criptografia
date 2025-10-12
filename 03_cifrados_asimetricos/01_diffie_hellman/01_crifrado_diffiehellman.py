#!/usr/bin/env python3
"""
DIFFIE-HELLMAN - Intercambio de Claves
=======================================
Implementación del protocolo de intercambio de claves Diffie-Hellman.
Permite a dos partes establecer una clave compartida sobre un canal inseguro.
"""

import random
from math import gcd


def es_primo(n, k=5):
    """
    Test de primalidad de Miller-Rabin.
    
    Determina si un número es probablemente primo.
    
    Parámetros:
        n: número a probar
        k: número de iteraciones (más iteraciones = más precisión)
    
    Retorna:
        True si n es probablemente primo, False si definitivamente es compuesto
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Escribir n-1 como 2^r × d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Test de Miller-Rabin k veces
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
    Genera un número primo aleatorio de un tamaño específico.
    
    Para propósitos educativos, usamos números más pequeños (16 bits).
    En producción se usarían 2048+ bits.
    
    Parámetros:
        bits: tamaño en bits del primo (default: 16)
    
    Retorna:
        Un número primo
    """
    while True:
        # Generar número impar aleatorio
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1  # Asegurar que sea de 'bits' bits e impar
        
        if es_primo(n):
            return n


def encontrar_generador(p):
    """
    Encuentra un generador (raíz primitiva) módulo p.
    
    Un generador g cumple que {g^1, g^2, ..., g^(p-1)} genera
    todos los números de 1 a p-1 módulo p.
    
    Para propósitos educativos, encontramos un generador pequeño.
    
    Parámetros:
        p: número primo
    
    Retorna:
        Un generador módulo p
    """
    # Para simplificar, probamos valores pequeños
    for g in range(2, min(p, 100)):
        # Verificar si g es generador
        # Un número g es generador si el orden de g es p-1
        # Simplificación: verificamos que g^2 y g^((p-1)/2) no sean 1
        if pow(g, 2, p) != 1 and pow(g, (p-1)//2, p) != 1:
            return g
    
    # Si no encontramos generador pequeño, usar uno aleatorio
    return random.randint(2, p - 2)


def exponenciacion_rapida(base, exponente, modulo):
    """
    Calcula (base^exponente) mod modulo eficientemente.
    
    Usa el algoritmo de exponenciación modular rápida (square-and-multiply).
    
    Proceso:
    1. Representar exponente en binario
    2. Para cada bit:
       - Elevar al cuadrado el resultado actual
       - Si el bit es 1, multiplicar por la base
    3. Aplicar módulo en cada paso
    
    Ejemplo:
        7^5 mod 13:
        5 en binario = 101
        7^1 = 7
        7^2 = 49 ≡ 10 (mod 13)
        7^4 = 10^2 = 100 ≡ 9 (mod 13)
        7^5 = 7^4 × 7^1 = 9 × 7 = 63 ≡ 11 (mod 13)
    
    Parámetros:
        base: base de la exponenciación
        exponente: exponente
        modulo: módulo
    
    Retorna:
        (base^exponente) mod modulo
    """
    resultado = 1
    base = base % modulo
    
    while exponente > 0:
        # Si el exponente es impar, multiplicar por base
        if exponente % 2 == 1:
            resultado = (resultado * base) % modulo
        
        # Elevar base al cuadrado
        exponente = exponente >> 1  # Dividir entre 2
        base = (base * base) % modulo
    
    return resultado


def generar_parametros_publicos(bits=16):
    """
    Genera los parámetros públicos del protocolo Diffie-Hellman.
    
    Parámetros públicos:
    - p: número primo grande
    - g: generador módulo p
    
    Estos parámetros pueden ser compartidos públicamente y usados
    por cualquier par de usuarios.
    
    Parámetros:
        bits: tamaño del primo en bits
    
    Retorna:
        Tupla (p, g)
    """
    p = generar_primo(bits)
    g = encontrar_generador(p)
    return p, g


def generar_clave_privada(p):
    """
    Genera una clave privada aleatoria.
    
    La clave privada debe estar en el rango [2, p-2].
    
    Parámetros:
        p: número primo (parámetro público)
    
    Retorna:
        Clave privada (número aleatorio)
    """
    return random.randint(2, p - 2)


def calcular_clave_publica(g, clave_privada, p):
    """
    Calcula la clave pública a partir de la clave privada.
    
    Fórmula: clave_publica = g^clave_privada mod p
    
    Parámetros:
        g: generador (parámetro público)
        clave_privada: clave privada del usuario
        p: primo (parámetro público)
    
    Retorna:
        Clave pública
    """
    return exponenciacion_rapida(g, clave_privada, p)


def calcular_secreto_compartido(clave_publica_otro, clave_privada_propia, p):
    """
    Calcula el secreto compartido.
    
    Fórmula: secreto = (clave_publica_otro)^clave_privada_propia mod p
    
    Este secreto es el mismo para ambas partes:
    - Alice: secreto = B^a mod p = (g^b)^a mod p = g^(ab) mod p
    - Bob:   secreto = A^b mod p = (g^a)^b mod p = g^(ab) mod p
    
    Parámetros:
        clave_publica_otro: clave pública de la otra parte
        clave_privada_propia: clave privada propia
        p: primo (parámetro público)
    
    Retorna:
        Secreto compartido
    """
    return exponenciacion_rapida(clave_publica_otro, clave_privada_propia, p)


def mostrar_paso_a_paso(p, g, a, A, b, B, secreto_alice, secreto_bob):
    """Muestra el proceso completo paso a paso."""
    print("\n" + "="*80)
    print("PROTOCOLO DIFFIE-HELLMAN - PASO A PASO")
    print("="*80)
    
    print("\n1. PARÁMETROS PÚBLICOS (conocidos por todos)")
    print("-"*80)
    print(f"   p (primo) = {p}")
    print(f"   g (generador) = {g}")
    
    print("\n2. ALICE genera su par de claves")
    print("-"*80)
    print(f"   Clave privada de Alice (a):  {a}  [SECRETA]")
    print(f"   Cálculo: A = g^a mod p = {g}^{a} mod {p}")
    print(f"   Clave pública de Alice (A):  {A}  [PÚBLICA]")
    
    print("\n3. BOB genera su par de claves")
    print("-"*80)
    print(f"   Clave privada de Bob (b):  {b}  [SECRETA]")
    print(f"   Cálculo: B = g^b mod p = {g}^{b} mod {p}")
    print(f"   Clave pública de Bob (B):  {B}  [PÚBLICA]")
    
    print("\n4. INTERCAMBIO PÚBLICO")
    print("-"*80)
    print(f"   Alice envía a Bob:  A = {A}")
    print(f"   Bob envía a Alice:  B = {B}")
    print("   ⚠️ Un atacante puede ver A y B, pero NO puede calcular el secreto")
    
    print("\n5. ALICE calcula el secreto compartido")
    print("-"*80)
    print(f"   Alice calcula: s = B^a mod p = {B}^{a} mod {p} = {secreto_alice}")
    
    print("\n6. BOB calcula el secreto compartido")
    print("-"*80)
    print(f"   Bob calcula: s = A^b mod p = {A}^{b} mod {p} = {secreto_bob}")
    
    print("\n7. VERIFICACIÓN")
    print("-"*80)
    if secreto_alice == secreto_bob:
        print(f"   ✅ ¡ÉXITO! Ambos tienen el mismo secreto: {secreto_alice}")
        print(f"   Ambos calcularon: g^(ab) mod p = {g}^({a}×{b}) mod {p} = {secreto_alice}")
    else:
        print(f"   ❌ ERROR: Los secretos no coinciden")
    
    print("\n" + "="*80)


def menu_principal():
    """Menú interactivo principal."""
    print("\n" + "="*80)
    print(" "*20 + "DIFFIE-HELLMAN")
    print(" "*15 + "Intercambio de Claves")
    print("="*80)
    print("\nProtocolo que permite a dos partes establecer un secreto compartido")
    print("sobre un canal público inseguro (sin encriptar el canal).")
    print("\nInventado por Whitfield Diffie y Martin Hellman en 1976.")
    print("="*80)
    
    while True:
        print("\n┌─── MENÚ PRINCIPAL ────────────────┐")
        print("│ 1. Ejecutar protocolo completo    │")
        print("│ 2. Modo interactivo (paso a paso) │")
        print("│ 3. Ver casos de uso               │")
        print("│ 4. Salir                          │")
        print("└───────────────────────────────────┘")
        
        opcion = input("\nSeleccione una opción [1-4]: ").strip()
        
        if opcion == '1':
            ejecutar_protocolo_completo()
        elif opcion == '2':
            modo_interactivo()
        elif opcion == '3':
            mostrar_casos_uso()
        elif opcion == '4':
            print("\n¡Hasta pronto! 👋\n")
            break
        else:
            print("\n❌ Opción inválida.")


def ejecutar_protocolo_completo():
    """Ejecuta el protocolo Diffie-Hellman completo."""
    print("\n" + "─"*80)
    print("EJECUCIÓN DEL PROTOCOLO DIFFIE-HELLMAN")
    print("─"*80)
    
    try:
        # Opción de tamaño
        print("\nTamaño de primo:")
        print("1. Pequeño (16 bits) - Rápido, educativo")
        print("2. Mediano (32 bits) - Más seguro")
        
        opcion = input("Seleccione [1-2, Enter=1]: ").strip()
        bits = 32 if opcion == '2' else 16
        
        print(f"\n⏳ Generando parámetros públicos ({bits} bits)...")
        p, g = generar_parametros_publicos(bits)
        
        print(f"✓ Parámetros generados:")
        print(f"  p = {p}")
        print(f"  g = {g}")
        
        # Alice genera su par de claves
        print("\n⏳ Alice genera su par de claves...")
        a = generar_clave_privada(p)
        A = calcular_clave_publica(g, a, p)
        print(f"✓ Alice lista (clave pública: {A})")
        
        # Bob genera su par de claves
        print("\n⏳ Bob genera su par de claves...")
        b = generar_clave_privada(p)
        B = calcular_clave_publica(g, b, p)
        print(f"✓ Bob listo (clave pública: {B})")
        
        # Calcular secretos compartidos
        print("\n⏳ Calculando secretos compartidos...")
        secreto_alice = calcular_secreto_compartido(B, a, p)
        secreto_bob = calcular_secreto_compartido(A, b, p)
        
        # Mostrar detalles
        mostrar_paso_a_paso(p, g, a, A, b, B, secreto_alice, secreto_bob)
        
        # Explicación de seguridad
        print("\n💡 SEGURIDAD:")
        print("   Un atacante que intercepta el canal ve:")
        print(f"   - p = {p}")
        print(f"   - g = {g}")
        print(f"   - A = {A} (clave pública de Alice)")
        print(f"   - B = {B} (clave pública de Bob)")
        print(f"\n   Pero NO puede calcular:")
        print(f"   - a = {a} (clave privada de Alice)")
        print(f"   - b = {b} (clave privada de Bob)")
        print(f"   - secreto = {secreto_alice}")
        print(f"\n   Esto es el Problema del Logaritmo Discreto (computacionalmente difícil)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def modo_interactivo():
    """Modo interactivo donde el usuario ingresa los valores."""
    print("\n" + "─"*80)
    print("MODO INTERACTIVO")
    print("─"*80)
    
    try:
        print("\nIngrese los parámetros públicos:")
        p = int(input("p (número primo): ").strip())
        g = int(input("g (generador): ").strip())
        
        print("\nIngrese las claves privadas:")
        a = int(input("Clave privada de Alice (a): ").strip())
        b = int(input("Clave privada de Bob (b): ").strip())
        
        # Calcular claves públicas
        print("\n⏳ Calculando claves públicas...")
        A = calcular_clave_publica(g, a, p)
        B = calcular_clave_publica(g, b, p)
        
        # Calcular secretos
        print("⏳ Calculando secretos compartidos...")
        secreto_alice = calcular_secreto_compartido(B, a, p)
        secreto_bob = calcular_secreto_compartido(A, b, p)
        
        # Mostrar resultados
        mostrar_paso_a_paso(p, g, a, A, b, B, secreto_alice, secreto_bob)
        
    except ValueError:
        print("\n❌ Error: Ingrese números válidos")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def mostrar_casos_uso():
    """Muestra casos de uso de ejemplo."""
    print("\n" + "="*80)
    print(" "*28 + "CASOS DE USO")
    print("="*80)
    
    casos = [
        {
            'nombre': 'Caso 1: Ejemplo simple (valores pequeños)',
            'p': 23,
            'g': 5,
            'a': 6,
            'b': 15
        },
        {
            'nombre': 'Caso 2: Otro ejemplo educativo',
            'p': 47,
            'g': 7,
            'a': 12,
            'b': 25
        }
    ]
    
    for i, caso in enumerate(casos, 1):
        print(f"\n{'─'*80}")
        print(f"{caso['nombre']}")
        print(f"{'─'*80}")
        print(f"Parámetros públicos: p={caso['p']}, g={caso['g']}")
        print(f"Claves privadas: a={caso['a']}, b={caso['b']}")
        
        try:
            A = calcular_clave_publica(caso['g'], caso['a'], caso['p'])
            B = calcular_clave_publica(caso['g'], caso['b'], caso['p'])
            
            secreto_alice = calcular_secreto_compartido(B, caso['a'], caso['p'])
            secreto_bob = calcular_secreto_compartido(A, caso['b'], caso['p'])
            
            print(f"\nClaves públicas: A={A}, B={B}")
            print(f"Secreto compartido: {secreto_alice}")
            
            if secreto_alice == secreto_bob:
                print("✓ Los secretos coinciden")
            
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "="*80)
    print("\n💡 Prueba estos casos en el modo interactivo (opción 2)")


if __name__ == "__main__":
    menu_principal()