import math
import numpy as np
from itertools import permutations
import re

class CryptoDecoder:
    def __init__(self):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
    def limpiar_texto(self, texto):
        """Limpia el texto manteniendo solo letras y convirtiendo a mayúsculas"""
        return ''.join(c.upper() for c in texto if c.isalpha())
    
    def es_texto_legible(self, texto):
        """Heurística simple para determinar si el texto descifrado es legible"""
        # Busca patrones comunes en español
        patrones_comunes = ['EL ', 'LA ', 'DE ', 'QUE ', 'Y ', 'EN ', 'UN ', 'ES ', 'SE ', 'NO ', 'TE ', 'LO ', 'LE ']
        texto_con_espacios = texto + ' '
        
        coincidencias = sum(1 for patron in patrones_comunes if patron in texto_con_espacios)
        return coincidencias >= 2 or len([c for c in 'AEIOU' if c in texto]) > len(texto) * 0.3
    
    def cifrado_cesar_descifrar(self, texto_cifrado):
        """Descifra usando todas las posibles rotaciones del cifrado César"""
        texto_limpio = self.limpiar_texto(texto_cifrado)
        resultados = []
        
        print("\n=== CIFRADO DE CÉSAR - TODAS LAS POSIBILIDADES ===")
        print("(Mostrando el resultado de aplicar cada desplazamiento)")
        
        for desplazamiento in range(26):
            texto_resultado = ""
            for char in texto_limpio:
                if char in self.alphabet:
                    # CORREGIDO: Para probar si fue cifrado con X, aplicamos +X
                    nueva_pos = (self.alphabet.index(char) + desplazamiento) % 26
                    texto_resultado += self.alphabet[nueva_pos]
                else:
                    texto_resultado += char
            
            es_legible = self.es_texto_legible(texto_resultado)
            resultados.append((desplazamiento, texto_resultado, es_legible))
            
            status = "⭐ POSIBLE" if es_legible else ""
            if desplazamiento == 0:
                print(f"Desplazamiento {desplazamiento:2d}: {texto_resultado} (texto original)")
            else:
                print(f"Desplazamiento {desplazamiento:2d}: {texto_resultado} {status}")
        
        # Mostrar los más probables
        probables = [r for r in resultados if r[2] and r[0] != 0]  # Excluir desplazamiento 0
        if probables:
            print(f"\n🎯 RESULTADOS MÁS PROBABLES:")
            for desp, texto, _ in probables:
                print(f"   Si fue cifrado con desplazamiento {desp}: {texto}")
        
        return resultados
    
    def gcd_extendido(self, a, b):
        """Algoritmo extendido de Euclides"""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.gcd_extendido(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def inverso_modular(self, a, m):
        """Calcula el inverso modular de a módulo m"""
        gcd, x, _ = self.gcd_extendido(a, m)
        if gcd != 1:
            return None
        return (x % m + m) % m
    
    def cifrado_afin_descifrar(self, texto_cifrado):
        """Descifra usando cifrado afín probando diferentes claves"""
        texto_limpio = self.limpiar_texto(texto_cifrado)
        resultados = []
        
        print("\n=== CIFRADO AFÍN ===")
        print("Probando diferentes combinaciones de claves (a, b)...")
        
        # Valores de 'a' que son coprimos con 26
        valores_a_validos = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        
        contador = 0
        for a in valores_a_validos:
            a_inv = self.inverso_modular(a, 26)
            if a_inv is None:
                continue
                
            for b in range(26):
                texto_descifrado = ""
                for char in texto_limpio:
                    if char in self.alphabet:
                        y = self.alphabet.index(char)
                        x = (a_inv * (y - b)) % 26
                        texto_descifrado += self.alphabet[x]
                    else:
                        texto_descifrado += char
                
                es_legible = self.es_texto_legible(texto_descifrado)
                
                if es_legible or contador < 10:  # Mostrar los primeros 10 y todos los legibles
                    status = "⭐ POSIBLE" if es_legible else ""
                    print(f"a={a:2d}, b={b:2d}: {texto_descifrado} {status}")
                    
                if es_legible:
                    resultados.append((a, b, texto_descifrado))
                    
                contador += 1
        
        if resultados:
            print(f"\n🎯 RESULTADOS MÁS PROBABLES:")
            for a, b, texto in resultados:
                print(f"   a={a}, b={b}: {texto}")
        else:
            print("No se encontraron resultados legibles claros.")
        
        return resultados
    
    def determinante_2x2(self, matriz):
        """Calcula el determinante de una matriz 2x2"""
        return (matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]) % 26
    
    def inversa_matriz_2x2(self, matriz):
        """Calcula la inversa de una matriz 2x2 módulo 26"""
        det = self.determinante_2x2(matriz)
        det_inv = self.inverso_modular(det, 26)
        
        if det_inv is None:
            return None
        
        inversa = [
            [(matriz[1][1] * det_inv) % 26, (-matriz[0][1] * det_inv) % 26],
            [(-matriz[1][0] * det_inv) % 26, (matriz[0][0] * det_inv) % 26]
        ]
        
        return inversa
    
    def cifrado_hill_descifrar(self, texto_cifrado, tamaño_clave=2):
        """Descifra usando cifrado de Hill con diferentes matrices clave"""
        texto_limpio = self.limpiar_texto(texto_cifrado)
        
        if len(texto_limpio) % tamaño_clave != 0:
            texto_limpio += 'X' * (tamaño_clave - len(texto_limpio) % tamaño_clave)
        
        print(f"\n=== CIFRADO DE HILL (Matriz {tamaño_clave}x{tamaño_clave}) ===")
        print("Probando diferentes matrices clave...")
        
        resultados = []
        matrices_probadas = 0
        
        # Probar diferentes matrices 2x2
        for a in range(1, 26, 2):  # Solo números impares para mejor probabilidad
            if math.gcd(a, 26) != 1:
                continue
            for b in range(0, 26, 3):
                for c in range(0, 26, 3):
                    for d in range(1, 26, 2):
                        if math.gcd(d, 26) != 1:
                            continue
                        
                        matriz_clave = [[a, b], [c, d]]
                        matriz_inversa = self.inversa_matriz_2x2(matriz_clave)
                        
                        if matriz_inversa is None:
                            continue
                        
                        texto_descifrado = ""
                        
                        # Procesar texto en bloques
                        for i in range(0, len(texto_limpio), tamaño_clave):
                            bloque = texto_limpio[i:i+tamaño_clave]
                            if len(bloque) == tamaño_clave:
                                # Convertir letras a números
                                numeros = [self.alphabet.index(c) for c in bloque]
                                
                                # Multiplicar por matriz inversa
                                resultado = [
                                    (matriz_inversa[0][0] * numeros[0] + matriz_inversa[0][1] * numeros[1]) % 26,
                                    (matriz_inversa[1][0] * numeros[0] + matriz_inversa[1][1] * numeros[1]) % 26
                                ]
                                
                                # Convertir números a letras
                                texto_descifrado += ''.join(self.alphabet[num] for num in resultado)
                        
                        es_legible = self.es_texto_legible(texto_descifrado)
                        matrices_probadas += 1
                        
                        if es_legible:
                            print(f"Matriz [[{a},{b}],[{c},{d}]]: {texto_descifrado} ⭐ POSIBLE")
                            resultados.append((matriz_clave, texto_descifrado))
                        elif matrices_probadas <= 5:  # Mostrar las primeras 5
                            print(f"Matriz [[{a},{b}],[{c},{d}]]: {texto_descifrado}")
                        
                        if matrices_probadas >= 100:  # Limitar búsqueda
                            break
                    if matrices_probadas >= 100:
                        break
                if matrices_probadas >= 100:
                    break
            if matrices_probadas >= 100:
                break
        
        print(f"\nSe probaron {matrices_probadas} matrices.")
        
        if resultados:
            print(f"\n🎯 RESULTADOS MÁS PROBABLES:")
            for matriz, texto in resultados[:5]:  # Mostrar los 5 mejores
                print(f"   Matriz {matriz}: {texto}")
        else:
            print("No se encontraron resultados legibles claros.")
        
        return resultados
    
    def cifrado_bloque_descifrar(self, texto_cifrado, tamaño_bloque=4):
        """Descifra usando transposición de bloques con diferentes permutaciones"""
        texto_limpio = self.limpiar_texto(texto_cifrado)
        
        # Ajustar longitud del texto
        while len(texto_limpio) % tamaño_bloque != 0:
            texto_limpio += 'X'
        
        print(f"\n=== CIFRADO DE BLOQUE (Tamaño de bloque: {tamaño_bloque}) ===")
        print("Probando diferentes permutaciones de transposición...")
        
        resultados = []
        
        # Generar algunas permutaciones comunes para el tamaño de bloque
        if tamaño_bloque <= 4:
            # Para bloques pequeños, probar todas las permutaciones
            todas_permutaciones = list(permutations(range(tamaño_bloque)))
            permutaciones_a_probar = todas_permutaciones[:24]  # Limitar a 24 permutaciones
        else:
            # Para bloques grandes, usar algunas permutaciones comunes
            permutaciones_a_probar = [
                tuple(range(tamaño_bloque)),  # Sin cambios
                tuple(reversed(range(tamaño_bloque))),  # Reverso
                tuple(range(1, tamaño_bloque)) + (0,),  # Rotar izquierda
                (tamaño_bloque-1,) + tuple(range(tamaño_bloque-1))  # Rotar derecha
            ]
        
        for i, permutacion in enumerate(permutaciones_a_probar):
            texto_descifrado = ""
            
            # Procesar cada bloque
            for j in range(0, len(texto_limpio), tamaño_bloque):
                bloque = texto_limpio[j:j+tamaño_bloque]
                if len(bloque) == tamaño_bloque:
                    # Aplicar la permutación inversa
                    bloque_descifrado = [''] * tamaño_bloque
                    for k, pos in enumerate(permutacion):
                        bloque_descifrado[pos] = bloque[k]
                    texto_descifrado += ''.join(bloque_descifrado)
            
            es_legible = self.es_texto_legible(texto_descifrado)
            
            if es_legible or i < 8:  # Mostrar los primeros 8 y todos los legibles
                status = "⭐ POSIBLE" if es_legible else ""
                print(f"Permutación {permutacion}: {texto_descifrado} {status}")
            
            if es_legible:
                resultados.append((permutacion, texto_descifrado))
        
        if resultados:
            print(f"\n🎯 RESULTADOS MÁS PROBABLES:")
            for perm, texto in resultados:
                print(f"   Permutación {perm}: {texto}")
        else:
            print("No se encontraron resultados legibles claros.")
        
        return resultados

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*60)
    print("🔓 DESCIFRADOR CRIPTOGRÁFICO")
    print("="*60)
    print("Seleccione el método de descifrado:")
    print("1. 🔄 Cifrado de César (todas las rotaciones)")
    print("2. 🧮 Cifrado Afín")
    print("3. 📊 Cifrado de Hill (matriz 2x2)")
    print("4. 🧩 Cifrado de Bloque (transposición)")
    print("5. 🚀 Probar todos los métodos")
    print("6. ❌ Salir")
    print("-" * 60)

