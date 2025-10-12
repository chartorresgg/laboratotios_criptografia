#!/usr/bin/env python3
"""
ARITMÉTICA MODULAR - Calculadora Completa MEJORADA
===================================================
Implementación educativa de operaciones de aritmética modular,
algoritmos de Euclides, inversos multiplicativos y grupos de unidades.

Nuevas características:
- Conversión modular universal (enteros, negativos, inversos, fracciones)
- Cálculo de grupos de unidades Z_n*
- Interfaz mejorada con explicaciones paso a paso
"""

from fractions import Fraction
from math import gcd as builtin_gcd


# =============================================================================
# OPERACIONES BÁSICAS DE ARITMÉTICA MODULAR
# =============================================================================

def mod_positivo(a, m):
    """
    Calcula a mod m asegurando resultado no negativo.
    
    En Python, el operador % ya retorna valores en [0, m-1],
    pero esta función hace explícito el concepto.
    
    Parámetros:
        a: número entero
        m: módulo (debe ser > 0)
    
    Retorna:
        Resultado en el rango [0, m-1]
    
    Ejemplo:
        mod_positivo(-7, 5) = 3  (porque -7 ≡ 3 (mod 5))
    """
    if m <= 0:
        raise ValueError("El módulo debe ser positivo")
    return a % m


def suma_mod(a, b, m):
    """
    Suma modular: (a + b) mod m
    
    Calcula la suma de a y b módulo m.
    
    Parámetros:
        a, b: números enteros
        m: módulo
    
    Retorna:
        (a + b) mod m
    """
    return (a + b) % m


def resta_mod(a, b, m):
    """
    Resta modular: (a - b) mod m
    
    Calcula la resta de a y b módulo m.
    
    Parámetros:
        a, b: números enteros
        m: módulo
    
    Retorna:
        (a - b) mod m
    """
    return (a - b) % m


def mult_mod(a, b, m):
    """
    Multiplicación modular: (a × b) mod m
    
    Calcula el producto de a y b módulo m.
    
    Parámetros:
        a, b: números enteros
        m: módulo
    
    Retorna:
        (a × b) mod m
    """
    return (a * b) % m


def congruencia(a, b, m):
    """
    Verifica si a ≡ b (mod m)
    
    Dos números son congruentes módulo m si su diferencia
    es divisible por m, es decir: m | (a - b)
    
    Parámetros:
        a, b: números a comparar
        m: módulo
    
    Retorna:
        True si a ≡ b (mod m), False en caso contrario
    """
    return (a - b) % m == 0


# =============================================================================
# ALGORITMO DE EUCLIDES
# =============================================================================

def euclides(a, b):
    """
    Algoritmo de Euclides para calcular el MCD (Máximo Común Divisor).
    
    Basado en el principio: MCD(a, b) = MCD(b, a mod b)
    Se repite hasta que b = 0, entonces MCD = a
    
    Parámetros:
        a, b: números enteros
    
    Retorna:
        MCD(a, b)
    
    Ejemplo:
        euclides(48, 18)
        48 = 18 × 2 + 12
        18 = 12 × 1 + 6
        12 = 6 × 2 + 0
        MCD = 6
    """
    a, b = abs(a), abs(b)  # Trabajar con valores absolutos
    
    pasos = []
    while b != 0:
        q = a // b
        r = a % b
        pasos.append({
            'a': a,
            'b': b,
            'q': q,
            'r': r,
            'ecuacion': f"{a} = {b} × {q} + {r}"
        })
        a, b = b, r
    
    return a, pasos


def euclides_extendido(a, b):
    """
    Algoritmo de Euclides Extendido.
    
    Encuentra el MCD(a, b) y los coeficientes x, y tales que:
        a·x + b·y = MCD(a, b)
    
    Esta es la Identidad de Bézout.
    
    Parámetros:
        a, b: números enteros
    
    Retorna:
        Tupla (mcd, x, y, pasos) donde:
        - mcd: MCD(a, b)
        - x, y: coeficientes de Bézout
        - pasos: lista de pasos del algoritmo
    
    Ejemplo:
        euclides_extendido(35, 15)
        MCD = 5
        35·(1) + 15·(-2) = 5
    """
    # Guardar valores originales
    a_orig, b_orig = a, b
    
    # Trabajar con valores absolutos
    a, b = abs(a), abs(b)
    
    # Coeficientes iniciales
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    
    pasos = []
    
    while b != 0:
        q = a // b
        
        # Actualizar a, b
        a, b = b, a % b
        
        # Actualizar coeficientes
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        
        pasos.append({
            'q': q,
            'a': a,
            'x': x0,
            'y': y0
        })
    
    mcd = a
    x, y = x0, y0
    
    # Ajustar signos según valores originales
    if a_orig < 0:
        x = -x
    if b_orig < 0:
        y = -y
    
    return mcd, x, y, pasos


