import bcrypt
import json
import os

ARQUIVO_USUARIOS = "usuarios.json"

def carregar_usuarios():
    """Carrega todos os usuários do arquivo JSON."""
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r") as f:
            return json.load(f)
    return {}

def salvar_usuarios(usuarios):
    """Salva a lista de usuários no arquivo JSON."""
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4) # Adicionei indent para o arquivo ficar mais legível

def cadastrar_usuario(usuario, senha):
    """Cadastra um novo usuário ou atualiza um existente."""
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        print("❌ Usuário já existe!")
        return

    salt = bcrypt.gensalt()
    hash_senha = bcrypt.hashpw(senha.encode('utf-8'), salt)
    
    # Armazena o hash como string para poder ser salvo no JSON
    usuarios[usuario] = {"senha": hash_senha.decode('utf-8')}
    salvar_usuarios(usuarios)
    print(f"✅ Usuário '{usuario}' cadastrado com sucesso!")

def login(usuario, senha):
    """Realiza o login de um usuário."""
    usuarios = carregar_usuarios()

    if usuario not in usuarios:
        print("❌ Usuário não encontrado.")
        return

    # Pega o hash da senha armazenado e o encode para comparar
    hash_armazenado = usuarios[usuario]["senha"].encode('utf-8')

    if bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado):
        print(f"✅ Login bem-sucedido para o usuário '{usuario}'!")
    else:
        print("❌ Senha incorreta.")


# --- Exemplo de uso ---
if _name_ == "_main_":
    # Cadastrando alguns usuários
    cadastrar_usuario("felipe", "minhaSenhaSuperForte")
    cadastrar_usuario("maria", "senhaDaMaria123")
    
    print("\n--- Testando o Login ---")
    
    # Tentativa de login bem-sucedida
    login("felipe", "minhaSenhaSuperForte")
    
    # Tentativa de login com senha incorreta
    login("felipe", "senhaErrada")

    # Tentativa de login de um usuário que não existe
    login("joao", "senhaQualquer")


    teste - branch teste