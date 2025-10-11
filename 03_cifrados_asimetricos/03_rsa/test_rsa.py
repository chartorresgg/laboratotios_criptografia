#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Pruebas para RSA
Valida la implementación con múltiples casos de prueba
"""

# ============================================================================
# FUNCIONES MATEMÁTICAS BASE
# ============================================================================

def gcd(a: int, b: int) -> int:
    """Máximo Común Divisor - Algoritmo de Euclides"""
    while b != 0:
        a, b = b, a % b
    return abs(a)


def extended_gcd(a: int, b: int) -> tuple:
    """Euclides Extendido: retorna (gcd, x, y) tal que a*x + b*y = gcd"""
    if b == 0:
        return abs(a), 1 if a >= 0 else -1, 0
    
    gcd_val, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    return gcd_val, x, y


def modular_inverse(a: int, m: int) -> int:
    """Inverso modular: encuentra x tal que (a*x) % m = 1"""
    gcd_val, x, _ = extended_gcd(a, m)
    
    if gcd_val != 1:
        raise ValueError(f"No existe inverso: gcd({a}, {m}) = {gcd_val} ≠ 1")
    
    return x % m


def modular_exponentiation(base: int, exp: int, mod: int) -> int:
    """Exponenciación modular rápida: base^exp mod mod"""
    result = 1
    base = base % mod
    
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    
    return result


# ============================================================================
# FUNCIONES DE CONVERSIÓN
# ============================================================================

def text_to_numbers(text: str) -> str:
    """Convierte texto a números: A=00, B=01, ..., Z=25"""
    text = text.upper()
    numeric_str = ""
    
    for char in text:
        if 'A' <= char <= 'Z':
            value = ord(char) - ord('A')
            numeric_str += f"{value:02d}"
    
    return numeric_str


def numbers_to_text(numeric_str: str) -> str:
    """Convierte números de vuelta a texto"""
    text = ""
    
    for i in range(0, len(numeric_str), 2):
        if i + 1 < len(numeric_str):
            pair = numeric_str[i:i+2]
            value = int(pair)
            if 0 <= value <= 25:
                text += chr(ord('A') + value)
    
    return text


def split_into_blocks(numeric_str: str, modulus: int) -> list:
    """Divide en bloques < modulus (algoritmo greedy)"""
    blocks = []
    i = 0
    
    while i < len(numeric_str):
        current_block = ""
        letters_count = 0
        
        while i < len(numeric_str):
            if i + 1 < len(numeric_str):
                next_pair = numeric_str[i:i+2]
                test_block = current_block + next_pair
                test_value = int(test_block)
                
                if test_value < modulus:
                    current_block = test_block
                    letters_count += 1
                    i += 2
                else:
                    break
            else:
                break
        
        if current_block:
            blocks.append((int(current_block), letters_count))
    
    return blocks


# ============================================================================
# FUNCIONES DE CIFRADO/DESCIFRADO
# ============================================================================

def encrypt_message(plaintext: str, e: int, n: int) -> list:
    """Cifra un mensaje completo"""
    numeric_str = text_to_numbers(plaintext)
    blocks = split_into_blocks(numeric_str, n)
    
    encrypted_blocks = []
    for block_value, num_letters in blocks:
        cipher_value = modular_exponentiation(block_value, e, n)
        encrypted_blocks.append((cipher_value, num_letters))
    
    return encrypted_blocks


def decrypt_message(encrypted_blocks: list, d: int, n: int) -> str:
    """Descifra un mensaje completo"""
    numeric_str = ""
    
    for cipher_value, num_letters in encrypted_blocks:
        block_value = modular_exponentiation(cipher_value, d, n)
        expected_length = num_letters * 2
        block_str = str(block_value).zfill(expected_length)
        numeric_str += block_str
    
    return numbers_to_text(numeric_str)


# ============================================================================
# FUNCIÓN DE PRUEBA
# ============================================================================

def test_case(p, q, e, mensaje, descripcion):
    """Ejecuta un caso de prueba completo"""
    print(f"\n{'='*70}")
    print(f"CASO DE PRUEBA: {descripcion}")
    print(f"{'='*70}")
    
    # Calcular parámetros RSA
    n = p * q
    phi = (p - 1) * (q - 1)
    
    try:
        # Calcular clave privada d
        d = modular_inverse(e, phi)
    except ValueError as error:
        print(f"  ❌ ERROR: {error}")
        return False
    
    print(f"\nParámetros RSA:")
    print(f"  p = {p}, q = {q}")
    print(f"  n = p×q = {n}")
    print(f"  φ(n) = (p-1)(q-1) = {phi}")
    print(f"  e (público) = {e}")
    print(f"  d (privado) = {d}")
    
    # Verificar que (e*d) mod φ = 1
    verification = (e * d) % phi
    print(f"  Verificación: (e×d) mod φ(n) = {verification}", end="")
    if verification == 1:
        print(" ✓")
    else:
        print(f" ✗ (debería ser 1)")
        return False
    
    print(f"\nMensaje original: \"{mensaje}\"")
    
    # Convertir a números
    numeric = text_to_numbers(mensaje)
    print(f"Representación numérica: {numeric}")
    
    # Dividir en bloques
    blocks = split_into_blocks(numeric, n)
    print(f"Bloques planos: {[(m, l) for m, l in blocks]}")
    
    # Cifrar
    encrypted = encrypt_message(mensaje, e, n)
    cipher_list = [c for c, _ in encrypted]
    print(f"Bloques cifrados: {cipher_list}")
    
    # Descifrar
    decrypted = decrypt_message(encrypted, d, n)
    print(f"Mensaje descifrado: \"{decrypted}\"")
    
    # Verificar
    print(f"\nComparación:")
    print(f"  Original:    \"{mensaje}\"")
    print(f"  Descifrado:  \"{decrypted}\"")
    
    if mensaje == decrypted:
        print(f"  ✓✓✓ ÉXITO: Los mensajes coinciden ✓✓✓")
        return True
    else:
        print(f"  ✗✗✗ ERROR: Los mensajes NO coinciden ✗✗✗")
        return False


# ============================================================================
# EJECUCIÓN DE PRUEBAS
# ============================================================================

def main():
    """Ejecuta todos los casos de prueba"""
    print("="*70)
    print(" "*20 + "SUITE DE PRUEBAS RSA")
    print("="*70)
    
    # Definir casos de prueba
    # Formato: (p, q, e, mensaje, descripción)
    casos = [
        (61, 53, 17, "A", "Caso 1: Una sola letra"),
        (61, 53, 17, "HELLO", "Caso 2: Ejemplo clásico - HELLO"),
        (61, 53, 17, "ATTACK", "Caso 3: Ejemplo clásico - ATTACK"),
        (61, 53, 17, "THEQUICKBROWNFOX", "Caso 4: Mensaje largo"),
        (97, 89, 5, "CRYPTO", "Caso 5: Primos medianos"),
        (103, 107, 7, "SECRET", "Caso 6: Primos más grandes"),
        (61, 53, 17, "Z", "Caso 7: Última letra del alfabeto"),
        (61, 53, 17, "AAAAAA", "Caso 8: Letras repetidas"),
    ]
    
    resultados = []
    
    # Ejecutar cada caso
    for p, q, e, msg, desc in casos:
        try:
            resultado = test_case(p, q, e, msg, desc)
            resultados.append((desc, resultado))
        except Exception as error:
            print(f"\n  ❌ EXCEPCIÓN: {error}")
            resultados.append((desc, False))
    
    # Resumen final
    print(f"\n{'='*70}")
    print("RESUMEN FINAL")
    print(f"{'='*70}")
    print(f"\nTotal de pruebas ejecutadas: {len(resultados)}")
    print(f"Exitosas: {sum(1 for _, r in resultados if r)}")
    print(f"Fallidas:  {sum(1 for _, r in resultados if not r)}")
    
    print(f"\nDetalle:")
    for desc, resultado in resultados:
        status = "✓" if resultado else "✗"
        print(f"  {status} {desc}")
    
    print(f"\n{'='*70}")
    if all(r for _, r in resultados):
        print("✓✓✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE ✓✓✓")
    else:
        print("✗✗✗ ALGUNAS PRUEBAS FALLARON ✗✗✗")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()