# =============================================================================
# INVERSO MODULAR
# =============================================================================

def inverso_mod(a, m):
    """
    Calcula el inverso modular de a módulo m.
    
    El inverso a^(-1) mod m existe si y solo si MCD(a, m) = 1.
    Cumple: a × a^(-1) ≡ 1 (mod m)
    
    Usa el Algoritmo de Euclides Extendido:
        a·x + m·y = 1
        a·x ≡ 1 (mod m)
        Por lo tanto, x es el inverso de a módulo m
    
    Parámetros:
        a: número a invertir
        m: módulo
    
    Retorna:
        a^(-1) mod m, o None si no existe
    
    Ejemplo:
        inverso_mod(3, 7) = 5
        Porque 3 × 5 = 15 ≡ 1 (mod 7)
    """
    if m <= 0:
        raise ValueError("El módulo debe ser positivo")
    
    a = a % m
    
    # Usar Euclides Extendido
    mcd, x, y, _ = euclides_extendido(a, m)
    
    if mcd != 1:
        return None  # No existe inverso
    
    # x es el inverso, asegurar que sea positivo
    return x % m


# =============================================================================
# ARITMÉTICA MODULAR CON FRACCIONES
# =============================================================================

def mod_fraccion(numerador, denominador, m):
    """
    Calcula (numerador / denominador) mod m
    
    La división modular se define como:
        (a / b) mod m = (a × b^(-1)) mod m
    
    donde b^(-1) es el inverso modular de b módulo m.
    
    Parámetros:
        numerador: numerador de la fracción
        denominador: denominador de la fracción
        m: módulo
    
    Retorna:
        Resultado de (numerador/denominador) mod m, o None si no existe
    
    Ejemplo:
        mod_fraccion(3, 4, 7)
        = (3 × 4^(-1)) mod 7
        = (3 × 2) mod 7    [porque 4 × 2 = 8 ≡ 1 (mod 7)]
        = 6
    """
    # Simplificar la fracción primero
    fraccion = Fraction(numerador, denominador)
    num = fraccion.numerator
    den = fraccion.denominator
    
    # Calcular inverso del denominador
    den_inv = inverso_mod(den, m)
    
    if den_inv is None:
        return None  # No existe inverso
    
    # Calcular (num × den^(-1)) mod m
    return (num * den_inv) % m


def suma_mod_fraccion(num1, den1, num2, den2, m):
    """
    Suma de fracciones módulo m: (num1/den1 + num2/den2) mod m
    
    Parámetros:
        num1, den1: primera fracción
        num2, den2: segunda fracción
        m: módulo
    
    Retorna:
        Resultado de la suma módulo m
    """
    # Sumar fracciones normalmente
    fraccion = Fraction(num1, den1) + Fraction(num2, den2)
    
    # Calcular módulo de la fracción resultante
    return mod_fraccion(fraccion.numerator, fraccion.denominator, m)


def resta_mod_fraccion(num1, den1, num2, den2, m):
    """
    Resta de fracciones módulo m: (num1/den1 - num2/den2) mod m
    """
    fraccion = Fraction(num1, den1) - Fraction(num2, den2)
    return mod_fraccion(fraccion.numerator, fraccion.denominator, m)


def mult_mod_fraccion(num1, den1, num2, den2, m):
    """
    Multiplicación de fracciones módulo m: (num1/den1 × num2/den2) mod m
    """
    fraccion = Fraction(num1, den1) * Fraction(num2, den2)
    return mod_fraccion(fraccion.numerator, fraccion.denominator, m)


def div_mod_fraccion(num1, den1, num2, den2, m):
    """
    División de fracciones módulo m: (num1/den1 ÷ num2/den2) mod m
    """
    fraccion = Fraction(num1, den1) / Fraction(num2, den2)
    return mod_fraccion(fraccion.numerator, fraccion.denominator, m)


# =============================================================================
# NUEVAS FUNCIONES: CONVERSIÓN MODULAR UNIVERSAL
# =============================================================================

