from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_connection
from models import criar_tabelas

app = Flask(__name__)
CORS(app)  # Permite que o frontend comunique com o Flask sem erros de CORS

# Inicializa as tabelas no MySQL ao ligar o servidor
with app.app_context():
    try:
        criar_tabelas()
        print("Banco de dados verificado e pronto!")
    except Exception as e:
        print(f"Erro ao conectar ao MySQL: {e}")


# ==========================================================
# ROTAS DO CRUD DE CLIENTES
# ==========================================================

@app.route('/api/clientes', methods=['GET'])
def listar_clientes():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_cliente, razao_social, cnpj, telefone, email_contato FROM clientes")
        clientes = cursor.fetchall()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao listar clientes: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()




@app.route('/api/clientes', methods=['POST'])
def criar_cliente():
    dados = request.get_json()
    
    # Atenção: As chaves aqui devem corresponder exatamente aos campos do formulário ou ao payload enviado
    cnpj = dados.get('CNPJ') or dados.get('cnpj')
    razao_social = dados.get('Razão Social') or dados.get('razao_social')
    telefone = dados.get('Telefone') or dados.get('telefone')
    email_contato = dados.get('E-mail') or dados.get('email_contato')
    
    if not razao_social:
        return jsonify({"mensagem": "A Razão Social é obrigatória!"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO clientes (cnpj, razao_social, telefone, email_contato) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (cnpj, razao_social, telefone, email_contato))
        conn.commit()
        return jsonify({"mensagem": "Cliente cadastrado com sucesso!"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"mensagem": f"Erro ao cadastrar cliente: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()








@app.route('/api/clientes/<int:id_cliente>', methods=['DELETE'])
def apagar_cliente(id_cliente):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
        return jsonify({"mensagem": "Cliente apagado com sucesso!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"mensagem": f"Erro ao apagar cliente: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()



@app.route('/api/vendedores', methods=['GET'])
def listar_vendedor():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT id_vendedor, nome_vendedor, email_vendedor FROM vendedores """)
        vendedores = cursor.fetchall()
        return jsonify(vendedores), 200
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao listar vendedores {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/vendedores",methods = ["POST"])
def criar_vendedores():
    dados = request.get_json()

    nome_vendedor = dados.get("NOME_VENDEDOR") or dados.get("nome_vendedor")
    email_vendedor = dados.get("EMAIL_VENDEDOR") or dados.get("email_vendedor")

    if not nome_vendedor:
        return jsonify({"mensagem":"O nome do Vendedor é obrigatório!"})
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql="""INSERT INTO vendedores (nome_vendedor, email_vendedor) 
        VALUES (%s, %s)"""
        cursor.execute(sql, (nome_vendedor, email_vendedor))
        conn.commit()
        return jsonify({"mensagem":f"Vendedor cadastrado com sucesso!"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"mensagem":f"Erro ao cadastrar cliente {str(e)}"}), 501
    finally:
        cursor.close()
        conn.close()

@app.route("/api/vendedores",methods = ["DELETE"])
def apagar_vendedor():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM vendedores WHERE id_vendedor = %s", {id_vendedor,})
        cursor.commit()
        return jsonify({"mensagem":f"Vendedor apagado com sucesso!"}),200
    except Exception as e:
        conn.rollback()
        return jsonify({"mensagem":f"Erro ao apagar vendedor: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/fornecedores", methods = ["GET"])
def criar_fornecedor():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(""" SELECT (id_cliente, cnpj, nome_fornecedor, nome_contato) FROM fornecedores""")
        fornecedores = cursor.fetchall()
        return jsonify(fornecedores), 200
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao listar fornecedores: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/fornecedores", methods = ['POST'])
def criar_tabelas():
    dados = request.get_json()

    cnpj = dados.get("CNPJ") or dados.get("cnpj")
    nome_empresa = dados.get("NOME_EMPRESA") or dados.get("nome_empresa")
    nome_contato = dados.get("NOME_CONTATO") or dados.get("nome_contato")

    if not cnpj:
        return jsonify({"mensagem":"O cnpj é obrigatório!"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO fornecedores (cnpj,nome_empresa,nome_contato)
            VALUES (%s, %s, %s)"""
        cursor.execute(sql, (cnpj, nome_empresa,nome_contato))
        cursor.commit()
    except Exception as e:
        return jsonify({"mensagem":f"Erro ao cadastrar fornecedor: {str(e)}"})
    finally:
        cursor.close()
        conn.close()

@app.route("/api/fornecedores", methods = ["DELETE"])
def apagar_fornecedor(id_fornecedor):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(" DELETE FROM fornedores WHERE id_fornecedor = %s, " {id_fornecedor})
        cursor.commit()
    except Exception as e:
         return jsonify({"mensagem":f"Erro ao apagar fornecedor: {str(e)}"})
    finally:
        cursor.close()
        conn.close()

@app.route("/api/transportadoras", methods = ["GET"])
def listar_transportadoras():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT (id_transportadora, nome_empresa, tipo_veiculo, telefone_contato)   """)
        cursor.fetchall()
        return jsonify(vendedores), 200
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao listar vendedores {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/transportadoras", methods = ["POST"])
def criar_tabelas():
    conn = get_connection()
    cursor = conn.cursor()

    dados = request.get_json()

    







    






    














if __name__ == '__main__':
    app.run(debug=True, port=5000)