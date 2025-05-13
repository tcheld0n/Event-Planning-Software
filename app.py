from flask import Flask, render_template, request, redirect, url_for, flash
from services.event_service import EventService
from services.participant_service import ParticipantService
from services.speaker_service import SpeakerService
from services.vendor_service import VendorService
from services.feedback_service import FeedbackService
from services.event_service import EventService  # para orçamento

def create_app():
    app = Flask(__name__)
    app.secret_key = 'sua_chave_secreta'

    # Rotas do front-end (rotas "amigáveis")

    @app.route("/")
    def index():
        return render_template("index.html")

    # Eventos
    @app.route("/criar_evento", methods=["GET", "POST"])
    def criar_evento():
        if request.method == "POST":
            nome = request.form.get("nome")
            data = request.form.get("data")
            orcamento = request.form.get("orcamento")
            try:
                evento = EventService().create(nome, data, int(orcamento))
                flash("Evento criado com sucesso!", "success")
                return redirect(url_for("listar_eventos"))
            except Exception as e:
                flash(f"Erro ao criar evento: {e}", "danger")
        return render_template("criar_evento.html")

    @app.route("/eventos")
    def listar_eventos():
        eventos = EventService().list_events()
        return render_template("eventos.html", eventos=eventos)

    @app.route("/editar_evento/<int:event_id>", methods=["GET", "POST"])
    def editar_evento(event_id):
        service = EventService()
        if request.method == "POST":
            nome = request.form.get("nome")
            data = request.form.get("data")
            orcamento = request.form.get("orcamento")
            try:
                service.update(event_id, name=nome, date=data, budget=orcamento)
                flash("Evento atualizado!", "success")
                return redirect(url_for("listar_eventos"))
            except Exception as e:
                flash(f"Erro ao atualizar: {e}", "danger")
        # Obtenha o evento para preencher os campos
        evento = next((ev for ev in service.list_events() if ev["id"] == event_id), None)
        return render_template("editar_evento.html", evento=evento)

    @app.route("/excluir_evento/<int:event_id>")
    def excluir_evento(event_id):
        if EventService().delete(event_id):
            flash("Evento excluído com sucesso!", "success")
        else:
            flash("Evento não encontrado!", "danger")
        return redirect(url_for("listar_eventos"))

    # Participantes
    @app.route("/registrar_participante", methods=["GET", "POST"])
    def registrar_participante():
        if request.method == "POST":
            event_id = request.form.get("event_id")
            nome = request.form.get("nome")
            try:
                ParticipantService().create(event_id, nome)
                flash("Participante registrado!", "success")
                return redirect(url_for("listar_participantes"))
            except Exception as e:
                flash(f"Erro: {e}", "danger")
        return render_template("registrar_participante.html")

    @app.route("/listar_participantes", methods=["GET"])
    def listar_participantes():
        participantes = None
        event_id = request.args.get("event_id")
        if event_id:
            participantes = ParticipantService().get_attendees(event_id)
        return render_template("participantes.html", participantes=participantes)

    @app.route("/editar_participante/<int:participant_id>", methods=["GET", "POST"])
    def editar_participante(participant_id):
        if request.method == "POST":
            novo_nome = request.form.get("novo_nome")
            try:
                ParticipantService().update(participant_id, novo_nome)
                flash("Participante atualizado!", "success")
                return redirect(url_for("listar_participantes"))
            except Exception as e:
                flash(f"Erro: {e}", "danger")
        # Aqui, para simplificar, você pode passar o ID e um nome vazio ou implementar uma consulta
        participante = {"id": participant_id, "name": ""}
        return render_template("editar_participante.html", participante=participante)

    # Palestrantes
    @app.route("/registrar_palestrante", methods=["GET", "POST"])
    def registrar_palestrante():
        if request.method == "POST":
            event_id = request.form.get("event_id")
            nome = request.form.get("nome")
            descricao = request.form.get("descricao")
            try:
                SpeakerService().create(event_id, nome, descricao)
                flash("Palestrante registrado!", "success")
                return redirect(url_for("listar_palestrantes"))
            except Exception as e:
                flash(f"Erro: {e}", "danger")
        return render_template("registrar_palestrante.html")

    @app.route("/listar_palestrantes", methods=["GET"])
    def listar_palestrantes():
        palestrantes = None
        event_id = request.args.get("event_id")
        if event_id:
            palestrantes = SpeakerService().list_speakers(event_id)
        return render_template("palestrantes.html", palestrantes=palestrantes)

    @app.route("/editar_palestrante/<int:speaker_id>", methods=["GET", "POST"])
    def editar_palestrante(speaker_id):
        if request.method == "POST":
            novo_nome = request.form.get("novo_nome")
            nova_descricao = request.form.get("nova_descricao")
            try:
                SpeakerService().update(speaker_id, new_name=novo_nome, new_description=nova_descricao)
                flash("Palestrante atualizado!", "success")
                return redirect(url_for("listar_palestrantes"))
            except Exception as e:
                flash(f"Erro: {e}", "danger")
        palestrante = {"id": speaker_id, "name": "", "description": ""}
        return render_template("editar_palestrante.html", palestrante=palestrante)

    # Fornecedores
    @app.route("/registrar_fornecedor", methods=["GET", "POST"])
    def registrar_fornecedor():
        if request.method == "POST":
            event_id = request.form.get("event_id")
            nome = request.form.get("nome")
            servicos = request.form.get("servicos")
            try:
                VendorService().create(event_id, nome, servicos)
                flash("Fornecedor registrado!", "success")
                return redirect(url_for("listar_fornecedores"))
            except Exception as e:
                flash(f"Erro: {e}", "danger")
        return render_template("registrar_fornecedor.html")

    @app.route("/listar_fornecedores", methods=["GET"])
    def listar_fornecedores():
        fornecedores = None
        event_id = request.args.get("event_id")
        if event_id:
            fornecedores = VendorService().list_vendors(event_id)
        return render_template("fornecedores.html", fornecedores=fornecedores)

    @app.route("/editar_fornecedor/<int:vendor_id>", methods=["GET", "POST"])
    def editar_fornecedor(vendor_id):
        if request.method == "POST":
            novo_nome = request.form.get("novo_nome")
            novos_servicos = request.form.get("novos_servicos")
            try:
                VendorService().update(vendor_id, new_name=novo_nome, new_services=novos_servicos)
                flash("Fornecedor atualizado!", "success")
                return redirect(url_for("listar_fornecedores"))
            except Exception as e:
                flash(f"Erro: {e}", "danger")
        fornecedor = {"id": vendor_id, "name": "", "services": ""}
        return render_template("editar_fornecedor.html", fornecedor=fornecedor)

    # Orçamento
    @app.route("/atualizar_orcamento", methods=["GET", "POST"])
    def atualizar_orcamento():
        if request.method == "POST":
            event_id = request.form.get("event_id")
            amount = request.form.get("amount")
            try:
                EventService().update_budget(event_id, int(amount))
                flash("Orçamento atualizado!", "success")
                return redirect(url_for("ver_orcamento"))
            except Exception as e:
                flash(f"Erro: {e}", "danger")
        return render_template("atualizar_orcamento.html")

    @app.route("/ver_orcamento", methods=["GET"])
    def ver_orcamento():
        budget = None
        event_id = request.args.get("event_id")
        if event_id:
            budget = EventService().get_budget(event_id)
        return render_template("ver_orcamento.html", budget=budget)

    @app.route("/editar_orcamento", methods=["GET", "POST"])
    def editar_orcamento():
        if request.method == "POST":
            event_id = request.form.get("event_id")
            novo_orcamento = request.form.get("novo_orcamento")
            try:
                EventService().edit_budget(event_id, int(novo_orcamento))
                flash("Orçamento alterado!", "success")
                return redirect(url_for("ver_orcamento"))
            except Exception as e:
                flash(f"Erro: {e}", "danger")
        return render_template("editar_orcamento.html")

    # Feedback
    @app.route("/adicionar_feedback", methods=["GET", "POST"])
    def adicionar_feedback():
        if request.method == "POST":
            event_id = request.form.get("event_id")
            feedback = request.form.get("feedback")
            try:
                FeedbackService().create(event_id, feedback)
                flash("Feedback adicionado!", "success")
                return redirect(url_for("index"))
            except Exception as e:
                flash(f"Erro: {e}", "danger")
        return render_template("adicionar_feedback.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