def conversion_modular_universal(expresion, modulo):
    """
    Convierte cualquier expresión numérica a su forma módulo m.
    Detecta automáticamente el tipo: entero, negativo, inverso o fracción.
    
    Parámetros:
        expresion: string con la expresión (ej: "-3", "64", "3^-1", "14/2")
        modulo: módulo m
    
    Retorna:
        Tupla (tipo, resultado, explicacion) donde:
        - tipo: tipo de operación detectada
        - resultado: resultado numérico
        - explicacion: dict con pasos de la conversión
    """
    expresion = expresion.strip()
    
    # Detectar tipo de expresión
    if "^-1" in expresion or "^(-1)" in expresion:
        # INVERSO MULTIPLICATIVO
        return _calcular_inverso_mod(expresion, modulo)
    
    elif "/" in expresion:
        # FRACCIÓN
        return _calcular_fraccion_mod(expresion, modulo)
    
    else:
        # ENTERO (positivo o negativo)
        return _calcular_entero_mod(expresion, modulo)


def _calcular_entero_mod(expresion, m):
    """Calcula módulo de un entero (positivo o negativo)"""
    try:
        numero = int(expresion)
        resultado = numero % m
        
        explicacion = {
            'numero_original': numero,
            'es_negativo': numero < 0,
            'division': numero // m,
            'residuo': numero % m,
            'resultado': resultado
        }
        
        if numero < 0:
            # Explicar conversión de negativo
            explicacion['proceso'] = [
                f"Número negativo: {numero}",
                f"Dividir: {numero} = {m} × {numero // m} + {numero % m}",
                f"Resultado: {numero} ≡ {resultado} (mod {m})"
            ]
            tipo = "entero_negativo"
        else:
            explicacion['proceso'] = [
                f"Número positivo: {numero}",
                f"Dividir: {numero} = {m} × {numero // m} + {resultado}",
                f"Resultado: {numero} ≡ {resultado} (mod {m})"
            ]
            tipo = "entero_positivo"
        
        return tipo, resultado, explicacion
    
    except ValueError:
        raise ValueError(f"'{expresion}' no es un número válido")


def _calcular_inverso_mod(expresion, m):
    """Calcula el inverso multiplicativo"""
    # Extraer el número base
    base_str = expresion.replace("^-1", "").replace("^(-1)", "").strip()
    
    try:
        a = int(base_str)
        a = a % m  # Normalizar a rango [0, m-1]
        
        # Verificar si existe inverso
        mcd = builtin_gcd(a, m)
        
        explicacion = {
            'numero_original': int(base_str),
            'numero_normalizado': a,
            'modulo': m,
            'mcd': mcd
        }
        
        if mcd != 1:
            explicacion['existe_inverso'] = False
            explicacion['proceso'] = [
                f"Verificar: MCD({a}, {m}) = {mcd}",
                f"MCD ≠ 1, por lo tanto NO existe inverso",
                f"Los números no son coprimos"
            ]
            return "inverso_no_existe", None, explicacion
        
        # Calcular inverso usando Euclides Extendido
        inverso = inverso_mod(a, m)
        
        # Verificación
        verificacion = (a * inverso) % m
        
        explicacion['existe_inverso'] = True
        explicacion['inverso'] = inverso
        explicacion['verificacion'] = verificacion
        explicacion['proceso'] = [
            f"Buscar: {a}^(-1) mod {m}",
            f"Verificar: MCD({a}, {m}) = {mcd} ✓",
            f"Usar Algoritmo de Euclides Extendido",
            f"Resultado: {a}^(-1) ≡ {inverso} (mod {m})",
            f"Verificación: {a} × {inverso} = {a * inverso} ≡ {verificacion} (mod {m})"
        ]
        
        return "inverso_multiplicativo", inverso, explicacion
    
    except ValueError:
        raise ValueError(f"'{base_str}' no es un número válido")


