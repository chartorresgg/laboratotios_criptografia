#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Descifrador de texto usando métodos de sustitución
Incluye Cifrado César, análisis de frecuencias y sustitución personalizada
"""

import string
from collections import Counter
import re

class DescifradorSustitucion:
    def __init__(self):
        # Frecuencias aproximadas de letras en español
        self.freq_espanol = {
            'E': 13.68, 'A': 12.53, 'O': 8.68, 'S': 7.98, 'R': 6.87,
            'N': 6.71, 'I': 6.25, 'D': 5.86, 'L': 4.97, 'C': 4.68,
            'T': 4.63, 'U': 3.93, 'M': 3.15, 'P': 2.51, 'B': 2.22,
            'G': 2.01, 'V': 1.90, 'Y': 1.90, 'Q': 1.88, 'H': 1.18,
            'F': 0.92, 'Z': 0.52, 'J': 0.44, 'Ñ': 0.31, 'X': 0.22,
            'K': 0.11, 'W': 0.04
        }
    
    def limpiar_texto(self, texto):
        """Limpia el texto manteniendo solo letras"""
        return re.sub(r'[^A-ZÑ]', '', texto.upper())
    
    def cifrado_cesar(self, texto, desplazamiento):
        """Aplica cifrado César con el desplazamiento dado"""
        alfabeto = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
        resultado = ""
        
        for char in texto:
            if char in alfabeto:
                indice_actual = alfabeto.index(char)
                nuevo_indice = (indice_actual + desplazamiento) % len(alfabeto)
                resultado += alfabeto[nuevo_indice]
            else:
                resultado += char
        
        return resultado
    
    def probar_cesar(self, texto_cifrado):
        """Prueba todos los desplazamientos posibles del cifrado César"""
        print("=== PROBANDO CIFRADO CÉSAR ===")
        texto_limpio = self.limpiar_texto(texto_cifrado)
        
        resultados = []
        for i in range(1, 28):  # 27 letras en el alfabeto español
            descifrado = self.cifrado_cesar(texto_limpio, -i)
            score = self.calcular_puntuacion(descifrado)
            resultados.append((i, descifrado, score))
            print(f"Desplazamiento -{i:2d}: {descifrado} (Score: {score:.2f})")
        
        # Mostrar el mejor resultado
        mejor = max(resultados, key=lambda x: x[2])
        print(f"\n🏆 MEJOR RESULTADO César (Desplazamiento -{mejor[0]}): {mejor[1]}")
        return mejor[1]
    
    def analisis_frecuencia(self, texto):
        """Analiza la frecuencia de letras en el texto"""
        texto_limpio = self.limpiar_texto(texto)
        contador = Counter(texto_limpio)
        total_letras = len(texto_limpio)
        
        print("\n=== ANÁLISIS DE FRECUENCIAS ===")
        print("Letra | Cantidad | Frecuencia | Freq. Esperada (ES)")
        print("-" * 50)
        
        frecuencias = {}
        for letra, cantidad in contador.most_common():
            freq = (cantidad / total_letras) * 100
            freq_esperada = self.freq_espanol.get(letra, 0)
            frecuencias[letra] = freq
            print(f"  {letra}   |    {cantidad:2d}    |   {freq:5.2f}%   |    {freq_esperada:5.2f}%")
        
        return frecuencias
    
    def calcular_puntuacion(self, texto):
        """Calcula puntuación basada en frecuencias esperadas del español"""
        frecuencias = Counter(self.limpiar_texto(texto))
        total = sum(frecuencias.values())
        if total == 0:
            return 0
        
        puntuacion = 0
        for letra, cantidad in frecuencias.items():
            freq_texto = (cantidad / total) * 100
            freq_esperada = self.freq_espanol.get(letra, 0)
            # Penalizar diferencias grandes en frecuencia
            puntuacion += max(0, 10 - abs(freq_texto - freq_esperada))
        
        return puntuacion
    
    def sustitucion_personalizada(self, texto_cifrado, clave_sustitucion):
        """Aplica una clave de sustitución personalizada"""
        resultado = ""
        for char in texto_cifrado.upper():
            if char in clave_sustitucion:
                resultado += clave_sustitucion[char]
            else:
                resultado += char
        return resultado
    
    def sugerir_sustitucion(self, texto_cifrado):
        """Sugiere una sustitución basada en análisis de frecuencias"""
        print("\n=== SUGERENCIA DE SUSTITUCIÓN ===")
        frecuencias = self.analisis_frecuencia(texto_cifrado)
        
        # Ordenar letras por frecuencia
        letras_cifrado = sorted(frecuencias.keys(), key=frecuencias.get, reverse=True)
        letras_espanol = ['E', 'A', 'O', 'S', 'R', 'N', 'I', 'D', 'L', 'C']
        
        sugerencia = {}
        print("\nSugerencia automática basada en frecuencias:")
        for i, letra_cifrada in enumerate(letras_cifrado[:10]):
            if i < len(letras_espanol):
                sugerencia[letra_cifrada] = letras_espanol[i]
                print(f"{letra_cifrada} → {letras_espanol[i]}")
        
        return sugerencia
    
    def descifrar_interactivo(self, texto_cifrado):
        """Modo interactivo para crear clave de sustitución"""
        print("\n=== MODO INTERACTIVO DE SUSTITUCIÓN ===")
        print("Introduce las sustituciones (formato: LETRA_CIFRADA=LETRA_REAL)")
        print("Ejemplo: Z=E, K=S, J=A")
        print("Escribe 'FIN' para terminar")
        
        clave = {}
        letras_unicas = set(self.limpiar_texto(texto_cifrado))
        
        print(f"Letras en el texto cifrado: {sorted(letras_unicas)}")
        
        while True:
            entrada = input("Sustitución (o 'FIN'): ").upper().strip()
            
            if entrada == 'FIN':
                break
            
            if '=' in entrada:
                try:
                    cifrada, real = entrada.split('=')
                    cifrada, real = cifrada.strip(), real.strip()
                    if len(cifrada) == 1 and len(real) == 1:
                        clave[cifrada] = real
                        print(f"✓ {cifrada} → {real}")
                        
                        # Mostrar resultado parcial
                        resultado_parcial = self.sustitucion_personalizada(texto_cifrado, clave)
                        print(f"Resultado parcial: {resultado_parcial}")
                    else:
                        print("❌ Formato incorrecto. Usa una sola letra a cada lado del =")
                except ValueError:
                    print("❌ Formato incorrecto. Usa: LETRA=LETRA")
            else:
                print("❌ Formato incorrecto. Usa: LETRA=LETRA")
        
        return clave

def main():
    descifrador = DescifradorSustitucion()
    
    print("🔍 DESCIFRADOR POR SUSTITUCIÓN")
    print("=" * 40)
    
    # Solicitar texto a descifrar
    texto_cifrado = input("Introduce el texto cifrado: ").strip()
    
    if not texto_cifrado:
        print("❌ No se introdujo ningún texto.")
        return
    
    print(f"\nTexto a descifrar: {texto_cifrado}")
    print(f"Texto limpio: {descifrador.limpiar_texto(texto_cifrado)}")
    
    while True:
        print("\n🎯 OPCIONES:")
        print("1. Probar Cifrado César (todos los desplazamientos)")
        print("2. Análisis de frecuencias")
        print("3. Sugerencia automática de sustitución")
        print("4. Sustitución personalizada (interactiva)")
        print("5. Aplicar clave de sustitución conocida")
        print("6. Cambiar texto cifrado")
        print("0. Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "1":
            descifrador.probar_cesar(texto_cifrado)
        
        elif opcion == "2":
            descifrador.analisis_frecuencia(texto_cifrado)
        
        elif opcion == "3":
            sugerencia = descifrador.sugerir_sustitucion(texto_cifrado)
            resultado = descifrador.sustitucion_personalizada(texto_cifrado, sugerencia)
            print(f"\n🎯 Resultado con sugerencia automática: {resultado}")
        
        elif opcion == "4":
            clave = descifrador.descifrar_interactivo(texto_cifrado)
            if clave:
                resultado = descifrador.sustitucion_personalizada(texto_cifrado, clave)
                print(f"\n🎯 RESULTADO FINAL: {resultado}")
        
        elif opcion == "5":
            print("Introduce la clave de sustitución conocida:")
            print("Formato: A=B,C=D,E=F (separado por comas)")
            clave_str = input("Clave: ").upper()
            
            try:
                clave = {}
                for par in clave_str.split(','):
                    cifrada, real = par.split('=')
                    clave[cifrada.strip()] = real.strip()
                
                resultado = descifrador.sustitucion_personalizada(texto_cifrado, clave)
                print(f"\n🎯 RESULTADO: {resultado}")
            except:
                print("❌ Formato de clave incorrecto.")
        
        elif opcion == "6":
            texto_cifrado = input("Introduce el nuevo texto cifrado: ").strip()
            print(f"Nuevo texto: {texto_cifrado}")
        
        elif opcion == "0":
            print("¡Hasta luego! 👋")
            break
        
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    main()