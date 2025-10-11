#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cifrado Afín (Affine Cipher)
Generalización del cifrado César usando función afín: C = (a*M + b) mod 26
"""


def clean_text(text: str) -> str:
    """
    Limpia el texto dejando solo letras A-Z en mayúsculas.
    
    Args:
        text: Texto de entrada
    
    Returns:
        Texto limpio (solo A-Z)
    """
    return ''.join(c.upper() for c in text if c.isalpha() and c.upper() <= 'Z')


def gcd(a: int, b: int) -> int:
    """
    Calcula el Máximo Común Divisor usando el algoritmo de Euclides.
    
    Funcionamiento:
    - Divide a entre b y toma el residuo
    - Reemplaza a con b, y b con el residuo
    - Repite hasta que b sea 0
    - El último valor de a es el MCD
    
    Aplicación en Afín:
    - Se usa para verificar que gcd(a, 26) = 1
    - Solo si son coprimos, a tiene inverso modular
    
    Args:
        a, b: Números enteros
    
    Returns:
        MCD(a, b)
    """
    while b != 0:
        a, b = b, a % b
    return abs(a)


def extended_gcd(a: int, b: int) -> tuple:
    """
    Algoritmo de Euclides Extendido.
    Retorna (gcd, x, y) tal que: a*x + b*y = gcd(a,b)
    
    Funcionamiento:
    - Usa recursión para llegar al caso base (b=0)
    - Al regresar, calcula los coeficientes x, y
    - Estos coeficientes son la Identidad de Bézout
    
    Aplicación en Afín:
    - Se usa para calcular el inverso modular de 'a'
    - Necesario para la fórmula de descifrado
    
    Args:
        a, b: Números enteros
    
    Returns:
        Tupla (gcd, x, y)
    """
    if b == 0:
        return abs(a), 1 if a >= 0 else -1, 0
    
    gcd_val, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    return gcd_val, x, y


def modular_inverse(a: int, m: int) -> int:
    """
    Calcula el inverso modular de 'a' módulo 'm'.
    Encuentra x tal que: (a * x) mod m = 1
    
    Funcionamiento:
    1. Usa extended_gcd para obtener x tal que a*x + m*y = gcd
    2. Si gcd(a,m) = 1, entonces x es el inverso modular
    3. Aplica módulo m para asegurar resultado positivo
    
    Aplicación en Afín:
    - Se usa para calcular a^(-1) mod 26
    - Necesario en la fórmula de descifrado: M = a^(-1) * (C - b) mod 26
    
    Args:
        a: Número a invertir
        m: Módulo
    
    Returns:
        Inverso modular de a módulo m
    
    Raises:
        ValueError: Si no existe inverso (gcd(a,m) ≠ 1)
    """
    gcd_val, x, _ = extended_gcd(a, m)
    
    if gcd_val != 1:
        raise ValueError(f"No existe inverso: gcd({a}, {m}) = {gcd_val} ≠ 1")
    
    return x % m


def is_valid_key_a(a: int) -> bool:
    """
    Verifica si 'a' es una clave válida para el cifrado Afín.
    
    Condición: gcd(a, 26) = 1
    
    Explicación:
    - 'a' debe ser coprimo con 26
    - Solo así tiene inverso modular
    - Sin inverso, no se puede descifrar
    
    Valores válidos de 'a': 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
    (Son los números coprimos con 26 en el rango 1-25)
    
    Args:
        a: Clave multiplicativa candidata
    
    Returns:
        True si es válida, False si no
    """
    return gcd(a, 26) == 1


def get_valid_keys_a() -> list:
    """
    Retorna la lista de todas las claves 'a' válidas.
    
    Returns:
        Lista de enteros válidos para 'a'
    """
    return [a for a in range(1, 26) if is_valid_key_a(a)]


def afin_encrypt(plaintext: str, a: int, b: int) -> str:
    """
    Cifra un mensaje usando el cifrado Afín.
    
    Fórmula: C = (a*M + b) mod 26
    
    Funcionamiento:
    1. Verifica que 'a' sea válida (gcd(a, 26) = 1)
    2. Para cada letra:
       a. Convierte letra a número (A=0, B=1, ..., Z=25)
       b. Aplica la transformación afín: a*M + b
       c. Aplica módulo 26
       d. Convierte de vuelta a letra
    
    Componentes:
    - a: clave multiplicativa (debe ser coprimo con 26)
    - b: clave aditiva (desplazamiento, puede ser 0-25)
    
    Casos especiales:
    - Si a=1, se reduce a César con clave b
    - Si b=0, es solo multiplicación
    
    Args:
        plaintext: Mensaje a cifrar
        a: Clave multiplicativa (debe cumplir gcd(a,26)=1)
        b: Clave aditiva (0-25)
    
    Returns:
        Mensaje cifrado
    
    Raises:
        ValueError: Si 'a' no es válida
    """
    if not is_valid_key_a(a):
        raise ValueError(f"La clave 'a'={a} no es válida. gcd({a}, 26) debe ser 1")
    
    plaintext = clean_text(plaintext)
    ciphertext = ""
    
    for char in plaintext:
        # Convertir letra a número (A=0)
        m = ord(char) - ord('A')
        
        # Aplicar fórmula afín: (a*m + b) mod 26
        c = (a * m + b) % 26
        
        # Convertir número de vuelta a letra
        ciphertext += chr(c + ord('A'))
    
    return ciphertext


def afin_decrypt(ciphertext: str, a: int, b: int) -> str:
    """
    Descifra un mensaje cifrado con Afín.
    
    Fórmula: M = a^(-1) * (C - b) mod 26
    
    Funcionamiento:
    1. Calcula a^(-1) (inverso modular de 'a' módulo 26)
    2. Para cada letra cifrada:
       a. Convierte letra a número
       b. Resta b
       c. Multiplica por a^(-1)
       d. Aplica módulo 26
       e. Convierte de vuelta a letra
    
    Derivación de la fórmula:
    - Cifrado: C = (a*M + b) mod 26
    - Despejar M:
      C = a*M + b (mod 26)
      C - b = a*M (mod 26)
      a^(-1)*(C - b) = M (mod 26)
    
    Args:
        ciphertext: Mensaje cifrado
        a: Clave multiplicativa usada al cifrar
        b: Clave aditiva usada al cifrar
    
    Returns:
        Mensaje original (texto plano)
    
    Raises:
        ValueError: Si 'a' no es válida
    """
    if not is_valid_key_a(a):
        raise ValueError(f"La clave 'a'={a} no es válida. gcd({a}, 26) debe ser 1")
    
    # Calcular inverso modular de 'a'
    a_inv = modular_inverse(a, 26)
    
    ciphertext = clean_text(ciphertext)
    plaintext = ""
    
    for char in ciphertext:
        # Convertir letra a número
        c = ord(char) - ord('A')
        
        # Aplicar fórmula inversa: a^(-1) * (c - b) mod 26
        m = (a_inv * (c - b)) % 26
        
        # Convertir número de vuelta a letra
        plaintext += chr(m + ord('A'))
    
    return plaintext


def show_transformation_table(plaintext: str, a: int, b: int):
    """
    Muestra la tabla de transformación letra por letra.
    
    Ayuda a visualizar cómo funciona la transformación afín.
    Muestra cada paso de la fórmula C = (a*M + b) mod 26
    
    Args:
        plaintext: Mensaje a cifrar
        a: Clave multiplicativa
        b: Clave aditiva
    """
    plaintext = clean_text(plaintext)
    ciphertext = afin_encrypt(plaintext, a, b)
    
    print("\n" + "="*70)
    print("TABLA DE TRANSFORMACIÓN DETALLADA")
    print("="*70)
    print(f"Claves: a = {a}, b = {b}")
    print(f"Fórmula: C = (a*M + b) mod 26 = ({a}*M + {b}) mod 26\n")
    print(f"{'Original':<10} {'M':<6} {'a*M':<8} {'a*M+b':<10} {'(a*M+b)%26':<12} {'Cifrado':<10}")
    print("-"*70)
    
    for i, char in enumerate(plaintext):
        m = ord(char) - ord('A')
        a_m = a * m
        a_m_b = a_m + b
        c = a_m_b % 26
        cipher_char = ciphertext[i]
        
        print(f"{char:<10} {m:<6} {a_m:<8} {a_m_b:<10} {c:<12} {cipher_char:<10}")


def demo_afin():
    """Demostración automática del cifrado Afín"""
    print("="*70)
    print(" "*20 + "CIFRADO AFÍN - DEMOSTRACIÓN")
    print("="*70)
    
    # Ejemplo 1: Mensaje simple
    mensaje = "HELLO"
    a, b = 5, 8
    
    print(f"\n📝 Ejemplo 1: Cifrado básico")
    print(f"   Mensaje original: {mensaje}")
    print(f"   Claves: a = {a}, b = {b}")
    print(f"   Verificación: gcd({a}, 26) = {gcd(a, 26)} ✓")
    
    cifrado = afin_encrypt(mensaje, a, b)
    print(f"   Mensaje cifrado: {cifrado}")
    
    a_inv = modular_inverse(a, 26)
    print(f"   Inverso de a: a^(-1) = {a_inv}")
    print(f"   Verificación: ({a} × {a_inv}) mod 26 = {(a * a_inv) % 26} ✓")
    
    descifrado = afin_decrypt(cifrado, a, b)
    print(f"   Mensaje descifrado: {descifrado}")
    print(f"   ✓ Verificación: {mensaje == descifrado}")
    
    # Mostrar transformación detallada
    show_transformation_table(mensaje, a, b)
    
    # Ejemplo 2: Mostrar claves válidas
    print(f"\n📝 Ejemplo 2: Claves válidas para 'a'")
    valid_keys = get_valid_keys_a()
    print(f"   Valores válidos de 'a' (coprimos con 26):")
    print(f"   {valid_keys}")
    print(f"   Total: {len(valid_keys)} claves válidas")
    
    # Ejemplo 3: Clave inválida
    print(f"\n📝 Ejemplo 3: Intentar con clave inválida")
    invalid_a = 2
    print(f"   Intentando a = {invalid_a}")
    print(f"   gcd({invalid_a}, 26) = {gcd(invalid_a, 26)} ≠ 1")
    print(f"   Resultado: No se puede cifrar (no tiene inverso modular)")


def interactive_mode():
    """Modo interactivo para el usuario"""
    print("\n" + "="*70)
    print(" "*20 + "CIFRADO AFÍN - MODO INTERACTIVO")
    print("="*70)
    
    while True:
        print("\n" + "="*70)
        print("MENÚ PRINCIPAL")
        print("="*70)
        print("1. Cifrar mensaje")
        print("2. Descifrar mensaje")
        print("3. Mostrar claves válidas")
        print("4. Ver demostración")
        print("5. Salir")
        print("="*70)
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == '1':
            # Cifrar
            print("\n" + "="*70)
            print("CIFRAR MENSAJE")
            print("="*70)
            
            mensaje = input("Ingrese el mensaje (solo letras A-Z): ").strip()
            
            print(f"\nClaves válidas para 'a': {get_valid_keys_a()}")
            
            try:
                a = int(input("Ingrese la clave 'a' (debe ser coprimo con 26): ").strip())
                b = int(input("Ingrese la clave 'b' (0-25): ").strip())
                
                if not is_valid_key_a(a):
                    print(f"❌ Error: a={a} no es válida. gcd({a}, 26) = {gcd(a, 26)} ≠ 1")
                    print(f"   Claves válidas: {get_valid_keys_a()}")
                    continue
                
                if not (0 <= b <= 25):
                    print("❌ Error: 'b' debe estar entre 0 y 25")
                    continue
            except ValueError:
                print("❌ Error: Ingrese números válidos")
                continue
            
            mensaje_limpio = clean_text(mensaje)
            if not mensaje_limpio:
                print("❌ Error: El mensaje debe contener al menos una letra")
                continue
            
            cifrado = afin_encrypt(mensaje_limpio, a, b)
            
            print(f"\n{'='*70}")
            print("RESULTADO")
            print("="*70)
            print(f"Mensaje original: {mensaje_limpio}")
            print(f"Claves: a = {a}, b = {b}")
            print(f"Mensaje cifrado: {cifrado}")
            
            ver_tabla = input("\n¿Desea ver la tabla de transformación? (s/n): ").strip().lower()
            if ver_tabla == 's':
                show_transformation_table(mensaje_limpio, a, b)
        
        elif opcion == '2':
            # Descifrar
            print("\n" + "="*70)
            print("DESCIFRAR MENSAJE")
            print("="*70)
            
            cifrado = input("Ingrese el mensaje cifrado (solo letras A-Z): ").strip()
            
            try:
                a = int(input("Ingrese la clave 'a': ").strip())
                b = int(input("Ingrese la clave 'b': ").strip())
                
                if not is_valid_key_a(a):
                    print(f"❌ Error: a={a} no es válida")
                    continue
            except ValueError:
                print("❌ Error: Ingrese números válidos")
                continue
            
            cifrado_limpio = clean_text(cifrado)
            if not cifrado_limpio:
                print("❌ Error: El mensaje debe contener al menos una letra")
                continue
            
            a_inv = modular_inverse(a, 26)
            descifrado = afin_decrypt(cifrado_limpio, a, b)
            
            print(f"\n{'='*70}")
            print("RESULTADO")
            print("="*70)
            print(f"Mensaje cifrado: {cifrado_limpio}")
            print(f"Claves: a = {a}, b = {b}")
            print(f"Inverso de a: a^(-1) = {a_inv}")
            print(f"Mensaje descifrado: {descifrado}")
        
        elif opcion == '3':
            # Mostrar claves válidas
            print("\n" + "="*70)
            print("CLAVES VÁLIDAS PARA 'a'")
            print("="*70)
            valid_keys = get_valid_keys_a()
            print(f"\nValores coprimos con 26:")
            print(f"{valid_keys}")
            print(f"\nTotal: {len(valid_keys)} claves válidas")
            print("\nNota: Solo estos valores de 'a' tienen inverso modular.")
        
        elif opcion == '4':
            # Demostración
            demo_afin()
        
        elif opcion == '5':
            # Salir
            print("\n¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida. Intente nuevamente.")


def main():
    """Función principal"""
    print("\n" + "="*70)
    print(" "*15 + "CIFRADO AFÍN (AFFINE CIPHER)")
    print(" "*10 + "Cifrado por Transformación Afín")
    print("="*70)
    print("\nEl cifrado Afín usa una función afín para transformar cada letra.")
    print("Es una generalización del cifrado César.")
    print("\nFórmulas:")
    print("  • Cifrado:    C = (a*M + b) mod 26")
    print("  • Descifrado: M = a^(-1) * (C - b) mod 26")
    print("\nRequisito: gcd(a, 26) = 1 (a debe ser coprimo con 26)")
    
    while True:
        print("\n" + "="*70)
        print("Modo de operación:")
        print("1. Demostración automática (recomendado)")
        print("2. Modo interactivo")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == '1':
            demo_afin()
            input("\nPresione Enter para continuar...")
        elif opcion == '2':
            interactive_mode()
            break
        elif opcion == '3':
            print("\n¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    main()