def _calcular_fraccion_mod(expresion, m):
    """Calcula módulo de una fracción"""
    try:
        # Parsear fracción
        partes = expresion.split("/")
        if len(partes) != 2:
            raise ValueError("Formato de fracción inválido")
        
        numerador = int(partes[0].strip())
        denominador = int(partes[1].strip())
        
        if denominador == 0:
            raise ValueError("El denominador no puede ser cero")
        
        # Simplificar fracción
        fraccion = Fraction(numerador, denominador)
        num_simplificado = fraccion.numerator
        den_simplificado = fraccion.denominator
        
        explicacion = {
            'numerador_original': numerador,
            'denominador_original': denominador,
            'numerador_simplificado': num_simplificado,
            'denominador_simplificado': den_simplificado,
            'modulo': m
        }
        
        # Calcular inverso del denominador
        den_inv = inverso_mod(den_simplificado, m)
        
        if den_inv is None:
            mcd = builtin_gcd(den_simplificado, m)
            explicacion['existe_resultado'] = False
            explicacion['mcd_denominador'] = mcd
            explicacion['proceso'] = [
                f"Fracción: {numerador}/{denominador}",
                f"Simplificada: {num_simplificado}/{den_simplificado}",
                f"Buscar inverso de {den_simplificado} mod {m}",
                f"MCD({den_simplificado}, {m}) = {mcd} ≠ 1",
                f"NO existe inverso del denominador",
                f"No se puede calcular la fracción mod {m}"
            ]
            return "fraccion_no_existe", None, explicacion
        
        # Calcular resultado
        resultado = (num_simplificado * den_inv) % m
        
        explicacion['denominador_inverso'] = den_inv
        explicacion['resultado'] = resultado
        explicacion['existe_resultado'] = True
        explicacion['proceso'] = [
            f"Fracción: {numerador}/{denominador}",
            f"Simplificada: {num_simplificado}/{den_simplificado}",
            f"Encontrar: {den_simplificado}^(-1) mod {m} = {den_inv}",
            f"Calcular: ({num_simplificado} × {den_inv}) mod {m}",
            f"= {num_simplificado * den_inv} mod {m}",
            f"= {resultado}",
            f"Resultado: {numerador}/{denominador} ≡ {resultado} (mod {m})"
        ]
        
        return "fraccion", resultado, explicacion
    
    except ValueError as e:
        raise ValueError(f"Error al procesar fracción: {str(e)}")


# =============================================================================
# NUEVAS FUNCIONES: GRUPO DE UNIDADES
# =============================================================================

def grupo_unidades(n):
    """
    Calcula el grupo de unidades Z_n* (elementos invertibles de Z_n).
    
    Z_n* = {a ∈ Z_n : MCD(a, n) = 1}
    
    Para cada elemento del grupo, calcula su inverso multiplicativo.
    
    Parámetros:
        n: módulo entero positivo
    
    Retorna:
        Diccionario con:
        - 'grupo': lista de elementos en Z_n*
        - 'inversos': diccionario {elemento: inverso}
        - 'tamaño': |Z_n*| (función φ de Euler)
        - 'tabla': tabla completa de multiplicación modular
    
    Ejemplo:
        grupo_unidades(12) = {
            'grupo': [1, 5, 7, 11],
            'inversos': {1: 1, 5: 5, 7: 7, 11: 11},
            'tamaño': 4,
            ...
        }
    """
    if n <= 0:
        raise ValueError("n debe ser un entero positivo")
    
    # Encontrar todos los elementos coprimos con n
    grupo = []
    inversos = {}
    
    for a in range(1, n):
        if builtin_gcd(a, n) == 1:
            grupo.append(a)
            # Calcular su inverso
            inv = inverso_mod(a, n)
            inversos[a] = inv
    
    # Calcular tabla de multiplicación
    tabla_mult = {}
    for a in grupo:
        tabla_mult[a] = {}
        for b in grupo:
            tabla_mult[a][b] = (a * b) % n
    
    # Verificar propiedad de grupo
    es_grupo = verificar_propiedades_grupo(grupo, n)
    
    resultado = {
        'n': n,
        'grupo': grupo,
        'inversos': inversos,
        'tamaño': len(grupo),
        'tabla_multiplicacion': tabla_mult,
        'propiedades': es_grupo
    }
    
    return resultado


def verificar_propiedades_grupo(elementos, n):
    """
    Verifica las propiedades de grupo para Z_n*
    
    1. Cerradura: a · b ∈ Z_n* para todo a, b ∈ Z_n*
    2. Identidad: existe 1 ∈ Z_n*
    3. Inversos: para todo a ∈ Z_n*, existe a^(-1) ∈ Z_n*
    4. Asociatividad: (a · b) · c = a · (b · c)
    """
    propiedades = {
        'cerradura': True,
        'identidad': 1 in elementos,
        'inversos': True,
        'asociatividad': True
    }
    
    # Verificar cerradura
    for a in elementos:
        for b in elementos:
            if (a * b) % n not in elementos:
                propiedades['cerradura'] = False
                break
        if not propiedades['cerradura']:
            break
    
    # Verificar existencia de inversos
    for a in elementos:
        tiene_inverso = False
        for b in elementos:
            if (a * b) % n == 1:
                tiene_inverso = True
                break
        if not tiene_inverso:
            propiedades['inversos'] = False
            break
    
    return propiedades


# =============================================================================
# FUNCIONES DE VISUALIZACIÓN MEJORADAS
# =============================================================================

