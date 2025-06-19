import os
import importlib.util
from logger import logger


def load_plugins(plugin_folder: str):
    """
    Carrega dinamicamente todos os módulos de plugin do diretório especificado.
    Cada plugin deve definir:
      - name: str
      - handle(text: str) -> Optional[str]
    """
    plugins = []
    if not os.path.isdir(plugin_folder):
        logger.warning(f"Pasta de plugins '{plugin_folder}' não encontrada.")
        return plugins

    for filename in os.listdir(plugin_folder):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            module_path = os.path.join(plugin_folder, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                # Verifica se o plugin tem os atributos esperados
                if hasattr(module, "name") and hasattr(module, "handle"):
                    plugins.append(module)
                    logger.info(f"Plugin '{module.name}' carregado.")
                else:
                    logger.warning(f"Arquivo {filename} não define 'name' e 'handle'. Ignorando.")
            except Exception as e:
                logger.error(f"Erro ao carregar plugin {filename}: {e}")
    return plugins
