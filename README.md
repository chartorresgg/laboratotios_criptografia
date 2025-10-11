# 🔐 Laboratorios de Criptografía

Repositorio de implementaciones educativas de algoritmos criptográficos clásicos, simétricos y asimétricos.

## 📁 Estructura del Proyecto

```
laboratorios_criptografia/
│
├── README.md
├── requirements.txt
│
├── 01_cifrados_clasicos/
│   ├── cesar.py
│   ├── vigenere.py
│   ├── hill.py
│   ├── playfair.py
│   ├── notebooks/
│   │   ├── lab01_cesar_vigenere.ipynb
│   │   └── lab01_hill_playfair.ipynb
│   └── tests/
│       └── test_clasicos.py
│
├── 02_cifrados_simetricos/
│   ├── des.py
│   ├── aes.py
│   ├── rc4.py
│   ├── notebooks/
│   │   ├── lab02_des.ipynb
│   │   ├── lab03_aes.ipynb
│   │   └── lab04_rc4.ipynb
│   └── tests/
│       └── test_simetricos.py
│
├── 03_cifrados_asimetricos/
│   ├── rsa.py                    ← Script interactivo RSA
│   ├── diffie_hellman.py
│   ├── elgamal.py
│   ├── ecc.py
│   ├── notebooks/
│   │   ├── lab05_rsa.ipynb       ← Notebook completo RSA
│   │   ├── lab06_diffie_hellman.ipynb
│   │   └── lab07_elgamal.ipynb
│   └── tests/
│       └── test_asimetricos.py
│
├── 04_funciones_hash/
│   ├── md5_custom.py
│   ├── sha_custom.py
│   ├── notebooks/
│   │   └── lab08_hash_functions.ipynb
│   └── tests/
│       └── test_hash.py
│
├── 05_firmas_digitales/
│   ├── rsa_signature.py
│   ├── dsa.py
│   ├── notebooks/
│   │   └── lab09_digital_signatures.ipynb
│   └── tests/
│       └── test_signatures.py
│
├── 06_protocolos/
│   ├── ssl_tls_demo.py
│   ├── pki_demo.py
│   ├── notebooks/
│   │   └── lab10_protocolos.ipynb
│   └── tests/
│       └── test_protocolos.py
│
├── utils/
│   ├── __init__.py
│   ├── math_utils.py      ← Funciones matemáticas comunes
│   ├── conversion.py      ← Conversiones de formato
│   └── visualization.py   ← Gráficos y diagramas
│
└── docs/
    ├── teoria_rsa.md
    ├── teoria_aes.md
    └── referencias.md
```

## 🚀 Inicio Rápido

### Instalación

```bash
git clone https://github.com/tu-usuario/laboratorios_criptografia.git
cd laboratorios_criptografia
pip install -r requirements.txt
```

### Ejecutar Scripts Python

```bash
# RSA interactivo con menú
python 03_cifrados_asimetricos/rsa.py

# Otros cifrados
python 01_cifrados_clasicos/cesar.py
python 02_cifrados_simetricos/aes.py
```

### Ejecutar Jupyter Notebooks

```bash
# Iniciar Jupyter
jupyter notebook

# O abrir directamente un laboratorio específico
jupyter notebook 03_cifrados_asimetricos/notebooks/lab05_rsa.ipynb
```

## 📚 Contenido de los Laboratorios

### 📖 Laboratorio 1-2: Cifrados Clásicos
**Ubicación**: `01_cifrados_clasicos/`

- **César**: Cifrado por sustitución con desplazamiento
- **Vigenère**: Cifrado polialfabético con clave
- **Hill**: Cifrado matricial
- **Playfair**: Cifrado por sustitución de digramas

**Notebooks**: `lab01_cesar_vigenere.ipynb`, `lab01_hill_playfair.ipynb`

---

### 🔐 Laboratorio 3-4: Cifrados Simétricos
**Ubicación**: `02_cifrados_simetricos/`

- **DES**: Data Encryption Standard (educativo)
- **AES**: Advanced Encryption Standard
- **RC4**: Stream cipher

