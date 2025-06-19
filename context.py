from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
from config import config
import openai

# Configura OpenAI
openai.api_key = config.OPENAI_API_KEY

# Banco de dados de contexto
engine = create_engine(config.DB_URL, connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
Base = declarative_base()

class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    role = Column(String)
    content = Column(Text)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Memory(Base):
    __tablename__ = 'memories'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Cria tabelas
Base.metadata.create_all(engine)

# Funções de contexto

def save_message(role, content):
    """Salva uma mensagem no histórico."""
    s = Session()
    s.add(History(role=role, content=content))
    s.commit()
    s.close()


def get_history(limit=20):
    """Retorna as últimas `limit` mensagens em ordem cronológica."""
    s = Session()
    rows = s.query(History).order_by(History.id.desc()).limit(limit).all()
    s.close()
    return list(reversed([(r.role, r.content) for r in rows]))


def save_memory(title, content):
    """Armazena uma memória de longo prazo."""
    s = Session()
    s.add(Memory(title=title, content=content))
    s.commit()
    s.close()


def get_memories(limit=10):
    """Retorna as últimas `limit` memórias."""
    s = Session()
    rows = s.query(Memory).order_by(Memory.id.desc()).limit(limit).all()
    s.close()
    return [(m.title, m.content) for m in rows]


def summarize_history():
    """
    Se o histórico exceder 20 mensagens, chama a OpenAI para resumir as primeiras e manter o contexto.
    Insere o resumo como `system` e preserva as últimas 20 mens agens.
    """
    hist = get_history(40)
    if len(hist) <= 20:
        return None
    prompt = ' '.join([f"{r}:{c}" for r, c in hist[:-20]])
    resp = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[{'role': 'system', 'content': 'Resuma: ' + prompt}]
    )
    summary = resp.choices[0].message.content
    s = Session()
    s.query(History).delete()
    s.commit()
    for r, c in hist[-20:]:
        s.add(History(role=r, content=c))
    s.add(History(role='system', content=summary))
    s.commit()
    s.close()
    return summary

