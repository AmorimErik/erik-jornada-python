from flask import Flask, render_template, url_for
from contextvars import Context
from forms import FormCriarConta, FormLogin

app = Flask(__name__)

lista_usuarios = ["Erik", "Lim", "Jose", "Maria", "Joao"]
lista_usuarios.sort()

app.config["SECRET_KEY"] = "d718df7d5300f2ec0a950cd9b804445b"

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html", lista_usuarios=lista_usuarios)


@app.route("/login")
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    return render_template(
        "login.html", form_login=form_login, form_criarconta=form_criarconta
    )


if __name__ == "__main__":
    app.run(debug=True)
