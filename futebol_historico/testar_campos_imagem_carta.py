#!/usr/bin/env python
"""
Script para testar que os campos imagem e carta funcionam de forma independente
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador
from django.core.files import File
from django.conf import settings

def testar_campos_independentes():
    """
    Testa que os campos imagem e carta funcionam de forma independente.
    Verifica se ao salvar uma imagem no campo 'imagem', não afeta o campo 'carta'.
    """
    print("🧪 Testando independência dos campos imagem e carta...\n")
    
    # Buscar o jogador Kaká
    try:
        kaka = Jogador.objects.get(nome__icontains='Kaká')
        print(f"✅ Jogador encontrado: {kaka.nome}\n")
        
        # Estado atual
        print("📊 Estado ANTES do teste:")
        print(f"   - Campo 'imagem': {kaka.imagem.name if kaka.imagem else 'None'}")
        print(f"   - Campo 'carta': {kaka.carta.name if kaka.carta else 'None'}\n")
        
        # Verificar se existe uma imagem em jogadores/ para testar
        caminho_imagem_teste = os.path.join(settings.MEDIA_ROOT, 'jogadores', 'kaka.jpg')
        
        if os.path.exists(caminho_imagem_teste):
            print("📝 Salvando imagem no campo 'imagem'...")
            with open(caminho_imagem_teste, 'rb') as f:
                kaka.imagem.save('kaka.jpg', File(f), save=True)
            
            # Recarregar do banco
            kaka.refresh_from_db()
            
            print("\n📊 Estado DEPOIS de salvar no campo 'imagem':")
            print(f"   - Campo 'imagem': {kaka.imagem.name if kaka.imagem else 'None'}")
            print(f"   - Campo 'carta': {kaka.carta.name if kaka.carta else 'None'}\n")
            
            # Verificar se a carta ainda está intacta
            if kaka.carta and kaka.carta.name:
                print("✅ SUCESSO: O campo 'carta' permaneceu intacto após salvar no campo 'imagem'!")
            else:
                print("⚠️  AVISO: O campo 'carta' está vazio (pode ser normal se não foi preenchido)")
        else:
            print(f"⚠️  Arquivo de teste não encontrado: {caminho_imagem_teste}")
            print("   Pulando teste de salvamento...\n")
        
        # Verificar estrutura dos diretórios
        print("📁 Verificando estrutura de diretórios:")
        dir_jogadores = os.path.join(settings.MEDIA_ROOT, 'jogadores')
        dir_cartas = os.path.join(settings.MEDIA_ROOT, 'cartas_jogadores')
        
        print(f"   - Diretório 'jogadores/': {dir_jogadores}")
        print(f"      Existe? {os.path.exists(dir_jogadores)}")
        if os.path.exists(dir_jogadores):
            arquivos = [f for f in os.listdir(dir_jogadores) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            print(f"      Arquivos: {len(arquivos)}")
        
        print(f"   - Diretório 'cartas_jogadores/': {dir_cartas}")
        print(f"      Existe? {os.path.exists(dir_cartas)}")
        if os.path.exists(dir_cartas):
            arquivos = [f for f in os.listdir(dir_cartas) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            print(f"      Arquivos: {len(arquivos)}")
        
        print("\n✅ Teste concluído!")
        
    except Jogador.DoesNotExist:
        print("❌ Jogador Kaká não encontrado no banco de dados.")
        print("\n📋 Listando alguns jogadores disponíveis:")
        jogadores = Jogador.objects.all()[:5]
        for j in jogadores:
            print(f"   - {j.nome}")
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_campos_independentes()





