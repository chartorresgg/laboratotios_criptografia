#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema RSA Educativo para Mensajes de Texto
Alfabeto: A-Z (26 letras) mapeado como A=00, B=01, ..., Z=25
Implementación completa con validaciones matemáticas y trazabilidad
"""

import random
from math import gcd


# ============================================================================
# FUNCIONES DE MAPEO DE TEXTO
# ============================================================================

def map_text_to_numbers(text):
    """
    Convierte texto a representación numérica.
    A=00, B=01, C=02, ..., Z=25
    
    Args:
        text: String con letras A-Z (mayúsculas)
    
    Returns:
        String numérico con pares de dígitos concatenados
    """
    numeric_str = ""
    for char in text:
        if not char.isalpha():
            continue
        char = char.upper()
        if 'A' <= char <= 'Z':
            numeric_value = ord(char) - ord('A')
            numeric_str += f"{numeric_value:02d}"
    return numeric_str


def map_numbers_to_text(numeric_str):
    """
    Convierte representación numérica de vuelta a texto.
    
    Args:
        numeric_str: String numérico con pares de dígitos
    
    Returns:
        String de texto con letras A-Z
    """
    text = ""
    for i in range(0, len(numeric_str), 2):
        if i + 1 < len(numeric_str):
            pair = numeric_str[i:i+2]
            numeric_value = int(pair)
            if 0 <= numeric_value <= 25:
                text += chr(ord('A') + numeric_value)
    return text


def clean_text(text):
    """
    Limpia el texto dejando solo letras A-Z en mayúsculas.
    
    Args:
        text: String de entrada
    
    Returns:
        Tupla (texto_limpio, fue_modificado)
    """
    original = text
    cleaned = ''.join(c.upper() for c in text if c.isalpha())
    return cleaned, (original != cleaned)


# ============================================================================
# FUNCIONES DE CONSTRUCCIÓN DE BLOQUES
# ============================================================================

def split_into_blocks(numeric_str, modulus):
    """
    Divide la representación numérica en bloques que sean < modulus.
    Usa algoritmo greedy: maximiza el tamaño de cada bloque.
    
    Args:
        numeric_str: String numérico (ej: "000102")
        modulus: Módulo m de RSA
    
    Returns:
        Lista de tuplas (bloque_entero, num_letras)
    """
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
# EXPONENCIACIÓN MODULAR CON TRAZABILIDAD
# ============================================================================

def modular_exponentiation_traced(base, exp, mod, verbose=False):
    """
    Exponenciación modular rápida (square-and-multiply) con trazabilidad.
    Calcula base^exp mod mod de manera eficiente.
    
    Args:
        base: Base
        exp: Exponente
        mod: Módulo
        verbose: Si True, imprime cada paso del algoritmo
    
    Returns:
        Resultado de base^exp mod mod
    """
    if verbose:
        print(f"\n{'='*70}")
        print(f"  Exponenciación Modular: {base}^{exp} mod {mod}")
        print(f"{'='*70}")
        
        # Convertir exponente a binario
        exp_binary = bin(exp)[2:]  # Quitar el '0b'
        print(f"\nPaso 1: Convertir exponente a binario")
        print(f"  {exp} (decimal) = {exp_binary} (binario)")
        print(f"  Longitud: {len(exp_binary)} bits")
        
        print(f"\nPaso 2: Algoritmo Square-and-Multiply")
        print(f"  Leer bits de izquierda a derecha:")
        print(f"  Bit 1 → result = base")
        print(f"  Bit 0 → result = result²")
        print(f"  Bit 1 → result = result² × base")
        print()
    
    result = 1
    base = base % mod
    step = 0
    
    if verbose:
        exp_binary = bin(exp)[2:]
        print(f"{'Paso':<6} {'Bit':<6} {'Operación':<30} {'Resultado':<15} {'mod {mod}'}")
        print('-' * 70)
    
    while exp > 0:
        if verbose:
            current_bit = exp & 1
            step += 1
        
        if exp & 1:  # Si el bit es 1
            if verbose:
                old_result = result
                result = (result * base) % mod
                print(f"{step:<6} {current_bit:<6} result = {old_result} × {base} mod {mod} = {result:<15}")
            else:
                result = (result * base) % mod
        else:
            if verbose:
                print(f"{step:<6} {current_bit:<6} (bit 0, solo elevar al cuadrado)")
        
        exp >>= 1  # Dividir exponente entre 2
        if exp > 0:  # No elevar al cuadrado en la última iteración
            if verbose:
                old_base = base
            base = (base * base) % mod
            if verbose and exp > 0:
                print(f"{'':>6} {'':>6} base = {old_base}² mod {mod} = {base:<15}")
    
    if verbose:
        print('-' * 70)
        print(f"✓ Resultado final: {result}\n")
    
    return result


# ============================================================================
# FUNCIONES CRIPTOGRÁFICAS
# ============================================================================

def encrypt_blocks(blocks, e, m, verbose=False):
    """
    Encripta cada bloque usando C = M^e mod m
    
    Args:
        blocks: Lista de tuplas (M, num_letras)
        e: Exponente público
        m: Módulo público
        verbose: Si True, muestra exponenciación detallada
    
    Returns:
        Lista de tuplas (C, num_letras)
    """
    encrypted = []
    for i, (M, num_letters) in enumerate(blocks, 1):
        if verbose:
            print(f"\n{'='*70}")
            print(f"  ENCRIPTANDO BLOQUE {i}")
            print(f"{'='*70}")
        C = modular_exponentiation_traced(M, e, m, verbose=verbose)
        encrypted.append((C, num_letters))
    return encrypted


def extended_gcd(a, b):
    """
    Algoritmo Extendido de Euclides.
    Encuentra d y y tales que: a*d + b*y = gcd(a,b)
    
    Args:
        a, b: Enteros
    
    Returns:
        Tupla (gcd, d, y)
    """
    if b == 0:
        return a, 1, 0
    
    gcd_val, x1, y1 = extended_gcd(b, a % b)
    d = y1
    y = x1 - (a // b) * y1
    
    return gcd_val, d, y


def modinv(e, phi):
    """
    Calcula la inversa modular de e módulo phi usando Euclides Extendido.
    Encuentra d tal que (e * d) % phi = 1
    
    Args:
        e: Exponente público
        phi: φ(n) = (p-1)(q-1)
    
    Returns:
        d: Exponente privado
    
    Raises:
        ValueError: Si no existe inversa modular
    """
    gcd_val, d, _ = extended_gcd(e, phi)
    
    if gcd_val != 1:
        raise ValueError(f"No existe inversa modular: gcd({e}, {phi}) = {gcd_val} ≠ 1")
    
    d = d % phi
    return d


def decrypt_blocks(encrypted_blocks, d, m, verbose=False):
    """
    Desencripta cada bloque usando M = C^d mod m
    
    Args:
        encrypted_blocks: Lista de tuplas (C, num_letras)
        d: Exponente privado
        m: Módulo público
        verbose: Si True, muestra exponenciación detallada
    
    Returns:
        Lista de tuplas (M, num_letras)
    """
    decrypted = []
    for i, (C, num_letters) in enumerate(encrypted_blocks, 1):
        if verbose:
            print(f"\n{'='*70}")
            print(f"  DESENCRIPTANDO BLOQUE {i}")
            print(f"{'='*70}")
        M = modular_exponentiation_traced(C, d, m, verbose=verbose)
        decrypted.append((M, num_letters))
    return decrypted


def reconstruct_numeric_string(decrypted_blocks, verbose=False):
    """
    Reconstruye la cadena numérica desde los bloques desencriptados.
    Preserva el padding de ceros a la izquierda.
    
    Args:
        decrypted_blocks: Lista de tuplas (M, num_letras)
        verbose: Si True, muestra detalles de reconstrucción
    
    Returns:
        String numérico completo
    """
    numeric_str = ""
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"  RECONSTRUCCIÓN DE CADENA NUMÉRICA")
        print(f"{'='*70}\n")
    
    for i, (M, num_letters) in enumerate(decrypted_blocks, 1):
        expected_length = num_letters * 2
        block_str = str(M).zfill(expected_length)
        
        if verbose:
            print(f"Bloque {i}:")
            print(f"  Valor desencriptado: {M}")
            print(f"  Número de letras: {num_letters}")
            print(f"  Longitud esperada: {num_letters} × 2 = {expected_length} dígitos")
            print(f"  Sin padding: '{M}'")
            print(f"  Con padding: '{block_str}'")
            
            # Mostrar desglose letra por letra
            print(f"  Desglose:")
            for j in range(0, len(block_str), 2):
                pair = block_str[j:j+2]
                value = int(pair)
                letter = chr(ord('A') + value)
                print(f"    '{pair}' → {value:2d} → {letter}")
            print()
        
        numeric_str += block_str
    
    if verbose:
        print(f"✓ Cadena numérica completa: {numeric_str}")
        print(f"{'='*70}\n")
    
    return numeric_str


# ============================================================================
# FUNCIONES DE VALIDACIÓN
# ============================================================================

def is_probable_prime(n, k=10):
    """
    Test de primalidad probabilístico de Miller-Rabin.
    
    Args:
        n: Número a probar
        k: Número de rondas (mayor k = mayor certeza)
    
    Returns:
        True si n es probablemente primo, False si es compuesto
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
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


