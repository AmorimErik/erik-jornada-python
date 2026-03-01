from flask import Blueprint, flash, redirect, request, render_template, url_for
from wtforms import BooleanField
from src.forms import FormCriarConta, FormLogin, FormEditarPerfil
from src.models import Usuario
from src import database, bcrypt
from flask_login import current_user, login_user, login_required, logout_user
from PIL import Image
from pathlib import Path
import secrets


main_bp = Blueprint("main", __name__)
lista_usuarios = []


@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/contato")
def contato():
    return render_template("contato.html")


@main_bp.route("/usuarios")
@login_required
def usuarios():
    return render_template("usuarios.html", lista_usuarios=lista_usuarios)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and "botao_submit_login" in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(
                f"Login feito com sucesso no e-mail: {form_login.email.data}",
                "alert-success",
            )
            parametro_next = request.args.get("next")
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for("main.home"))
        else:
            flash("Falha no login. E-mail ou senha incorretos", "alert-danger")

    if (
        form_criarconta.validate_on_submit()
        and "botao_submit_criarconta" in request.form
    ):
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=senha_cript,
        )
        database.session.add(usuario)
        database.session.commit()
        flash(
            f"Conta criada com sucesso para o e-mail: {form_criarconta.email.data}",
            "alert-success",
        )
        return redirect(url_for("main.home"))

    return render_template(
        "login.html", form_login=form_login, form_criarconta=form_criarconta
    )


@main_bp.route("/sair")
@login_required
def sair():
    logout_user()
    flash("Logout feito com sucesso!", "alert-success")
    return redirect(url_for("main.home"))


@main_bp.route("/perfil")
@login_required
def perfil():
    foto_perfil = url_for("static", filename=f"fotos_perfil/{current_user.foto_perfil}")
    return render_template("perfil.html", foto_perfil=foto_perfil)


@main_bp.route("/post/criar")
@login_required
def criar_post():
    return render_template("criarpost.html")


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    arquivo = Path(imagem.filename)
    nome_arquivo_imagem = f"{arquivo.stem}{codigo}{arquivo.suffix}"
    caminho_diretorio = Path(main_bp.root_path) / "static" / "fotos_perfil"
    caminho_arquivo = caminho_diretorio / nome_arquivo_imagem
    foto_antiga = current_user.foto_perfil
    if foto_antiga != "default.jpg":
        caminho_antigo = caminho_diretorio / foto_antiga
        if caminho_antigo.exists():
            caminho_antigo.unlink()
    tamanho_imagem = (200, 200)
    with Image.open(imagem) as img:
        img.thumbnail(tamanho_imagem)
        caminho_diretorio.mkdir(parents=True, exist_ok=True)
        img.save(caminho_arquivo)
    return nome_arquivo_imagem


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if "curso_" in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ";".join(lista_cursos), len(lista_cursos)


@main_bp.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos, current_user.total_cursos = atualizar_cursos(form)
        database.session.commit()
        flash(f"Perfil atualizado com sucesso", "alert-success")
        return redirect(url_for("main.perfil"))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
        for campo in form:
            for curso in current_user.cursos.split(";"):
                if curso in str(campo.label):
                    campo.data = BooleanField(default="checked")

    foto_perfil = url_for("static", filename=f"fotos_perfil/{current_user.foto_perfil}")
    return render_template("editarperfil.html", foto_perfil=foto_perfil, form=form)
