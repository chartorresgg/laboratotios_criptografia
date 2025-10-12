# Casos de Prueba - Sistemas Criptográficos

**Asignatura:** Criptografía  
**Fecha:** Octubre 2025  
**Objetivo:** Validar la correcta implementación de todos los sistemas criptográficos

---

## Tabla de Contenidos
1. [Aritmética Modular](#1-aritmética-modular)
2. [Cifrado César](#2-cifrado-césar)
3. [Cifrado Afín](#3-cifrado-afín)
4. [Cifrado Vigenère](#4-cifrado-vigenère)
5. [Cifrado de Sustitución](#5-cifrado-de-sustitución)
6. [Cifrado de Hill](#6-cifrado-de-hill)
7. [Diffie-Hellman](#7-diffie-hellman)
8. [ElGamal](#8-elgamal)
9. [RSA](#9-rsa)

---

## 1. Aritmética Modular

### Caso 1.1: Conversión de Entero Negativo
```
Entrada: -3 mod 2
Resultado Esperado: 1
Proceso:
  -3 = 2 × (-2) + 1
  -3 ≡ 1 (mod 2)
```

### Caso 1.2: Conversión de Entero Positivo
```
Entrada: 64 mod 24
Resultado Esperado: 16
Proceso:
  64 = 24 × 2 + 16
  64 ≡ 16 (mod 24)
```

### Caso 1.3: Inverso Multiplicativo
```
Entrada: 3^-1 mod 7
Resultado Esperado: 5
Verificación: 3 × 5 = 15 ≡ 1 (mod 7)
```

### Caso 1.4: Fracción Modular
```
Entrada: 14/2 mod 9
Resultado Esperado: 7
Proceso:
  14/2 = 7
  7 mod 9 = 7
```

### Caso 1.5: Grupo de Unidades Z₁₂*
```
Entrada: n = 12
Resultado Esperado: {1, 5, 7, 11}
Tamaño: 4 (función φ de Euler)
Inversos:
  1⁻¹ = 1
  5⁻¹ = 5
  7⁻¹ = 7
  11⁻¹ = 11
```

---

## 2. Cifrado César

### Caso 2.1: Cifrado Básico
```
Mensaje: HELLO
Clave: 3
Cifrado Esperado: KHOOR
Proceso:
  H (7) → K (10)
  E (4) → H (7)
  L (11) → O (14)
  L (11) → O (14)
  O (14) → R (17)
```

### Caso 2.2: Cifrado con Rotación Completa
```
Mensaje: XYZ
Clave: 3
Cifrado Esperado: ABC
Proceso:
  X (23) → (23+3) mod 26 = 0 → A
  Y (24) → (24+3) mod 26 = 1 → B
  Z (25) → (25+3) mod 26 = 2 → C
```

### Caso 2.3: Descifrado
```
Mensaje Cifrado: KHOOR
Clave: 3
Descifrado Esperado: HELLO
```

---

## 3. Cifrado Afín

### Caso 3.1: Cifrado Básico
```
Mensaje: HELLO
Claves: a = 5, b = 8
Cifrado Esperado: RCLLA
Proceso:
  H (7): (5×7 + 8) mod 26 = 43 mod 26 = 17 → R
  E (4): (5×4 + 8) mod 26 = 28 mod 26 = 2 → C
  L (11): (5×11 + 8) mod 26 = 63 mod 26 = 11 → L
  L (11): (5×11 + 8) mod 26 = 63 mod 26 = 11 → L
  O (14): (5×14 + 8) mod 26 = 78 mod 26 = 0 → A
```

### Caso 3.2: Validación de Clave
```
Clave válida: a = 5
  gcd(5, 26) = 1 ✓
  Inverso: 5⁻¹ mod 26 = 21
  Verificación: (5 × 21) mod 26 = 105 mod 26 = 1 ✓
```

### Caso 3.3: Clave Inválida
```
Clave inválida: a = 2
  gcd(2, 26) = 2 ≠ 1 ✗
  No tiene inverso modular
```

### Caso 3.4: Descifrado
```
Mensaje Cifrado: RCLLA
Claves: a = 5, b = 8
Descifrado Esperado: HELLO
a⁻¹ = 21
Fórmula: M = 21 × (C - 8) mod 26
```

---

## 4. Cifrado Vigenère

### Caso 4.1: Ejemplo Clásico
```
Mensaje: ATTACKATDAWN
Clave: LEMON
Cifrado Esperado: LXFOPVEFRNHR

Clave extendida: LEMONLEMONLE

Proceso por letras:
  A (0) + L (11) = 11 → L
  T (19) + E (4) = 23 → X
  T (19) + M (12) = 31 mod 26 = 5 → F
  A (0) + O (14) = 14 → O
  C (2) + N (13) = 15 → P
  K (10) + L (11) = 21 → V
  ...
```

### Caso 4.2: Mensaje Corto
```
Mensaje: HELLO
Clave: KEY
Cifrado Esperado: RIJVS

Clave extendida: KEYKE

Proceso:
  H (7) + K (10) = 17 → R
  E (4) + E (4) = 8 → I
  L (11) + Y (24) = 35 mod 26 = 9 → J
  L (11) + K (10) = 21 → V
  O (14) + E (4) = 18 → S
```

### Caso 4.3: Descifrado
```
Mensaje Cifrado: RIJVS
Clave: KEY
Descifrado Esperado: HELLO
Fórmula: M[i] = (C[i] - K[i]) mod 26
```

---

## 5. Cifrado de Sustitución

### Caso 5.1: Sustitución Simple
```
Mensaje: HELLO
Clave: QWERTYUIOPASDFGHJKLZXCVBNM

Alfabeto normal: ABCDEFGHIJKLMNOPQRSTUVWXYZ
Clave:           QWERTYUIOPASDFGHJKLZXCVBNM

Cifrado Esperado: ITSSG

Proceso:
  H → I (H es la 8ª letra, 8ª en clave es I)
  E → T (E es la 5ª letra, 5ª en clave es T)
  L → S (L es la 12ª letra, 12ª en clave es S)
  L → S
  O → G (O es la 15ª letra, 15ª en clave es G)
```

### Caso 5.2: Alfabeto Invertido
```
Mensaje: HELLO
Clave: ZYXWVUTSRQPONMLKJIHGFEDCBA
Cifrado Esperado: SVOOL
```

### Caso 5.3: Descifrado
```
Mensaje Cifrado: ITSSG
Clave: QWERTYUIOPASDFGHJKLZXCVBNM
Descifrado Esperado: HELLO
```

---

## 6. Cifrado de Hill

### Caso 6.1: Matriz 2×2 Clásica
```
Mensaje: HI
Matriz Clave: [[7, 1], [2, 1]]
Cifrado Esperado: FW

Proceso:
│ 7  1 │   │ 7  │     │ 50 │     │ 24 │
│ 2  1 │ × │ 8  │  =  │ 22 │ mod │ 22 │ (mod 26)

H (7) → F (5)... error en ejemplo
Correcto: 
│ 7  1 │   │ 7  │     │ 57 │     │ 5  │
│ 2  1 │ × │ 8  │  =  │ 22 │ mod │ 22 │ (mod 26)

Resultado: FW
```

### Caso 6.2: Validación de Matriz
```
Matriz: [[7, 1], [2, 1]]
Determinante: 7×1 - 1×2 = 5
det mod 26 = 5
gcd(5, 26) = 1 ✓
Es válida para Hill
```

### Caso 6.3: Cálculo de Matriz Inversa
```
Matriz: [[7, 1], [2, 1]]
det = 5
det⁻¹ mod 26 = 21

Matriz de cofactores: [[1, -2], [-1, 7]]
Adjunta (transpuesta): [[1, -1], [-2, 7]]
Inversa = 21 × [[1, -1], [-2, 7]] mod 26
       = [[21, -21], [-42, 147]] mod 26
       = [[21, 5], [10, 17]]

Verificación:
[[7, 1], [2, 1]] × [[21, 5], [10, 17]] mod 26 = [[1, 0], [0, 1]] ✓
```

### Caso 6.4: Descifrado
```
Mensaje Cifrado: FW
Matriz Clave: [[7, 1], [2, 1]]
Matriz Inversa: [[21, 5], [10, 17]]
Descifrado Esperado: HI
```

---

## 7. Diffie-Hellman

### Caso 7.1: Intercambio Básico
```
Parámetros Públicos:
  p = 23 (primo)
  g = 5 (generador)

Alice:
  Clave privada: a = 6
  Clave pública: A = 5⁶ mod 23 = 8

Bob:
  Clave privada: b = 15
  Clave pública: B = 5¹⁵ mod 23 = 19

Secreto Compartido:
  Alice calcula: s = 19⁶ mod 23 = 2
  Bob calcula: s = 8¹⁵ mod 23 = 2
  
✓ Ambos obtienen el mismo secreto: 2
```

### Caso 7.2: Verificación Matemática
```
Verificar que g^(ab) mod p es igual desde ambos lados:
  g^(ab) = 5^(6×15) = 5^90 mod 23
  
Desde Alice: (g^b)^a = 19⁶ mod 23 = 2
Desde Bob: (g^a)^b = 8¹⁵ mod 23 = 2
✓ Coinciden
```

---

## 8. ElGamal

### Caso 8.1: Generación de Claves
```
Parámetros:
  p = 23 (primo)
  g = 5 (generador)
  x = 6 (clave privada)

Clave Pública:
  h = g^x mod p = 5⁶ mod 23 = 8

Claves Completas:
  Pública: (p=23, g=5, h=8)
  Privada: x=6
```

### Caso 8.2: Cifrado de Letra
```
Mensaje: H (7)
Clave Pública: (23, 5, 8)
k aleatorio: k = 3

Cifrado:
  c₁ = g^k mod p = 5³ mod 23 = 10
  s = h^k mod p = 8³ mod 23 = 6
  c₂ = (m × s) mod p = (7 × 6) mod 23 = 42 mod 23 = 19

Resultado: (c₁=10, c₂=19)
```

### Caso 8.3: Descifrado
```
Mensaje Cifrado: (c₁=10, c₂=19)
Clave Privada: x=6
Módulo: p=23

Descifrado:
  s = c₁^x mod p = 10⁶ mod 23 = 6
  s⁻¹ mod 23 = 6⁻¹ mod 23 = 4
  (verificar: 6 × 4 = 24 ≡ 1 mod 23 ✓)
  
  m = (c₂ × s⁻¹) mod p = (19 × 4) mod 23 = 76 mod 23 = 7

Resultado: 7 → H ✓
```

---

## 9. RSA

### Caso 9.1: Ejemplo Clásico
```
Claves:
  p = 61, q = 53
  n = p × q = 3233
  φ(n) = (p-1)(q-1) = 60 × 52 = 3120
  e = 17
  d = e⁻¹ mod φ(n) = 2753
  (verificar: 17 × 2753 = 46801 = 15 × 3120 + 1 ✓)

Mensaje: HELLO
Representación numérica: 0704111114
```

### Caso 9.2: División en Bloques
```
Mensaje numérico: 0704111114
n = 3233

Bloques (cada bloque < 3233):
  Bloque 1: 0704 (4 dígitos, 2 letras)
  Bloque 2: 1111 (4 dígitos, 2 letras)
  Bloque 3: 14 (2 dígitos, 1 letra)
```

### Caso 9.3: Cifrado
```
Bloque 1: M = 704
  C = 704¹⁷ mod 3233 = 2676

Bloque 2: M = 1111
  C = 1111¹⁷ mod 3233 = 2927

Bloque 3: M = 14
  C = 14¹⁷ mod 3233 = 542

Mensaje Cifrado: [2676, 2927, 542]
```

### Caso 9.4: Descifrado
```
Bloque 1: C = 2676
  M = 2676²⁷⁵³ mod 3233 = 704

Bloque 2: C = 2927
  M = 2927²⁷⁵³ mod 3233 = 1111

Bloque 3: C = 542
  M = 542²⁷⁵³ mod 3233 = 14

Reconstrucción:
  704 → 0704 (2 letras)
  1111 → 1111 (2 letras)
  14 → 14 (1 letra)
  
Cadena numérica: 0704111114
Mensaje: HELLO ✓
```

---

## Resumen de Validación

| Cifrado | Caso de Prueba | Estado |
|---------|---------------|---------|
| Aritmética Modular | -3 mod 2 = 1 | ✓ |
| César | HELLO + 3 = KHOOR | ✓ |
| Afín | HELLO (5,8) = RCLLA | ✓ |
| Vigenère | HELLO + KEY = RIJVS | ✓ |
| Sustitución | HELLO → ITSSG | ✓ |
| Hill | HI [[7,1],[2,1]] = FW | ✓ |
| Diffie-Hellman | Secreto = 2 | ✓ |
| ElGamal | H → (10, 19) | ✓ |
| RSA | HELLO → [2676, 2927, 542] | ✓ |

---

## Notas de Implementación

### Validaciones Críticas
1. **Aritmética Modular**: Verificar operaciones con negativos
2. **Afín**: Validar que gcd(a, 26) = 1
3. **Hill**: Verificar que det(K) sea coprimo con 26
4. **RSA**: Validar primalidad de p y q

### Casos Límite
- Mensajes con longitud 1
- Mensajes muy largos (>1000 caracteres)
- Claves en el límite del rango válido
- Caracteres especiales (deben ignorarse)

---

**Fin del Documento**