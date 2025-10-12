#!/usr/bin/env python3
"""
CIFRADO DE VIGENÈRE - Script de Consola Interactivo
====================================================
Implementación completa del cifrado de Vigenère (polialfabético).
Alfabeto: A=0, B=1, ..., Z=25 (26 letras)
"""

def limpiar_texto(texto):
    """
    Limpia el texto dejando solo letras mayúsculas del alfabeto inglés.
    
    Parámetros:
        texto: cadena de entrada
    
    Retorna:
        Cadena con solo letras mayúsculas A-Z
    """
    return ''.join(c.upper() for c in texto if c.isalpha())


def preparar_clave(clave, longitud_mensaje):
    """
    Repite la clave hasta que coincida con la longitud del mensaje.
    
    Parámetros:
        clave: palabra clave (string)
        longitud_mensaje: longitud del mensaje a cifrar
    
    Retorna:
        Clave extendida del mismo tamaño que el mensaje
    
    Ejemplo:
        clave = "KEY", longitud = 10
        resultado = "KEYKEYKEYKEY"[:10] = "KEYKEYKEYK"
    """
    clave_limpia = limpiar_texto(clave)
    if not clave_limpia:
        raise ValueError("La clave no puede estar vacía")
    
    # Repetir la clave hasta cubrir la longitud del mensaje
    repeticiones_necesarias = (longitud_mensaje // len(clave_limpia)) + 1
    clave_extendida = (clave_limpia * repeticiones_necesarias)[:longitud_mensaje]
    
    return clave_extendida


def texto_a_numeros(texto):
    """
    Convierte texto a lista de números (A=0, B=1, ..., Z=25).
    
    Parámetros:
        texto: cadena de letras mayúsculas
    
    Retorna:
        Lista de números [0-25]
    """
    return [ord(c) - ord('A') for c in texto]


def numeros_a_texto(numeros):
    """
    Convierte lista de números a texto (0=A, 1=B, ..., 25=Z).
    
    Parámetros:
        numeros: lista de números [0-25]
    
    Retorna:
        Cadena de letras mayúsculas
    """
    return ''.join(chr(n + ord('A')) for n in numeros)


def cifrar_vigenere(texto, clave):
    """
    Cifra un texto usando el Cifrado de Vigenère: C[i] = (M[i] + K[i]) mod 26
    
    El cifrado de Vigenère es un cifrado polialfabético que usa una palabra clave.
    Cada letra de la clave determina un desplazamiento diferente.
    
    Parámetros:
        texto: mensaje a cifrar
        clave: palabra clave para el cifrado
    
    Retorna:
        Tupla (texto_cifrado, detalles) donde detalles es una lista de diccionarios
    """
    texto_limpio = limpiar_texto(texto)
    
    if not texto_limpio:
        raise ValueError("El texto no puede estar vacío")
    
    # Preparar la clave extendida
    clave_extendida = preparar_clave(clave, len(texto_limpio))
    
    # Convertir a números
    numeros_mensaje = texto_a_numeros(texto_limpio)
    numeros_clave = texto_a_numeros(clave_extendida)
    
    detalles = []
    numeros_cifrados = []
    
    for i, (m, k) in enumerate(zip(numeros_mensaje, numeros_clave)):
        # Fórmula de cifrado: c = (m + k) mod 26
        c = (m + k) % 26
        numeros_cifrados.append(c)
        
        detalles.append({
            'posicion': i,
            'letra_mensaje': texto_limpio[i],
            'valor_mensaje': m,
            'letra_clave': clave_extendida[i],
            'valor_clave': k,
            'calculo': f"({m} + {k}) mod 26 = {m + k} mod 26 = {c}",
            'letra_cifrada': chr(c + ord('A')),
            'valor_cifrado': c
        })
    
    texto_cifrado = numeros_a_texto(numeros_cifrados)
    return texto_cifrado, clave_extendida, detalles


def descifrar_vigenere(texto_cifrado, clave):
    """
    Descifra un texto usando el Cifrado de Vigenère: M[i] = (C[i] - K[i]) mod 26
    
    Para descifrar, restamos el valor de la clave en lugar de sumarlo.
    
    Parámetros:
        texto_cifrado: mensaje cifrado
        clave: palabra clave usada en el cifrado
    
    Retorna:
        Tupla (texto_descifrado, detalles) donde detalles es una lista de diccionarios
    """
    texto_limpio = limpiar_texto(texto_cifrado)
    
    if not texto_limpio:
        raise ValueError("El texto cifrado no puede estar vacío")
    
    # Preparar la clave extendida
    clave_extendida = preparar_clave(clave, len(texto_limpio))
    
    # Convertir a números
    numeros_cifrado = texto_a_numeros(texto_limpio)
    numeros_clave = texto_a_numeros(clave_extendida)
    
    detalles = []
    numeros_descifrados = []
    
    for i, (c, k) in enumerate(zip(numeros_cifrado, numeros_clave)):
        # Fórmula de descifrado: m = (c - k) mod 26
        m = (c - k) % 26
        numeros_descifrados.append(m)
        
        detalles.append({
            'posicion': i,
            'letra_cifrada': texto_limpio[i],
            'valor_cifrado': c,
            'letra_clave': clave_extendida[i],
            'valor_clave': k,
            'calculo': f"({c} - {k}) mod 26 = {c - k} mod 26 = {m}",
            'letra_original': chr(m + ord('A')),
            'valor_original': m
        })
    
    texto_descifrado = numeros_a_texto(numeros_descifrados)
    return texto_descifrado, clave_extendida, detalles


def mostrar_detalles_cifrado(detalles, clave_extendida):
    """Muestra los detalles del proceso de cifrado en formato tabular."""
    print("\n" + "="*90)
    print("DETALLES DEL PROCESO DE CIFRADO")
    print("="*90)
    print(f"Clave extendida: {clave_extendida}")
    print("-"*90)
    print(f"{'Pos':<4} {'Mensaje':<8} {'M':<4} {'Clave':<7} {'K':<4} {'Cálculo':<30} {'Cifrado':<8} {'C':<4}")
    print("-"*90)
    
    for d in detalles:
        print(f"{d['posicion']:<4} {d['letra_mensaje']:<8} {d['valor_mensaje']:<4} "
              f"{d['letra_clave']:<7} {d['valor_clave']:<4} {d['calculo']:<30} "
              f"{d['letra_cifrada']:<8} {d['valor_cifrado']:<4}")


def mostrar_detalles_descifrado(detalles, clave_extendida):
    """Muestra los detalles del proceso de descifrado en formato tabular."""
    print("\n" + "="*90)
    print("DETALLES DEL PROCESO DE DESCIFRADO")
    print("="*90)
    print(f"Clave extendida: {clave_extendida}")
    print("-"*90)
    print(f"{'Pos':<4} {'Cifrado':<8} {'C':<4} {'Clave':<7} {'K':<4} {'Cálculo':<30} {'Original':<8} {'M':<4}")
    print("-"*90)
    
    for d in detalles:
        print(f"{d['posicion']:<4} {d['letra_cifrada']:<8} {d['valor_cifrado']:<4} "
              f"{d['letra_clave']:<7} {d['valor_clave']:<4} {d['calculo']:<30} "
              f"{d['letra_original']:<8} {d['valor_original']:<4}")


def menu_principal():
    """Menú interactivo principal del programa."""
    print("\n" + "="*80)
    print(" "*23 + "CIFRADO DE VIGENÈRE")
    print("="*80)
    print("\nFórmulas:")
    print("  • Cifrado:    C[i] = (M[i] + K[i]) mod 26")
    print("  • Descifrado: M[i] = (C[i] - K[i]) mod 26")
    print("\nDonde:")
    print("  • M[i]: letra i del mensaje")
    print("  • K[i]: letra i de la clave (repetida)")
    print("  • C[i]: letra i del cifrado")
    print("\nAlfabeto: A=0, B=1, C=2, ..., Z=25")
    print("="*80)
    
    while True:
        print("\n┌─── MENÚ PRINCIPAL ───┐")
        print("│ 1. Cifrar mensaje    │")
        print("│ 2. Descifrar mensaje │")
        print("│ 3. Ver casos de uso  │")
        print("│ 4. Salir             │")
        print("└──────────────────────┘")
        
        opcion = input("\nSeleccione una opción [1-4]: ").strip()
        
        if opcion == '1':
            cifrar_mensaje()
        elif opcion == '2':
            descifrar_mensaje()
        elif opcion == '3':
            mostrar_casos_uso()
        elif opcion == '4':
            print("\n¡Hasta pronto! 👋\n")
            break
        else:
            print("\n❌ Opción inválida. Intente nuevamente.")


def cifrar_mensaje():
    """Interfaz para cifrar un mensaje."""
    print("\n" + "─"*80)
    print("CIFRADO DE MENSAJE")
    print("─"*80)
    
    mensaje = input("Ingrese el mensaje a cifrar: ").strip()
    
    if not mensaje:
        print("❌ El mensaje no puede estar vacío.")
        return
    
    clave = input("Ingrese la palabra clave: ").strip()
    
    if not clave:
        print("❌ La clave no puede estar vacía.")
        return
    
    try:
        print(f"\n📝 Mensaje original: {mensaje}")
        print(f"🔑 Clave: {clave}")
        
        mensaje_limpio = limpiar_texto(mensaje)
        print(f"📝 Mensaje limpio: {mensaje_limpio}")
        
        texto_cifrado, clave_extendida, detalles = cifrar_vigenere(mensaje, clave)
        
        mostrar_detalles_cifrado(detalles, clave_extendida)
        
        print("\n" + "="*90)
        print(f"🔒 MENSAJE CIFRADO: {texto_cifrado}")
        print("="*90)
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


def descifrar_mensaje():
    """Interfaz para descifrar un mensaje."""
    print("\n" + "─"*80)
    print("DESCIFRADO DE MENSAJE")
    print("─"*80)
    
    mensaje_cifrado = input("Ingrese el mensaje cifrado: ").strip()
    
    if not mensaje_cifrado:
        print("❌ El mensaje no puede estar vacío.")
        return
    
    clave = input("Ingrese la palabra clave: ").strip()
    
    if not clave:
        print("❌ La clave no puede estar vacía.")
        return
    
    try:
        print(f"\n🔒 Mensaje cifrado: {mensaje_cifrado}")
        print(f"🔑 Clave: {clave}")
        
        texto_descifrado, clave_extendida, detalles = descifrar_vigenere(mensaje_cifrado, clave)
        
        mostrar_detalles_descifrado(detalles, clave_extendida)
        
        print("\n" + "="*90)
        print(f"🔓 MENSAJE DESCIFRADO: {texto_descifrado}")
        print("="*90)
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


def mostrar_casos_uso():
    """Muestra casos de uso de ejemplo para probar el cifrado."""
    print("\n" + "="*80)
    print(" "*25 + "CASOS DE USO")
    print("="*80)
    
    casos = [
        {
            'nombre': 'Caso 1: Ejemplo clásico',
            'mensaje': 'ATTACKATDAWN',
            'clave': 'LEMON',
            'esperado': 'LXFOPVEFRNHR'
        },
        {
            'nombre': 'Caso 2: Mensaje corto',
            'mensaje': 'HELLO',
            'clave': 'KEY',
            'esperado': 'RIJVS'
        },
        {
            'nombre': 'Caso 3: Clave larga',
            'mensaje': 'CRYPTO',
            'clave': 'SECRET',
            'esperado': 'UWIRGB'
        },
        {
            'nombre': 'Caso 4: Frase completa',
            'mensaje': 'VIGENERE CIPHER',
            'clave': 'WORD',
            'esperado': 'RMKZIVKVUMRKCV'
        }
    ]
    
    for i, caso in enumerate(casos, 1):
        print(f"\n{'─'*80}")
        print(f"{caso['nombre']}")
        print(f"{'─'*80}")
        print(f"Mensaje:   {caso['mensaje']}")
        print(f"Clave:     {caso['clave']}")
        print(f"Esperado:  {caso['esperado']}")
        print(f"\nPruébalo tú mismo en la opción 1 del menú principal.")
    
    print("\n" + "="*80)
    print("\n💡 Consejos:")
    print("   • La clave puede ser cualquier palabra")
    print("   • Claves más largas proporcionan mejor seguridad")
    print("   • La clave se repite automáticamente para cubrir el mensaje")
    print("   • Ejemplo: clave='KEY', mensaje='HELLO' → clave extendida='KEYKE'")


if __name__ == "__main__":
    menu_principal()