def validate_keys(p, q, m, e, verbose=True):
    """
    Valida que las claves sean matemáticamente correctas.
    
    Args:
        p, q: Primos candidatos
        m: Módulo público
        e: Exponente público
        verbose: Si True, imprime detalles
    
    Returns:
        Tupla (es_valido, phi, mensaje_error)
    """
    if not is_probable_prime(p):
        return False, None, f"Error: p={p} no parece ser primo (test Miller-Rabin)"
    if not is_probable_prime(q):
        return False, None, f"Error: q={q} no parece ser primo (test Miller-Rabin)"
    
    if verbose:
        print(f"✓ p={p} es probablemente primo")
        print(f"✓ q={q} es probablemente primo")
    
    if p * q != m:
        return False, None, f"Error: p*q = {p*q} ≠ m = {m}"
    
    if verbose:
        print(f"✓ p*q = {p}*{q} = {m} ✓")
    
    phi = (p - 1) * (q - 1)
    if verbose:
        print(f"✓ φ(n) = (p-1)(q-1) = {p-1}*{q-1} = {phi}")
    
    gcd_val = gcd(e, phi)
    if gcd_val != 1:
        return False, phi, f"Error: gcd(e, φ) = gcd({e}, {phi}) = {gcd_val} ≠ 1"
    
    if verbose:
        print(f"✓ gcd(e, φ) = gcd({e}, {phi}) = 1 ✓")
    
    return True, phi, "Claves válidas"


