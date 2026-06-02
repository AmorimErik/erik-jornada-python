from flask import Flask, render_template

main_bp = Flask(__name__)


@main_bp.route("/")
def homepage():
    return render_template("homepage.html")


@main_bp.route("/perfil")
def perfil():
    return "Perfil do usuário"


if __name__ == "__main__":
    main_bp.run(debug=True)
