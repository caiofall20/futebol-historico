"""Geração em segundo plano (thread) para não bloquear a interface."""
import logging
import threading

from django.db import close_old_connections

logger = logging.getLogger(__name__)

_running = set()


def start_background_generation(rascunho_id: int, nome_busca: str) -> bool:
    """
    Inicia thread de geração. Retorna False se já houver geração ativa para este id.
    """
    if rascunho_id in _running:
        return False

    def work():
        close_old_connections()
        _running.add(rascunho_id)
        try:
            from blog.models import JogadorRascunho
            from blog.content_pipeline.services import run_generation_for_rascunho

            rascunho = JogadorRascunho.objects.get(pk=rascunho_id)
            if rascunho.status == 'publicado':
                return
            run_generation_for_rascunho(rascunho, nome_busca)
        except Exception as e:
            logger.exception('Geração em background falhou (rascunho %s): %s', rascunho_id, e)
            try:
                from blog.models import JogadorRascunho
                rascunho = JogadorRascunho.objects.get(pk=rascunho_id)
                if rascunho.status == 'gerando':
                    rascunho.status = 'erro'
                    rascunho.mensagem_erro = str(e)
                    rascunho.save(update_fields=['status', 'mensagem_erro', 'atualizado_em'])
            except Exception:
                pass
        finally:
            _running.discard(rascunho_id)
            close_old_connections()

    threading.Thread(target=work, daemon=True).start()
    return True