def mostrar_conversion_modular(expresion, modulo):
    """Muestra el proceso de conversión modular con explicación detallada"""
    print("\n" + "="*70)
    print("CONVERSIÓN MODULAR UNIVERSAL")
    print("="*70)
    print(f"Expresión: {expresion}")
    print(f"Módulo: {modulo}")
    print("─"*70)
    
    try:
        tipo, resultado, explicacion = conversion_modular_universal(expresion, modulo)
        
        print(f"\nTipo detectado: {tipo.replace('_', ' ').title()}")
        print("\nProceso:")
        
        for paso in explicacion['proceso']:
            print(f"  {paso}")
        
        print("\n" + "─"*70)
        
        if resultado is not None:
            print(f"✓ RESULTADO: {expresion} ≡ {resultado} (mod {modulo})")
        else:
            print(f"✗ NO EXISTE RESULTADO")
        
        # Mostrar información adicional según el tipo
        if tipo == "inverso_multiplicativo" and resultado is not None:
            a = explicacion['numero_normalizado']
            print(f"\nVerificación: {a} × {resultado} = {a * resultado} ≡ {(a * resultado) % modulo} (mod {modulo})")
        
        elif tipo == "fraccion" and resultado is not None:
            print(f"\nInverso del denominador: {explicacion['denominador_simplificado']}^(-1) ≡ {explicacion['denominador_inverso']} (mod {modulo})")
        
    except ValueError as e:
        print(f"\n❌ ERROR: {str(e)}")
    
    print("="*70)


def mostrar_grupo_unidades(n):
    """Muestra el grupo de unidades Z_n* con explicación detallada"""
    print("\n" + "="*70)
    print(f"GRUPO DE UNIDADES Z_{n}*")
    print("="*70)
    print(f"Conjunto completo: Z_{n} = {{{', '.join(map(str, range(n)))}}}")
    print("─"*70)
    
    resultado = grupo_unidades(n)
    
    print(f"\n📌 Elementos coprimos con {n} (grupo de unidades):")
    print(f"   Z_{n}* = {{{', '.join(map(str, resultado['grupo']))}}}")
    print(f"\n📊 Tamaño del grupo: |Z_{n}*| = {resultado['tamaño']} (Función φ de Euler)")
    
    print("\n🔄 INVERSOS MULTIPLICATIVOS:")
    print("─"*70)
    print(f"{'Elemento':>10} │ {'Inverso':>10} │ {'Verificación':>25}")
    print("─"*70)
    
    for elemento in sorted(resultado['grupo']):
        inverso = resultado['inversos'][elemento]
        verificacion = f"{elemento} × {inverso} ≡ {(elemento * inverso) % n} (mod {n})"
        print(f"{elemento:>10} │ {inverso:>10} │ {verificacion:>25}")
    
    print("─"*70)
    
    # Mostrar propiedades de grupo
    print("\n✓ PROPIEDADES DE GRUPO:")
    props = resultado['propiedades']
    print(f"  • Cerradura:     {'✓' if props['cerradura'] else '✗'} - El producto de elementos del grupo está en el grupo")
    print(f"  • Identidad:     {'✓' if props['identidad'] else '✗'} - Contiene el elemento neutro (1)")
    print(f"  • Inversos:      {'✓' if props['inversos'] else '✗'} - Cada elemento tiene inverso")
    print(f"  • Asociatividad: {'✓' if props['asociatividad'] else '✗'} - La multiplicación es asociativa")
    
    # Mostrar tabla de multiplicación (solo para grupos pequeños)
    if len(resultado['grupo']) <= 12:
        print("\n📋 TABLA DE MULTIPLICACIÓN MOD " + str(n) + ":")
        print("─"*70)
        
        # Encabezado
        print("   ×  │", end="")
        for b in resultado['grupo']:
            print(f"{b:>4}", end="")
        print("\n" + "─"*70)
        
        # Filas
        for a in resultado['grupo']:
            print(f"{a:>4}  │", end="")
            for b in resultado['grupo']:
                producto = resultado['tabla_multiplicacion'][a][b]
                print(f"{producto:>4}", end="")
            print()
    
    print("="*70)


def mostrar_operacion_basica(a, b, m, operacion):
    """Muestra el resultado de una operación básica."""
    print("\n" + "="*70)
    print(f"OPERACIÓN: {operacion}")
    print("="*70)
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"m = {m}")
    
    if operacion == "Suma":
        resultado = suma_mod(a, b, m)
        print(f"\nResultado: ({a} + {b}) mod {m} = {resultado}")
    elif operacion == "Resta":
        resultado = resta_mod(a, b, m)
        print(f"\nResultado: ({a} - {b}) mod {m} = {resultado}")
    elif operacion == "Multiplicación":
        resultado = mult_mod(a, b, m)
        print(f"\nResultado: ({a} × {b}) mod {m} = {resultado}")
    elif operacion == "Congruencia":
        resultado = congruencia(a, b, m)
        signo = "≡" if resultado else "≢"
        print(f"\nResultado: {a} {signo} {b} (mod {m})")
        print(f"Verificación: ({a} - {b}) mod {m} = {(a-b) % m}")


