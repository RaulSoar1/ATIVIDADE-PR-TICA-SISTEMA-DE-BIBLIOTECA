from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

BANCO = "Biblioteca.db"


def conectar_banco():
    conexao = sqlite3.connect(BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    conexao = conectar_banco()

    if request.method == "POST":

        titulo = request.form["titulo"]
        ano = request.form["ano"]
        id_autor = request.form["id_autor"]
        id_categoria = request.form["id_categoria"]

        conexao.execute("""
            INSERT INTO livros
            (titulo, ano_publicacao, id_autor, id_categoria)
            VALUES (?, ?, ?, ?)
        """, (titulo, ano, id_autor, id_categoria))

        conexao.commit()
        conexao.close()

        return redirect(url_for("livros"))

    autores = conexao.execute("""
        SELECT * FROM autores
        ORDER BY nome
    """).fetchall()

    categorias = conexao.execute("""
        SELECT * FROM categorias
        ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template(
        "cadastro.html",
        autores=autores,
        categorias=categorias
    )


@app.route("/livros")
def livros():

    conexao = conectar_banco()

    livros = conexao.execute("""
        SELECT
            livros.id_livro,
            livros.titulo,
            livros.ano_publicacao,
            autores.nome AS autor,
            categorias.nome AS categoria
        FROM livros
        INNER JOIN autores
            ON livros.id_autor = autores.id_autor
        INNER JOIN categorias
            ON livros.id_categoria = categorias.id_categoria
        ORDER BY livros.titulo
    """).fetchall()

    conexao.close()

    return render_template("livros.html", livros=livros)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    conexao = conectar_banco()

    if request.method == "POST":

        titulo = request.form["titulo"]
        ano = request.form["ano"]
        id_autor = request.form["id_autor"]
        id_categoria = request.form["id_categoria"]

        conexao.execute("""
            UPDATE livros
            SET titulo = ?,
                ano_publicacao = ?,
                id_autor = ?,
                id_categoria = ?
            WHERE id_livro = ?
        """, (titulo, ano, id_autor, id_categoria, id))

        conexao.commit()
        conexao.close()

        return redirect(url_for("livros"))

    livro = conexao.execute("""
        SELECT * FROM livros
        WHERE id_livro = ?
    """, (id,)).fetchone()

    autores = conexao.execute("""
        SELECT * FROM autores
        ORDER BY nome
    """).fetchall()

    categorias = conexao.execute("""
        SELECT * FROM categorias
        ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template(
        "editar.html",
        livro=livro,
        autores=autores,
        categorias=categorias
    )


@app.route("/excluir/<int:id>")
def excluir(id):

    conexao = conectar_banco()

    conexao.execute("""
        DELETE FROM livros
        WHERE id_livro = ?
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect(url_for("livros"))


if __name__ == "__main__":
    app.run(debug=True)
