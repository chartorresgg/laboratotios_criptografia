# 🔐 Laboratorios de Criptografía

Repositorio de implementaciones educativas de algoritmos criptográficos clásicos, simétricos y asimétricos.

## 📁 Estructura del Proyecto
laboratorios_criptografia/
├── 01_cifrados_clasicos/      # César, Vigenère, Hill, Playfair
├── 02_cifrados_simetricos/    # DES, AES, RC4
├── 03_cifrados_asimetricos/   # RSA, Diffie-Hellman, ElGamal, ECC
├── 04_funciones_hash/         # MD5, SHA (implementaciones educativas)
├── 05_firmas_digitales/       # RSA Signatures, DSA
├── 06_protocolos/             # SSL/TLS demos, PKI
└── utils/                     # Utilidades compartidas

## 🚀 Inicio Rápido

### Instalación
```bash
git clone https://github.com/tu-usuario/laboratorios_criptografia.git
cd laboratorios_criptografia
pip install -r requirements.txt
Ejecutar Scripts
bash# RSA interactivo
python 03_cifrados_asimetricos/rsa.py

# Jupyter Notebooks
jupyter notebook 03_cifrados_asimetricos/notebooks/lab05_rsa.ipynb
📚 Laboratorios
Lab 1-2: Cifrados Clásicos

César, Vigenère, Hill, Playfair

Lab 3-4: Cifrados Simétricos

DES, AES, RC4

Lab 5: RSA ⭐

Algoritmo de Euclides Extendido
Exponenciación Modular Rápida
Sistema RSA completo con alfabeto A-Z

Lab 6-7: Otros Asimétricos

Diffie-Hellman, ElGamal, ECC

Lab 8: Funciones Hash

MD5, SHA (versiones educativas)

Lab 9: Firmas Digitales

RSA Signatures, DSA

Lab 10: Protocolos

TLS, PKI

⚠️ Advertencia
Uso Educativo Solamente: Estas implementaciones son para aprendizaje. NO usar en producción. Para aplicaciones reales, usar bibliotecas establecidas como:

cryptography
PyCryptodome
OpenSSL

🤝 Contribuciones
Las contribuciones son bienvenidas. Por favor:

Fork el repositorio
Crea una rama (git checkout -b feature/nueva-funcionalidad)
Commit cambios (git commit -am 'Agrega nueva funcionalidad')
Push a la rama (git push origin feature/nueva-funcionalidad)
Crea un Pull Request

📖 Referencias

Rivest, Shamir, Adleman (1977): "A Method for Obtaining Digital Signatures"
NIST Standards
Applied Cryptography (Bruce Schneier)

📝 Licencia
MIT License - Ver archivo LICENSE

Desarrollado para fines educativos en criptografía 🎓

### 📄 requirements.txt
```txt
jupyter>=1.0.0
notebook>=6.5.0
numpy>=1.24.0
matplotlib>=3.7.0
📋 Instrucciones Finales
Para usar el script refinado:

Activa el modo detallado (opción 7) en el menú interactivo
Al encriptar o desencriptar, verás:

Exponenciación paso a paso con binario
Bloques con padding explícito
Desglose letra por letra



Para usar el Jupyter Notebook:

Copia el contenido del artifact en 03_cifrados_asimetricos/notebooks/lab05_rsa.ipynb
Ejecuta celda por celda para entender cada algoritmo
Todas las funciones tienen docstrings y ejemplos