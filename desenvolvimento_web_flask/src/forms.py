from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from src.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField("Nome de Usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField(
        "Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")]
    )
    botao_submit_criarconta = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado. Faça login para continuar")


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField("Lembrar Dados de Acesso")
    botao_submit_login = SubmitField("Fazer Login")


class FormEditarPerfil(FlaskForm):
    username = StringField("Nome de Usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    foto_perfil = FileField(
        "Atualizar a foto do perfil", validators=[FileAllowed(["jpg", "png", "jpeg"])]
    )
    curso_excel = BooleanField("Excel Impressionador")
    curso_vba = BooleanField("VBA Impressionador")
    curso_powerbi = BooleanField("Power BI Impressionador")
    curso_python = BooleanField("Python Impressionador")
    curso_ppt = BooleanField("Apresentações Impressionadoras")
    curso_sql = BooleanField("SQL Impressionador")
    botao_submit_editar_perfil = SubmitField("Confirmar edição")

    def validate_email(self, email):
        # Verificando alteração de e-mail
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError(
                    "Já existe um usuário com este e-mail. Cadastre outro e-mail."
                )