def main():
    decoder = CryptoDecoder()
    
    print("🔓 BIENVENIDO AL DESCIFRADOR CRIPTOGRÁFICO")
    print("Este programa intentará descifrar texto usando diferentes métodos.")
    
    while True:
        # Pedir texto al usuario
        print("\n" + "="*60)
        texto_cifrado = input("📝 Ingrese el texto cifrado que desea descifrar: ").strip()
        
        if not texto_cifrado:
            print("⚠️  No se ingresó ningún texto. Intente de nuevo.")
            continue
        
        print(f"✅ Texto recibido: {texto_cifrado}")
        print(f"📊 Longitud: {len(texto_cifrado)} caracteres")
        
        while True:
            mostrar_menu()
            
            try:
                opcion = input("Seleccione una opción (1-6): ").strip()
                
                if opcion == '1':
                    decoder.cifrado_cesar_descifrar(texto_cifrado)
                    
                elif opcion == '2':
                    decoder.cifrado_afin_descifrar(texto_cifrado)
                    
                elif opcion == '3':
                    decoder.cifrado_hill_descifrar(texto_cifrado)
                    
                elif opcion == '4':
                    decoder.cifrado_bloque_descifrar(texto_cifrado)
                    
                elif opcion == '5':
                    print("\n🚀 PROBANDO TODOS LOS MÉTODOS...")
                    print("Esto puede tomar unos momentos...")
                    
                    decoder.cifrado_cesar_descifrar(texto_cifrado)
                    decoder.cifrado_afin_descifrar(texto_cifrado)
                    
                    print("¿Conoce la matriz clave para Hill? (s/n): ", end="")
                    conoce_clave = input().strip().lower()
                    if conoce_clave == 's':
                        matriz = decoder.pedir_matriz_hill()
                        if matriz:
                            decoder.cifrado_hill_descifrar(texto_cifrado, matriz_clave=matriz)
                        else:
                            decoder.cifrado_hill_descifrar(texto_cifrado)
                    else:
                        decoder.cifrado_hill_descifrar(texto_cifrado)
                    
                    decoder.cifrado_bloque_descifrar(texto_cifrado)
                    
                    print("\n✅ Análisis completo terminado.")
                    
                elif opcion == '6':
                    print("👋 ¡Gracias por usar el descifrador criptográfico!")
                    return
                    
                else:
                    print("⚠️  Opción no válida. Seleccione un número del 1 al 6.")
                    continue
                
                # Preguntar si quiere continuar con el mismo texto
                continuar = input("\n¿Desea probar otro método con el mismo texto? (s/n): ").strip().lower()
                if continuar != 's':
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrumpido por el usuario.")
                return
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        print("Por favor, reinicie el programa.")