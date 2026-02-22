from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from contextvars import Context
from forms import FormCriarConta, FormLogin
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

basedir = Path(__file__).resolve().parent
data_dir = basedir / "data"
data_dir.mkdir(exist_ok=True)

db_path = data_dir / "projetosite.db"

app = Flask(__name__)

lista_usuarios = ["Erik", "Lim", "Jose", "Maria", "Joao"]
lista_usuarios.sort()

app.config["SECRET_KEY"] = "d718df7d5300f2ec0a950cd9b804445b"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

database = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html", lista_usuarios=lista_usuarios)


@app.route("/login", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and "botao_submit_login" in request.form:
        flash(
            f"Login feito com sucesso no e-mail: {form_login.email.data}",
            "alert-success",
        )
        return redirect(url_for("home"))

    if (
        form_criarconta.validate_on_submit()
        and "botao_submit_criarconta" in request.form
    ):
        flash(
            f"Conta criada com sucesso para o e-mail: {form_login.email.data}",
            "alert-success",
        )
        return redirect(url_for("home"))

    return render_template(
        "login.html", form_login=form_login, form_criarconta=form_criarconta
    )


if __name__ == "__main__":
    app.run(debug=True)
