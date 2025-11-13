# 🏷️ Sistema de Gestão de Fornecedores e Vendedores de Tênis

Um sistema web desenvolvido em **Django** para gerenciamento de **fornecedores, vendedores e produtos**.  
Permite o controle de **preços, margens de lucro, comissões, taxas de plataformas** e **upload de mídias** (imagens e vídeos).

---

## 🚀 Funcionalidades Principais

- 🧾 **Cadastro de fornecedores, vendedores e produtos**
- 📦 **Upload de até 5 imagens e 1 vídeo por produto**
- 💰 **Cálculo automático de preço físico e Shopee**, com base em:
  - Comissão da plataforma
  - Margem de lucro padrão
  - Programa de frete grátis
  - Taxa de campanha destaque
  - Custo fixo e taxa por item vendido
- 📊 **Visualização clara no painel administrativo**
- 🪄 **Interface moderna e organizada (Bootstrap + CSS customizado)**
- 📁 **Painel de administração personalizado com pré-visualização de imagens**

---

## 🧩 Estrutura do Projeto

```
fornecedores_vendedores/
├── manage.py
├── requirements.txt
├── README.md
├── media/
│   └── (uploads de imagens e vídeos)
├── app/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   ├── templates/
│   │   └── produtos/
│   │       ├── listar_produtos.html
│   │       └── detalhe_produto.html
│   └── static/
│       └── css/
│           └── estilo.css
└── settings.py
```

---

## ⚙️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|-------------|-------------|
| **Python 3.12+** | Linguagem principal |
| **Django 5+** | Framework backend |
| **SQLite / PostgreSQL** | Banco de dados |
| **Bootstrap 5** | Estilo e responsividade |
| **Pillow** | Upload e manipulação de imagens |
| **HTML5 / CSS3 / JS** | Front-end do painel |

---

## 🧱 Instalação e Execução

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seuusuario/fornecedores-vendedores.git
   cd fornecedores-vendedores
   ```

2. **Crie e ative o ambiente virtual**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # (Windows)
   source venv/bin/activate  # (Linux/Mac)
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Crie o banco de dados e execute as migrações**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crie um superusuário**
   ```bash
   python manage.py createsuperuser
   ```

6. **Execute o servidor**
   ```bash
   python manage.py runserver
   ```

7. **Acesse**
   ```
   http://127.0.0.1:8000/admin/
   ```

---

## 🖼️ Upload de Imagens e Vídeos

- Máximo de **5 imagens** por produto  
- Suporte a **1 vídeo opcional** (formato MP4 recomendado)  
- Todos os arquivos ficam armazenados em `media/`  
- Configurações no `settings.py`:
  ```python
  MEDIA_URL = '/media/'
  MEDIA_ROOT = BASE_DIR / 'media'
  ```

---

## 🧠 Lógica dos Cálculos

Os preços finais são calculados automaticamente com base na configuração global (`PlatformFeeConfig`):

```python
vf_fisica = custo + (margem_fisica_padrão)
vf_shopee = custo + comissão_shopee + programa_frete_gratis + taxa_fixa + taxa_campanha
```

Essas taxas podem ser ajustadas diretamente no painel administrativo.

---

## 👨‍💻 Autor

**Moisés Souza Santos**  
Engenheiro de Software & Desenvolvedor Django  
📧 [moisessouzasantos001@gmail.com](mailto:moisessouzasantos001@gmail.com)

---

## 🪪 Licença

Este projeto é de propriedade intelectual do autor.  
É permitida a modificação e uso pessoal, **desde que não haja revenda ou distribuição sem autorização**.

---

### ⭐ Sugestão
Se for disponibilizar publicamente no GitHub, adicione:
```bash
git init
git add .
git commit -m "Sistema de gestão de fornecedores e vendedores"
```
