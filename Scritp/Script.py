import bcrypt
import json
import os
import threading
import time
import argparse 

ARQUIVO_USUARIOS = "usuarios.json"

lock = threading.Lock()
senha_encontrada = False

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


if __name__ == "__main__":
    # --- Configuração da Linha de Comando ---
    parser = argparse.ArgumentParser(description="Ferramenta de ataque de dicionário para senhas com bcrypt.")
    parser.add_argument("--usuario", required=True, help="Nome do usuário para o ataque.")
    parser.add_argument("--wordlist", required=True, help="Caminho para o arquivo com a lista de senhas.")
    
    args = parser.parse_args()

    # Acessa os argumentos passados pelo usuário
    TARGET_USERNAME = args.usuario
    WORDLIST_FILE = args.wordlist

    # Lógica principal do ataque
    usuarios = carregar_usuarios()
    
    # Valida se o usuário existe
    if TARGET_USERNAME not in usuarios:
        print(f"❌ Usuário '{TARGET_USERNAME}' não encontrado. Certifique-se de que ele foi cadastrado.")
    else:
        # Valida se o arquivo de wordlist existe
        try:
            with open(WORDLIST_FILE, "r") as f:
                passwords = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print(f"❌ Arquivo de wordlist '{WORDLIST_FILE}' não encontrado.")
        else:
            print(f"Iniciando ataque para o usuário: {TARGET_USERNAME}")
            print(f"Total de senhas a serem testadas: {len(passwords)}")

            num_threads = 4  # Você pode ajustar esse número para testar
            chunk_size = len(passwords) // num_threads
            chunks = [passwords[i:i + chunk_size] for i in range(0, len(passwords), chunk_size)]
            
            target_hash = usuarios[TARGET_USERNAME]["senha"].encode('utf-8')

            threads = []
            start_time = time.time() # Começa a contar o tempo

            # Cria e inicia os threads
            for chunk in chunks:
                thread = threading.Thread(target=brute_force_attack_thread, args=(TARGET_USERNAME, target_hash, chunk))
                threads.append(thread)
                thread.start()

            # Espera todos os threads terminarem
            for thread in threads:
                thread.join()

            end_time = time.time()
            
            if not senha_encontrada:
                print("\n❌ [FALHA] Senha não encontrada na wordlist.")

            print(f"Tempo total do ataque: {end_time - start_time:.2f} segundos.")