def mostrar_euclides(a, b):
    """Muestra el proceso del Algoritmo de Euclides."""
    print("\n" + "="*70)
    print("ALGORITMO DE EUCLIDES")
    print("="*70)
    print(f"Calcular MCD({a}, {b})")
    print("\nPasos:")
    print("-"*70)
    
    mcd, pasos = euclides(a, b)
    
    for i, paso in enumerate(pasos, 1):
        print(f"Paso {i}: {paso['ecuacion']}")
    
    print("-"*70)
    print(f"\n✓ MCD({a}, {b}) = {mcd}")
    print("="*70)


def mostrar_euclides_extendido(a, b):
    """Muestra el proceso del Algoritmo de Euclides Extendido."""
    print("\n" + "="*70)
    print("ALGORITMO DE EUCLIDES EXTENDIDO")
    print("="*70)
    print(f"Calcular MCD({a}, {b}) y coeficientes de Bézout")
    
    mcd, x, y, pasos = euclides_extendido(a, b)
    
    print("\nPasos del algoritmo:")
    print("-"*70)
    for i, paso in enumerate(pasos, 1):
        if i <= 5 or i > len(pasos) - 2:
            print(f"Paso {i}: q={paso['q']}, a={paso['a']}, x={paso['x']}, y={paso['y']}")
        elif i == 6:
            print("   ...")
    print("-"*70)
    
    print(f"\n✓ MCD({a}, {b}) = {mcd}")
    print(f"\nIdentidad de Bézout:")
    print(f"  {a} × ({x}) + {b} × ({y}) = {mcd}")
    print(f"\nVerificación: {a*x + b*y} = {mcd}")
    print("="*70)


def mostrar_inverso(a, m):
    """Muestra el cálculo del inverso modular."""
    print("\n" + "="*70)
    print("INVERSO MODULAR")
    print("="*70)
    print(f"Calcular {a}^(-1) mod {m}")
    
    # Verificar si son coprimos
    mcd = builtin_gcd(abs(a), m)
    print(f"\nVerificación: MCD({a}, {m}) = {mcd}")
    
    if mcd != 1:
        print(f"\n❌ No existe inverso porque MCD({a}, {m}) ≠ 1")
        print("="*70)
        return
    
    inverso = inverso_mod(a, m)
    print(f"\n✓ {a}^(-1) mod {m} = {inverso}")
    
    # Verificación
    verificacion = (a * inverso) % m
    print(f"\nVerificación: {a} × {inverso} mod {m} = {verificacion}")
    print("="*70)


def mostrar_mod_fraccion(num, den, m):
    """Muestra el cálculo de módulo de una fracción."""
    print("\n" + "="*70)
    print("MÓDULO DE FRACCIÓN")
    print("="*70)
    print(f"Calcular ({num}/{den}) mod {m}")
    
    # Simplificar fracción
    fraccion = Fraction(num, den)
    print(f"\nFracción simplificada: {fraccion.numerator}/{fraccion.denominator}")
    
    resultado = mod_fraccion(fraccion.numerator, fraccion.denominator, m)
    
    if resultado is None:
        print(f"\n❌ No se puede calcular (denominador no tiene inverso mod {m})")
    else:
        den_inv = inverso_mod(fraccion.denominator, m)
        print(f"\nPasos:")
        print(f"  1. Inverso de {fraccion.denominator} mod {m} = {den_inv}")
        print(f"  2. ({fraccion.numerator} × {den_inv}) mod {m} = {resultado}")
        print(f"\n✓ Resultado: ({num}/{den}) mod {m} = {resultado}")
    
    print("="*70)


# =============================================================================
# MENÚ PRINCIPAL MEJORADO
# =============================================================================

def menu_principal():
    """Menú interactivo principal."""
    print("\n" + "="*70)
    print(" "*15 + "ARITMÉTICA MODULAR - VERSIÓN MEJORADA")
    print("="*70)
    print("\nCalculadora completa con conversión universal y grupos de unidades")
    
    while True:
        print("\n" + "┌─── MENÚ PRINCIPAL ───────────────────────┐")
        print("│ 1. Conversión Modular Universal        │")
        print("│ 2. Grupo de Unidades Z_n*              │")
        print("│ 3. Operaciones básicas (enteros)       │")
        print("│ 4. Algoritmo de Euclides               │")
        print("│ 5. Algoritmo de Euclides Extendido     │")
        print("│ 6. Inverso Modular                     │")
        print("│ 7. Operaciones con fracciones          │")
        print("│ 8. Módulo de fracción                  │")
        print("│ 9. Casos de uso de ejemplo             │")
        print("│ 10. Salir                              │")
        print("└──────────────────────────────────────────┘")
        
        opcion = input("\nSeleccione una opción [1-10]: ").strip()
        
        if opcion == '1':
            menu_conversion_universal()
        elif opcion == '2':
            menu_grupo_unidades()
        elif opcion == '3':
            menu_operaciones_basicas()
        elif opcion == '4':
            menu_euclides()
        elif opcion == '5':
            menu_euclides_extendido()
        elif opcion == '6':
            menu_inverso()
        elif opcion == '7':
            menu_fracciones()
        elif opcion == '8':
            menu_mod_fraccion()
        elif opcion == '9':
            mostrar_ejemplos()
        elif opcion == '10':
            print("\n¡Hasta pronto! 👋\n")
            break
        else:
            print("\n❌ Opción inválida. Intente nuevamente.")


def menu_conversion_universal():
    """Menú para conversión modular universal"""
    print("\n" + "─"*70)
    print("CONVERSIÓN MODULAR UNIVERSAL")
    print("─"*70)
    print("\nEsta herramienta convierte automáticamente:")
    print("  • Enteros positivos: 64 mod 24")
    print("  • Enteros negativos: -3 mod 2")
    print("  • Inversos: 3^-1 mod 7")
    print("  • Fracciones: 14/2 mod 9")
    print("─"*70)
    
    try:
        expresion = input("\nIngrese la expresión (ej: '64', '-3', '3^-1', '14/2'): ").strip()
        modulo = int(input("Ingrese el módulo: "))
        
        if modulo <= 0:
            print("❌ El módulo debe ser positivo")
            return
        
        mostrar_conversion_modular(expresion, modulo)
    
    except ValueError as e:
        print(f"❌ Entrada inválida: {str(e)}")


def menu_grupo_unidades():
    """Menú para calcular grupos de unidades"""
    print("\n" + "─"*70)
    print("GRUPO DE UNIDADES Z_n*")
    print("─"*70)
    print("\nCalcular el grupo de unidades (elementos invertibles) de Z_n")
    print("El grupo Z_n* contiene todos los elementos coprimos con n")
    print("─"*70)
    
    try:
        entrada = input("\nIngrese n (ej: 12 para Z_12): ").strip()
        
        # Permitir entrada como "Z12" o "12"
        if entrada.upper().startswith('Z'):
            n = int(entrada[1:])
        else:
            n = int(entrada)
        
        if n <= 0:
            print("❌ n debe ser un entero positivo")
            return
        
        mostrar_grupo_unidades(n)
    
    except ValueError:
        print("❌ Entrada inválida. Use un número entero positivo.")


def menu_operaciones_basicas():
    """Submenú para operaciones básicas."""
    print("\n" + "─"*70)
    print("OPERACIONES BÁSICAS")
    print("─"*70)
    
    try:
        a = int(input("Ingrese el primer número (a): "))
        b = int(input("Ingrese el segundo número (b): "))
        m = int(input("Ingrese el módulo (m): "))
        
        if m <= 0:
            print("❌ El módulo debe ser positivo")
            return
        
        print("\n¿Qué operación desea realizar?")
        print("1. Suma: (a + b) mod m")
        print("2. Resta: (a - b) mod m")
        print("3. Multiplicación: (a × b) mod m")
        print("4. Congruencia: ¿a ≡ b (mod m)?")
        
        op = input("\nSeleccione [1-4]: ").strip()
        
        if op == '1':
            mostrar_operacion_basica(a, b, m, "Suma")
        elif op == '2':
            mostrar_operacion_basica(a, b, m, "Resta")
        elif op == '3':
            mostrar_operacion_basica(a, b, m, "Multiplicación")
        elif op == '4':
            mostrar_operacion_basica(a, b, m, "Congruencia")
        else:
            print("❌ Opción inválida")
    
    except ValueError:
        print("❌ Entrada inválida. Use números enteros.")


def menu_euclides():
    """Submenú para Algoritmo de Euclides."""
    print("\n" + "─"*70)
    print("ALGORITMO DE EUCLIDES")
    print("─"*70)
    
    try:
        a = int(input("Ingrese el primer número: "))
        b = int(input("Ingrese el segundo número: "))
        
        mostrar_euclides(a, b)
    
    except ValueError:
        print("❌ Entrada inválida. Use números enteros.")


