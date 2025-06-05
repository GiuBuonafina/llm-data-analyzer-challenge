from dotenv import dotenv_values

def load_config(path="Configuration.env"):
    """
    Carrega as configurações do arquivo .env.
    """
    return dotenv_values(path)