**Notebooks**: `lab02_des.ipynb`, `lab03_aes.ipynb`, `lab04_rc4.ipynb`

---

### 🔑 **Laboratorio 5: RSA (Completo)** ⭐
**Ubicación**: `03_cifrados_asimetricos/`

#### Características del Script (`rsa.py`):
- ✅ Modo interactivo con menú
- ✅ Demostración automática (p=61, q=53, e=17, "HELLO")
- ✅ Exponenciación modular con trazabilidad
- ✅ Visualización de bloques y padding
- ✅ Validación matemática completa

#### Contenido del Notebook (`lab05_rsa.ipynb`):
1. **Algoritmo de Euclides y Euclides Extendido**
   - Cálculo de MCD
   - Inversos modulares
2. **Exponenciación Modular Rápida**
   - Algoritmo Square-and-Multiply
   - Visualización paso a paso
3. **Generación de Claves RSA**
   - Validación de primos
   - Cálculo de φ(n)
   - Generación de (e,n) y (d,n)
4. **Cifrado y Descifrado**
   - RSA básico
   - Sistema de bloques para texto
5. **Aplicación Completa**
   - Mapeo A-Z → números
   - Ejemplo: "ATTACK" con claves específicas
   - Suite de pruebas

**Ejemplo de uso**:
```python
# En el notebook o script
p, q, e = 61, 53, 17
public_key, private_key = generate_keys(p, q, e)

plaintext = "ATTACK"
cipher_blocks = encrypt_message(plaintext, e, n)
decrypted = decrypt_message(cipher_blocks, d, n)

print(cipher_blocks)  # [2478, 2382]
print(decrypted)      # "ATTACK"
```

---

### 🌐 Laboratorio 6-7: Otros Cifrados Asimétricos
**Ubicación**: `03_cifrados_asimetricos/`

- **Diffie-Hellman**: Intercambio de claves
- **ElGamal**: Cifrado asimétrico
- **ECC**: Criptografía de curvas elípticas

**Notebooks**: `lab06_diffie_hellman.ipynb`, `lab07_elgamal.ipynb`

---

### #️⃣ Laboratorio 8: Funciones Hash
**Ubicación**: `04_funciones_hash/`

- **MD5**: Message Digest 5 (educativo)
- **SHA**: Secure Hash Algorithm (versiones educativas)

**Notebook**: `lab08_hash_functions.ipynb`

---

### ✍️ Laboratorio 9: Firmas Digitales
**Ubicación**: `05_firmas_digitales/`

- **RSA Signatures**: Firma y verificación
- **DSA**: Digital Signature Algorithm

**Notebook**: `lab09_digital_signatures.ipynb`

---

### 🔒 Laboratorio 10: Protocolos
**Ubicación**: `06_protocolos/`

- **SSL/TLS**: Demostración de handshake
- **PKI**: Public Key Infrastructure

**Notebook**: `lab10_protocolos.ipynb`

---

## 🛠️ Utilidades

### `utils/math_utils.py`
Funciones matemáticas reutilizables:
- `gcd()`: Máximo común divisor
- `extended_gcd()`: Algoritmo extendido de Euclides
- `modular_inverse()`: Inverso modular
- `is_prime()`: Test de primalidad
- `generate_prime()`: Generación de primos

### `utils/conversion.py`
Conversiones de formato:
- Texto ↔ Números
- Binario ↔ Hexadecimal
- Base64 encoding/decoding

### `utils/visualization.py`
Visualizaciones:
- Diagramas de flujo de algoritmos
- Gráficos de distribución
- Animaciones de cifrado

---

## ⚠️ Advertencia Importante

### ⚠️ USO EDUCATIVO SOLAMENTE

**Estas implementaciones son para aprendizaje y NO deben usarse en producción.**

