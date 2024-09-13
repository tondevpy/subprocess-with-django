from django.shortcuts import render
from django.http import StreamingHttpResponse
import subprocess
import os
from django.conf import settings

def projetos(request):
    # Retorna a página com o layout inicial (botão e espaço para o output)
    return render(request, 'projetos.html')

# Essa view executa o script e envia a saída em tempo real via StreamingHttpResponse
def executar_projetos(request):
    script_path = os.path.join(settings.BASE_DIR, 'app.py')
    
    def generate_output():
        # Subprocesso para rodar o script e capturar a saída
        process = subprocess.Popen(
            ['python', script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

        # Itera sobre cada linha de saída do script
        for line in iter(process.stdout.readline, ''):
            if line:
                yield line  # Envia cada linha para o cliente

        process.stdout.close()

    # Resposta com a saída do script
    return StreamingHttpResponse(generate_output(), content_type="text/plain")
