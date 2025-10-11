#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cifrado César (Caesar Cipher)
Cifrado por sustitución monoalfabética con desplazamiento fijo
"""


def clean_text(text: str) -> str:
    """
    Limpia el texto dejando solo letras A-Z en mayúsculas.
    
    Funcionamiento:
    - Convierte todo a mayúsculas
    - Elimina caracteres que no sean letras A-Z
    - Preserva solo el alfabeto inglés
    
    Args:
        text: Texto de entrada
    
    Returns:
        Texto limpio (solo A-Z)
    """
    return ''.join(c.upper() for c in text if c.isalpha() and c.upper() <= 'Z')


def cesar_encrypt(plaintext: str, key: int) -> str:
    """
    Cifra un mensaje usando el cifrado César.
    
    Fórmula: C = (M + k) mod 26
    Donde:
    - C: carácter cifrado
    - M: carácter original (0-25)
    - k: clave de desplazamiento
    
    Funcionamiento:
    1. Convierte cada letra a número (A=0, B=1, ..., Z=25)
    2. Suma la clave k
    3. Aplica módulo 26 para mantener en el alfabeto
    4. Convierte de vuelta a letra
    
    Ejemplo: Con k=3
    - A (0) → (0+3) mod 26 = 3 → D
    - X (23) → (23+3) mod 26 = 0 → A (cicla)
    
    Args:
        plaintext: Mensaje a cifrar (texto plano)
        key: Desplazamiento (0-25)
    
    Returns:
        Mensaje cifrado
    """
    plaintext = clean_text(plaintext)
    ciphertext = ""
    
    for char in plaintext:
        # Convertir letra a número (A=0)
        m = ord(char) - ord('A')
        
        # Aplicar fórmula César: (m + k) mod 26
        c = (m + key) % 26
        
        # Convertir número de vuelta a letra
        ciphertext += chr(c + ord('A'))
    
    return ciphertext


def cesar_decrypt(ciphertext: str, key: int) -> str:
    """
    Descifra un mensaje cifrado con César.
    
    Fórmula: M = (C - k) mod 26
    Donde:
    - M: carácter original recuperado
    - C: carácter cifrado (0-25)
    - k: clave de desplazamiento
    
    Funcionamiento:
    1. Convierte cada letra cifrada a número
    2. Resta la clave k
    3. Aplica módulo 26 (para manejar números negativos)
    4. Convierte de vuelta a letra
    
    Nota: Descifrar es equivalente a cifrar con clave -k
    Es decir: decrypt(C, k) = encrypt(C, -k)
    
    Args:
        ciphertext: Mensaje cifrado
        key: Desplazamiento usado al cifrar (0-25)
    
    Returns:
        Mensaje original (texto plano)
    """
    ciphertext = clean_text(ciphertext)
    plaintext = ""
    
    for char in ciphertext:
        # Convertir letra a número
        c = ord(char) - ord('A')
        
        # Aplicar fórmula inversa: (c - k) mod 26
        m = (c - key) % 26
        
        # Convertir número de vuelta a letra
        plaintext += chr(m + ord('A'))
    
    return plaintext


def cesar_brute_force(ciphertext: str):
    """
    Ataque de fuerza bruta: prueba todas las claves posibles.
    
    Funcionamiento:
    - El cifrado César solo tiene 26 claves posibles (0-25)
    - Prueba descifrar con cada clave
    - Muestra todos los resultados
    - El usuario puede identificar el mensaje correcto
    
    Vulnerabilidad:
    - César es inseguro porque el espacio de claves es muy pequeño
    - Un atacante puede probar todas las claves en segundos
    
    Args:
        ciphertext: Mensaje cifrado a atacar
    """
    print("\n" + "="*70)
    print("ATAQUE DE FUERZA BRUTA - TODAS LAS CLAVES POSIBLES")
    print("="*70)
    
    ciphertext = clean_text(ciphertext)
    
    for key in range(26):
        decrypted = cesar_decrypt(ciphertext, key)
        print(f"Clave {key:2d}: {decrypted}")


def show_transformation_table(plaintext: str, key: int):
    """
    Muestra la tabla de transformación letra por letra.
    
    Ayuda a entender cómo funciona el cifrado visualmente.
    Muestra cada letra original, su desplazamiento y resultado.
    
    Args:
        plaintext: Mensaje a cifrar
        key: Clave de desplazamiento
    """
    plaintext = clean_text(plaintext)
    ciphertext = cesar_encrypt(plaintext, key)
    
    print("\n" + "="*70)
    print("TABLA DE TRANSFORMACIÓN DETALLADA")
    print("="*70)
    print(f"Clave de desplazamiento: k = {key}\n")
    print(f"{'Original':<10} {'Valor':<8} {'Operación':<20} {'Nuevo Valor':<12} {'Cifrado':<10}")
    print("-"*70)
    
    for i, char in enumerate(plaintext):
        m = ord(char) - ord('A')
        c = (m + key) % 26
        cipher_char = ciphertext[i]
        
        operation = f"({m} + {key}) mod 26"
        print(f"{char:<10} {m:<8} {operation:<20} {c:<12} {cipher_char:<10}")


def demo_cesar():
    """Demostración automática del cifrado César"""
    print("="*70)
    print(" "*20 + "CIFRADO CÉSAR - DEMOSTRACIÓN")
    print("="*70)
    
    # Ejemplo 1: Mensaje simple
    mensaje = "HELLO"
    clave = 3
    
    print(f"\n📝 Ejemplo 1: Cifrado básico")
    print(f"   Mensaje original: {mensaje}")
    print(f"   Clave: {clave}")
    
    cifrado = cesar_encrypt(mensaje, clave)
    print(f"   Mensaje cifrado: {cifrado}")
    
    descifrado = cesar_decrypt(cifrado, clave)
    print(f"   Mensaje descifrado: {descifrado}")
    print(f"   ✓ Verificación: {mensaje == descifrado}")
    
    # Mostrar transformación detallada
    show_transformation_table(mensaje, clave)
    
    # Ejemplo 2: Ataque de fuerza bruta
    print(f"\n📝 Ejemplo 2: Ataque de fuerza bruta")
    print(f"   Mensaje cifrado: {cifrado}")
    cesar_brute_force(cifrado)


def interactive_mode():
    """Modo interactivo para el usuario"""
    print("\n" + "="*70)
    print(" "*20 + "CIFRADO CÉSAR - MODO INTERACTIVO")
    print("="*70)
    
    while True:
        print("\n" + "="*70)
        print("MENÚ PRINCIPAL")
        print("="*70)
        print("1. Cifrar mensaje")
        print("2. Descifrar mensaje")
        print("3. Ataque de fuerza bruta")
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
            
            try:
                clave = int(input("Ingrese la clave de desplazamiento (0-25): ").strip())
                if not (0 <= clave <= 25):
                    print("❌ Error: La clave debe estar entre 0 y 25")
                    continue
            except ValueError:
                print("❌ Error: Ingrese un número válido")
                continue
            
            mensaje_limpio = clean_text(mensaje)
            if not mensaje_limpio:
                print("❌ Error: El mensaje debe contener al menos una letra")
                continue
            
            if mensaje != mensaje_limpio:
                print(f"\n⚠️  Texto limpio: {mensaje_limpio}")
            
            cifrado = cesar_encrypt(mensaje_limpio, clave)
            
            print(f"\n{'='*70}")
            print("RESULTADO")
            print("="*70)
            print(f"Mensaje original: {mensaje_limpio}")
            print(f"Clave: {clave}")
            print(f"Mensaje cifrado: {cifrado}")
            
            ver_tabla = input("\n¿Desea ver la tabla de transformación? (s/n): ").strip().lower()
            if ver_tabla == 's':
                show_transformation_table(mensaje_limpio, clave)
        
        elif opcion == '2':
            # Descifrar
            print("\n" + "="*70)
            print("DESCIFRAR MENSAJE")
            print("="*70)
            
            cifrado = input("Ingrese el mensaje cifrado (solo letras A-Z): ").strip()
            
            try:
                clave = int(input("Ingrese la clave de desplazamiento (0-25): ").strip())
                if not (0 <= clave <= 25):
                    print("❌ Error: La clave debe estar entre 0 y 25")
                    continue
            except ValueError:
                print("❌ Error: Ingrese un número válido")
                continue
            
            cifrado_limpio = clean_text(cifrado)
            if not cifrado_limpio:
                print("❌ Error: El mensaje debe contener al menos una letra")
                continue
            
            descifrado = cesar_decrypt(cifrado_limpio, clave)
            
            print(f"\n{'='*70}")
            print("RESULTADO")
            print("="*70)
            print(f"Mensaje cifrado: {cifrado_limpio}")
            print(f"Clave: {clave}")
            print(f"Mensaje descifrado: {descifrado}")
        
        elif opcion == '3':
            # Fuerza bruta
            print("\n" + "="*70)
            print("ATAQUE DE FUERZA BRUTA")
            print("="*70)
            
            cifrado = input("Ingrese el mensaje cifrado (solo letras A-Z): ").strip()
            cifrado_limpio = clean_text(cifrado)
            
            if not cifrado_limpio:
                print("❌ Error: El mensaje debe contener al menos una letra")
                continue
            
            cesar_brute_force(cifrado_limpio)
        
        elif opcion == '4':
            # Demostración
            demo_cesar()
        
        elif opcion == '5':
            # Salir
            print("\n¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida. Intente nuevamente.")


def main():
    """Función principal"""
    print("\n" + "="*70)
    print(" "*15 + "CIFRADO CÉSAR (CAESAR CIPHER)")
    print(" "*10 + "Cifrado por Desplazamiento Alfabético")
    print("="*70)
    print("\nEl cifrado César desplaza cada letra del alfabeto un número")
    print("fijo de posiciones. Es uno de los cifrados más antiguos.")
    print("\nFórmulas:")
    print("  • Cifrado:    C = (M + k) mod 26")
    print("  • Descifrado: M = (C - k) mod 26")
    
    while True:
        print("\n" + "="*70)
        print("Modo de operación:")
        print("1. Demostración automática (recomendado)")
        print("2. Modo interactivo")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == '1':
            demo_cesar()
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