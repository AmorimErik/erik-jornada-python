from flask import Blueprint, flash, redirect, request, render_template, url_for
from src.forms import FormCriarConta, FormLogin
from src.models import Usuario
from src import database

main_bp = Blueprint("main", __name__)
lista_usuarios = []


@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/contato")
def contato():
    return render_template("contato.html")


@main_bp.route("/usuarios")
def usuarios():
    return render_template("usuarios.html", lista_usuarios=lista_usuarios)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and "botao_submit_login" in request.form:
        flash(
            f"Login feito com sucesso no e-mail: {form_login.email.data}",
            "alert-success",
        )
        return redirect(url_for("main.home"))

    if (
        form_criarconta.validate_on_submit()
        and "botao_submit_criarconta" in request.form
    ):
        usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=form_criarconta.senha.data,
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
