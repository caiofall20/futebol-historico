# Passo a Passo para Configurar e Rodar o Projeto Futebol Histórico

Este guia descreve como ativar o ambiente virtual, instalar as dependências e rodar o projeto em sistemas Windows e Linux.

---

## **Windows**

### **1. Ativar o Ambiente Virtual**

1. Abra o terminal (PowerShell ou CMD).
2. Navegue até o diretório onde o ambiente virtual está localizado:
   ```powershell
   cd C:\Users\usuario\www\futebol-historico\env-windows
   ```
3. Ative o ambiente virtual:
   ```powershell
   .\Scripts\Activate.ps1
   ```
   Após ativar, você verá o nome do ambiente virtual, como `(env-windows)`, no início da linha do terminal.

### **2. Instalar Dependências**

1. Navegue para a raiz do projeto:
   ```powershell
   cd C:\Users\usuario\www\futebol-historico
   ```
2. Instale as dependências do projeto:
   ```powershell
   pip install -r requirements.txt
   ```

### **3. Rodar o Projeto**


1. Navegue para a pasta do projeto:
     ```powershell
   cd C:\Users\usuario\www\futebol-historico\env-windows
   ```
2. Com o ambiente virtual ativo e as dependências instaladas, inicie o servidor de desenvolvimento:
   ```powershell
   python manage.py runserver
   ```
3. Acesse o projeto no navegador pelo endereço:
   ```powershell
    http://127.0.0.1:8000/
   ```

---

## **Linux**

### **1. Ativar o Ambiente Virtual**

1. Abra o terminal.
2. Navegue até o diretório onde o ambiente virtual está localizado:
   ```bash
   C:\Users\usuario\www\futebol-historico\env
   ```
3. Ative o ambiente virtual:
   ```bash
   source env/bin/activate
   ```
   Após ativar, você verá o nome do ambiente virtual, como `(env)`, no início da linha do terminal.

### **2. Instalar Dependências**

1. Navegue para a raiz do projeto:
   ```bash
    C:\Users\usuario\www\futebol-historico\
   ```
2. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```

### **3. Rodar o Projeto**

1. Navegue para a pasta do projeto:
     ```powershell
   cd C:\Users\usuario\www\futebol-historico\futebol-historico
   ```
2. Com o ambiente virtual ativo e as dependências instaladas, inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```
2. Acesse o projeto no navegador pelo endereço:
   ```bash
    http://127.0.0.1:8000
   ```

---

## Resolução de Problemas

- **Permissão no PowerShell (Windows)**:
  Caso tenha problemas ao ativar o ambiente virtual, execute este comando para alterar a política de execução temporariamente:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  ```

- **Dependência Não Encontrada**:
  Certifique-se de que o arquivo `requirements.txt` está na mesma pasta do comando executado.

- **Erro de Versão do Python**:
  Verifique se a versão correta do Python está sendo usada:
  ```bash
  python --version
  ```

Agora você está pronto para configurar e rodar o projeto em Windows e Linux!