#### Razones:
- ❌ Primos pequeños (fácilmente factorizables)
- ❌ Sin padding criptográfico (OAEP, PKCS#1)
- ❌ Sin protección contra ataques de temporización
- ❌ Sin generación segura de números aleatorios
- ❌ Sin manejo de errores robusto

#### Para aplicaciones reales, usar:
```bash
pip install cryptography      # Recomendada
pip install PyCryptodome       # Alternativa
```

Ejemplo de uso seguro:
```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Generar claves RSA de 2048 bits
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
```

---

## 📖 Guía de Uso

### Para Estudiantes

1. **Empezar con los notebooks**: Cada laboratorio tiene teoría + práctica
2. **Ejecutar celda por celda**: Entender cada paso
3. **Experimentar**: Modificar parámetros y observar resultados
4. **Hacer los ejercicios**: Al final de cada notebook

### Para Profesores

1. **Usar como material de clase**: Notebooks listos para enseñar
2. **Asignar ejercicios**: Cada lab tiene tareas adicionales
3. **Modificar ejemplos**: Todo el código es modificable
4. **Crear nuevos labs**: Estructura extensible

---

## 🧪 Ejecutar Tests

```bash
# Test de todos los algoritmos
python -m pytest tests/

# Test específico
python -m pytest 03_cifrados_asimetricos/tests/test_asimetricos.py

# Con cobertura
python -m pytest --cov=. tests/
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenadas. Por favor:

1. **Fork** el repositorio
2. Crea una **rama** para tu feature:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. **Commit** tus cambios:
   ```bash
   git commit -am 'Agrega cifrado XYZ'
   ```
4. **Push** a la rama:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Crea un **Pull Request**

### Guía de Estilo
- Seguir PEP 8 para Python
- Docstrings en todas las funciones
- Type hints cuando sea posible
- Tests unitarios para nuevas funcionalidades

---

## 📚 Referencias y Recursos

### Papers Fundamentales
- **RSA (1977)**: Rivest, Shamir, Adleman - "A Method for Obtaining Digital Signatures and Public-Key Cryptosystems"
- **DES (1977)**: Data Encryption Standard - FIPS PUB 46
- **AES (2001)**: Advanced Encryption Standard - FIPS PUB 197

### Libros Recomendados
- **Applied Cryptography** - Bruce Schneier
- **Introduction to Algorithms** - Cormen, Leiserson, Rivest, Stein
- **Handbook of Applied Cryptography** - Menezes, van Oorschot, Vanstone

### Estándares
- **NIST**: National Institute of Standards and Technology
- **RFC 8017**: PKCS #1: RSA Cryptography Specifications
- **RFC 5246**: The Transport Layer Security (TLS) Protocol

### Recursos Online
- [Cryptography I - Coursera](https://www.coursera.org/learn/crypto)
- [Applied Cryptography - Udacity](https://www.udacity.com/course/applied-cryptography--cs387)
- [CrypTool](https://www.cryptool.org/) - Herramienta interactiva

---

## 📝 Licencia

MIT License

Copyright (c) 2025 Laboratorios de Criptografía

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 👥 Autores

- **Nombre del Profesor/Instructor** - Desarrollo inicial
- Ver [CONTRIBUTORS.md](CONTRIBUTORS.md) para la lista completa de contribuyentes

---

## 📞 Contacto

- **Email**: criptografia.labs@example.com
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/laboratorios_criptografia/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/tu-usuario/laboratorios_criptografia/discussions)

---

## 🎯 Roadmap

### Versión Actual (v1.0)
- ✅ RSA completo
- ✅ Cifrados clásicos
- ✅ Notebooks interactivos

### Próximas Versiones
- ⏳ v1.1: Diffie-Hellman y ElGamal
- ⏳ v1.2: Curvas Elípticas (ECC)
- ⏳ v1.3: Protocolos SSL/TLS
- ⏳ v2.0: Interfaz web interactiva

---

## ⭐ Agradecimientos

Este proyecto fue desarrollado con fines educativos para enseñar los fundamentos de la criptografía moderna. Agradecemos a la comunidad de código abierto y a todos los contribuyentes.

**Si este proyecto te fue útil, considera darle una ⭐ en GitHub!**

---

*Última actualización: Octubre 2025*
*Desarrollado para fines educativos en criptografía* 🎓