# ============================================================================
# INTERFAZ Y FLUJO PRINCIPAL
# ============================================================================

def print_separator(char='=', length=70):
    """Imprime una línea separadora."""
    print(char * length)


def print_section(title):
    """Imprime un título de sección."""
    print_separator()
    print(f"  {title}")
    print_separator()


def demo_rsa():
    """
    Demostración automática con el ejemplo clásico:
    p=61, q=53, m=3233, e=17, mensaje="HELLO"
    """
    print_section("DEMOSTRACIÓN AUTOMÁTICA RSA")
    print("Usando el ejemplo clásico educativo:")
    print("  p = 61, q = 53")
    print("  m = p*q = 3233")
    print("  e = 17")
    print("  Mensaje: HELLO")
    print()
    
    p, q = 61, 53
    m = p * q
    e = 17
    original_message = "HELLO"
    
    print_section("PASO 1: MAPEO DE TEXTO A NÚMEROS")
    print(f"Mensaje original: {original_message}")
    numeric_repr = map_text_to_numbers(original_message)
    print(f"Representación numérica: {numeric_repr}")
    print("Mapeo: H=07, E=04, L=11, L=11, O=14")
    print()
    
    print_section("PASO 2: DIVISIÓN EN BLOQUES")
    print(f"Módulo m = {m}")
    blocks = split_into_blocks(numeric_repr, m)
    print(f"Bloques generados (greedy, cada bloque < {m}):")
    for i, (block_val, num_letters) in enumerate(blocks, 1):
        print(f"  Bloque {i}: M = {block_val:4d} ({num_letters} letra(s)) < {m}")
    print()
    
    print_section("PASO 3: ENCRIPTACIÓN")
    print(f"Fórmula: C = M^e mod m = M^{e} mod {m}")
    encrypted = encrypt_blocks(blocks, e, m, verbose=False)
    print("Bloques cifrados:")
    for i, ((M, _), (C, num_letters)) in enumerate(zip(blocks, encrypted), 1):
        print(f"  Bloque {i}: C = {M}^{e} mod {m} = {C}")
    print()
    print(f"Mensaje cifrado (lista de enteros): {[C for C, _ in encrypted]}")
    print()
    
    print_section("PASO 4: VALIDACIÓN DE CLAVES PRIVADAS")
    is_valid, phi, msg = validate_keys(p, q, m, e, verbose=True)
    if not is_valid:
        print(f"ERROR: {msg}")
        return
    print()
    
    print_section("PASO 5: CÁLCULO DEL EXPONENTE PRIVADO d")
    print(f"Necesitamos encontrar d tal que: (e * d) mod φ = 1")
    print(f"Es decir: ({e} * d) mod {phi} = 1")
    print(f"\nUsando Algoritmo Extendido de Euclides:")
    d = modinv(e, phi)
    print(f"  d = {d}")
    print(f"\nVerificación: ({e} * {d}) mod {phi} = {(e * d) % phi}")
    assert (e * d) % phi == 1
    print("✓ Verificación exitosa: (e * d) mod φ = 1 ✓")
    print()
    
    print_section("PASO 6: DESENCRIPTACIÓN")
    print(f"Fórmula: M = C^d mod m = C^{d} mod {m}")
    decrypted = decrypt_blocks(encrypted, d, m, verbose=False)
    print("Bloques desencriptados:")
    for i, ((C, _), (M, num_letters)) in enumerate(zip(encrypted, decrypted), 1):
        print(f"  Bloque {i}: M = {C}^{d} mod {m} = {M}")
    print()
    
    print_section("PASO 7: RECONSTRUCCIÓN DEL MENSAJE")
    reconstructed_numeric = reconstruct_numeric_string(decrypted, verbose=False)
    print(f"Cadena numérica reconstruida: {reconstructed_numeric}")
    print(f"Cadena numérica original:     {numeric_repr}")
    assert reconstructed_numeric == numeric_repr
    print("✓ Las cadenas numéricas coinciden ✓")
    print()
    
    decrypted_message = map_numbers_to_text(reconstructed_numeric)
    print(f"Mensaje desencriptado: {decrypted_message}")
    print(f"Mensaje original:      {original_message}")
    assert decrypted_message == original_message
    print("✓ Los mensajes coinciden perfectamente ✓")
    print()
    
    print_section("RESUMEN FINAL")
    print(f"Claves públicas:  m = {m}, e = {e}")
    print(f"Claves privadas:  p = {p}, q = {q}, d = {d}")
    print(f"φ(n) = {phi}")
    print(f"Mensaje original: {original_message}")
    print(f"Mensaje cifrado:  {[C for C, _ in encrypted]}")
    print(f"Mensaje recuperado: {decrypted_message}")
    print(f"\n✓✓✓ DEMOSTRACIÓN EXITOSA ✓✓✓")
    print_separator()


