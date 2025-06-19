# -- logger.py
# noinspection PyPackageRequirements
from opentelemetry import trace
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

# Inicializa tracer OpenTelemetry
tracer = trace.get_tracer('lia')
# Logger Python padrão para mensagens
logger = logging.getLogger('lia')