def menu_euclides_extendido():
    """Submenú para Algoritmo de Euclides Extendido."""
    print("\n" + "─"*70)
    print("ALGORITMO DE EUCLIDES EXTENDIDO")
    print("─"*70)
    
    try:
        a = int(input("Ingrese el primer número: "))
        b = int(input("Ingrese el segundo número: "))
        
        mostrar_euclides_extendido(a, b)
    
    except ValueError:
        print("❌ Entrada inválida. Use números enteros.")


def menu_inverso():
    """Submenú para Inverso Modular."""
    print("\n" + "─"*70)
    print("INVERSO MODULAR")
    print("─"*70)
    
    try:
        a = int(input("Ingrese el número (a): "))
        m = int(input("Ingrese el módulo (m): "))
        
        if m <= 0:
            print("❌ El módulo debe ser positivo")
            return
        
        mostrar_inverso(a, m)
    
    except ValueError:
        print("❌ Entrada inválida. Use números enteros.")


def menu_fracciones():
    """Submenú para operaciones con fracciones."""
    print("\n" + "─"*70)
    print("OPERACIONES CON FRACCIONES")
    print("─"*70)
    
    try:
        print("\nPrimera fracción:")
        num1 = int(input("  Numerador: "))
        den1 = int(input("  Denominador: "))
        
        print("\nSegunda fracción:")
        num2 = int(input("  Numerador: "))
        den2 = int(input("  Denominador: "))
        
        m = int(input("\nMódulo (m): "))
        
        if m <= 0:
            print("❌ El módulo debe ser positivo")
            return
        
        print("\n¿Qué operación desea realizar?")
        print("1. Suma")
        print("2. Resta")
        print("3. Multiplicación")
        print("4. División")
        
        op = input("\nSeleccione [1-4]: ").strip()
        
        print("\n" + "="*70)
        
        if op == '1':
            resultado = suma_mod_fraccion(num1, den1, num2, den2, m)
            print(f"({num1}/{den1} + {num2}/{den2}) mod {m} = {resultado}")
        elif op == '2':
            resultado = resta_mod_fraccion(num1, den1, num2, den2, m)
            print(f"({num1}/{den1} - {num2}/{den2}) mod {m} = {resultado}")
        elif op == '3':
            resultado = mult_mod_fraccion(num1, den1, num2, den2, m)
            print(f"({num1}/{den1} × {num2}/{den2}) mod {m} = {resultado}")
        elif op == '4':
            resultado = div_mod_fraccion(num1, den1, num2, den2, m)
            print(f"({num1}/{den1} ÷ {num2}/{den2}) mod {m} = {resultado}")
        
        print("="*70)
    
    except ValueError:
        print("❌ Entrada inválida.")
    except ZeroDivisionError:
        print("❌ El denominador no puede ser cero.")


def menu_mod_fraccion():
    """Submenú para módulo de fracción."""
    print("\n" + "─"*70)
    print("MÓDULO DE FRACCIÓN")
    print("─"*70)
    
    try:
        num = int(input("Numerador: "))
        den = int(input("Denominador: "))
        m = int(input("Módulo (m): "))
        
        if m <= 0:
            print("❌ El módulo debe ser positivo")
            return
        
        mostrar_mod_fraccion(num, den, m)
    
    except ValueError:
        print("❌ Entrada inválida.")
    except ZeroDivisionError:
        print("❌ El denominador no puede ser cero.")


def mostrar_ejemplos():
    """Muestra casos de uso de ejemplo."""
    print("\n" + "="*70)
    print(" "*20 + "CASOS DE USO - VERSIÓN MEJORADA")
    print("="*70)
    
    ejemplos = [
        {
            'titulo': 'Ejemplo 1: Conversión - Entero Negativo',
            'funcion': lambda: mostrar_conversion_modular("-3", 2)
        },
        {
            'titulo': 'Ejemplo 2: Conversión - Entero Positivo',
            'funcion': lambda: mostrar_conversion_modular("64", 24)
        },
        {
            'titulo': 'Ejemplo 3: Conversión - Inverso Multiplicativo',
            'funcion': lambda: mostrar_conversion_modular("3^-1", 7)
        },
        {
            'titulo': 'Ejemplo 4: Conversión - Fracción',
            'funcion': lambda: mostrar_conversion_modular("14/2", 9)
        },
        {
            'titulo': 'Ejemplo 5: Grupo de Unidades Z_12*',
            'funcion': lambda: mostrar_grupo_unidades(12)
        },
        {
            'titulo': 'Ejemplo 6: Grupo de Unidades Z_10*',
            'funcion': lambda: mostrar_grupo_unidades(10)
        }
    ]
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n{ejemplo['titulo']}")
        ejemplo['funcion']()
        
        if i < len(ejemplos):
            input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    menu_principal()