def interactive_mode():
    """Modo interactivo con menú."""
    print_section("SISTEMA RSA INTERACTIVO")
    
    m, e = None, None
    original_message = None
    numeric_repr = None
    blocks = None
    encrypted = None
    p, q, d, phi = None, None, None, None
    show_details = False
    
    while True:
        print("\n" + "="*70)
        print("MENÚ PRINCIPAL")
        print("="*70)
        print("1. Ingresar claves públicas (m, e)")
        print("2. Ingresar mensaje a encriptar")
        print("3. Realizar encriptación")
        print("4. Ingresar claves privadas (p, q) y desencriptar")
        print("5. Mostrar información completa del sistema")
        print("6. Ejecutar demostración automática (p=61, q=53, e=17, 'HELLO')")
        print(f"7. Activar/Desactivar modo detallado (actual: {'ON' if show_details else 'OFF'})")
        print("8. Salir")
        print("="*70)
        
        choice = input("\nSeleccione una opción: ").strip()
        
        if choice == '1':
            print_section("INGRESO DE CLAVES PÚBLICAS")
            try:
                m = int(input("Ingrese el módulo m (entero positivo): "))
                e = int(input("Ingrese el exponente público e (entero > 1): "))
                
                if m <= 0 or e <= 1:
                    print("❌ Error: m debe ser positivo y e debe ser > 1")
                    m, e = None, None
                else:
                    print(f"✓ Claves públicas guardadas: m={m}, e={e}")
            except ValueError:
                print("❌ Error: Ingrese valores numéricos válidos")
                m, e = None, None
        
        elif choice == '2':
            print_section("INGRESO DE MENSAJE")
            text = input("Ingrese el mensaje (solo letras A-Z): ").strip()
            
            cleaned, modified = clean_text(text)
            
            if not cleaned:
                print("❌ Error: El mensaje debe contener al menos una letra")
                continue
            
            if modified:
                print(f"\nTexto limpio (solo A-Z): {cleaned}")
                confirm = input("¿Desea usar este texto? (s/n): ").strip().lower()
                if confirm != 's':
                    print("Operación cancelada")
                    continue
            
            original_message = cleaned
            numeric_repr = map_text_to_numbers(original_message)
            print(f"\n✓ Mensaje guardado: {original_message}")
            print(f"  Representación numérica: {numeric_repr}")
            
            blocks = None
            encrypted = None
        
        elif choice == '3':
            if m is None or e is None:
                print("❌ Error: Primero ingrese las claves públicas (opción 1)")
                continue
            if original_message is None:
                print("❌ Error: Primero ingrese un mensaje (opción 2)")
                continue
            
            print_section("ENCRIPTACIÓN")
            print(f"Mensaje: {original_message}")
            print(f"Representación numérica: {numeric_repr}")
            print(f"Claves: m={m}, e={e}")
            print()
            
            blocks = split_into_blocks(numeric_repr, m)
            print("Bloques generados:")
            for i, (block_val, num_letters) in enumerate(blocks, 1):
                print(f"  Bloque {i}: M={block_val:4d} ({num_letters} letra(s))")
            print()
            
            encrypted = encrypt_blocks(blocks, e, m, verbose=show_details)
            
            if not show_details:
                print("Bloques cifrados:")
                for i, ((M, _), (C, _)) in enumerate(zip(blocks, encrypted), 1):
                    print(f"  Bloque {i}: {M}^{e} mod {m} = {C}")
                print()
            
            cipher_list = [C for C, _ in encrypted]
            print(f"✓ Mensaje cifrado: {cipher_list}")
        
        elif choice == '4':
            if encrypted is None:
                print("❌ Error: Primero realice la encriptación (opción 3)")
                continue
            
            print_section("DESENCRIPTACIÓN")
            
            try:
                p = int(input("Ingrese el primo p: "))
                q = int(input("Ingrese el primo q: "))
            except ValueError:
                print("❌ Error: Ingrese valores numéricos válidos")
                continue
            
            print()
            print("Validando claves privadas...")
            is_valid, phi, msg = validate_keys(p, q, m, e, verbose=True)
            
            if not is_valid:
                print(f"\n❌ {msg}")
                p, q, d, phi = None, None, None, None
                continue
            
            print()
            print("Calculando exponente privado d...")
            try:
                d = modinv(e, phi)
                print(f"  d = {d}")
                print(f"Verificación: ({e} * {d}) mod {phi} = {(e*d)%phi}")
                assert (e * d) % phi == 1
                print("✓ Verificación exitosa")
            except ValueError as ve:
                print(f"❌ Error: {ve}")
                continue
            
            print()
            print("Desencriptando bloques...")
            decrypted = decrypt_blocks(encrypted, d, m, verbose=show_details)
            
            if not show_details:
                for i, ((C, _), (M, _)) in enumerate(zip(encrypted, decrypted), 1):
                    print(f"  Bloque {i}: {C}^{d} mod {m} = {M}")
            
            reconstructed_numeric = reconstruct_numeric_string(decrypted, verbose=show_details)
            
            if not show_details:
                print(f"\nCadena numérica reconstruida: {reconstructed_numeric}")
            
            decrypted_message = map_numbers_to_text(reconstructed_numeric)
            
            print(f"\n✓ Mensaje desencriptado: {decrypted_message}")
            
            if original_message:
                if decrypted_message == original_message:
                    print(f"✓✓ Coincide con el mensaje original: {original_message} ✓✓")
                else:
                    print(f"❌ NO coincide con el mensaje original: {original_message}")
        
        elif choice == '5':
            print_section("INFORMACIÓN DEL SISTEMA")
            print(f"Claves públicas:  m = {m}, e = {e}")
            print(f"Claves privadas:  p = {p}, q = {q}, d = {d}")
            if phi:
                print(f"φ(n) = {phi}")
            if original_message:
                print(f"\nMensaje original: {original_message}")
                print(f"Representación numérica: {numeric_repr}")
            if blocks:
                print(f"\nBloques: {[(M, n) for M, n in blocks]}")
            if encrypted:
                print(f"Cifrado: {[C for C, _ in encrypted]}")
        
        elif choice == '6':
            demo_rsa()
        
        elif choice == '7':
            show_details = not show_details
            print(f"✓ Modo detallado: {'ACTIVADO' if show_details else 'DESACTIVADO'}")
        
        elif choice == '8':
            print("\n¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida. Intente nuevamente.")


def main():
    """Función principal."""
    print("\n" + "="*70)
    print(" "*15 + "SISTEMA RSA EDUCATIVO")
    print(" "*10 + "Encriptación/Desencriptación de Texto")
    print("="*70)
    print("\nEste programa implementa RSA para mensajes de texto usando")
    print("el alfabeto A-Z mapeado como: A=00, B=01, ..., Z=25")
    print()
    
    while True:
        print("\nModo de operación:")
        print("1. Demostración automática (recomendado para empezar)")
        print("2. Modo interactivo (control manual)")
        print("3. Salir")
        
        choice = input("\nSeleccione una opción: ").strip()
        
        if choice == '1':
            demo_rsa()
            input("\nPresione Enter para continuar...")
        elif choice == '2':
            interactive_mode()
            break
        elif choice == '3':
            print("\n¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    main()