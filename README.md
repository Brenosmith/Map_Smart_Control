# MaP_Smart_Control
Plataforma desenvolvida para trabalho de conclusão de curso Escola Politécnica da USP - PSI

Desenvolvimento backend Python com Django, frontend com html, css e JavaScript

---

## Passos para utilização da plataforma:
1. Pré requisito: ambiente Python instalado;
2. Criar embiente virtual: 

```python
python -m venv nome_do_projeto
```

3. Acessar ambiente virtual:
```python
nome_do_projeto\Scripts\activate.bat
```

4. Instalar bibliotecas e suas versões necessárias com arquivo requirements.txt:
```python
pip install -r requiremenst.txt
```

5. Criar um novo projeto Django:
```python
django-admin startproject nome_do_projeto
```

6. Criar o app do projeto:
```python
python manage.py startapp main
```

7. Com a hierarquia já criada, baixar arquivos deste repositório da pasta Arquivos e substituir os existentes ou colar os novos copiando a hierarquia abaixo (obs.: neste exemplo da imagem o projeto chama mysite);

<p align="center">
  <img src="https://github.com/Brenosmith/Map_Smart_Control/blob/main/hierarquia_projeto.png">
</p>

8. Acesse o diretório com o nome do projeto criado e rode o seguinte comando para iniciar o servidor:
```python
python manage.py runserver
```

9. Para acessar a plataforma acesse o caminho indicado no prompt.
10. Execute uma migração para gerar e atualizar o bando de dados:
```python
python manage.py makemigrations
python manage.py migrate
```
Extra: Comandos interessantes:
- Criar superuser para o site:
```python
manage.py createsuperuser
```

---

Passos para utilização da solução IoT:
