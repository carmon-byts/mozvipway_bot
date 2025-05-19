from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import os
import time

# ========== CONFIGURAÇÕES ==========
TOKEN = "7666717095:AAGD0o2jhEs6-wQRTk1uhUbywjaVC3OBQX4"
PACOTE_PATH = "PACOTE-MAGICO-MZ.zip"
ADMIN_CHAT_ID = 123456789  # Substitua pelo seu ID do Telegram
comprovativos = {}
ultimo_envio_foto = {}  # Para evitar spam de fotos

PALAVRAS_PROIBIDAS = ["merda", "filho da puta", "ladrão", "scam", "roubo", "burla"]

# ========== PACOTES DISPONÍVEIS==========
PACOTES = {
    "vpn": {
        "nome": "🔓 Pacote VIP: Internet Ilimitada",
        "preco": 20,
        "descricao": (
            "🔥 Adquira acesso total à internet!\n\n"
            "Este pacote inclui:\n"
            "- Arquivos de configuração para VPN poderosa e secreta\n"
            "- Tutorial passo a passo para usar no seu celular\n"
            "- Funciona em qualquer operadora (Vodacom, Movitel, TMcel)\n\n"
            "🌐 Navega ilimitado. Vê vídeos, usa redes sociais, joga online SEM PAGAR SALDO.\n\n"
            "TUDO EM UM ARQUIVO ZIP PRONTO PARA BAIXAR assim que validar pagamento."
        )
    },
    "app": {
        "nome": "💸 Guia: Ganhe Dinheiro Online",
        "preco": 30,
        "descricao": (
            "💰 Transforme seu tempo livre em renda real SEM INVESTIMENTO!\n\n"
            "Você vai receber:\n"
            "- Um guia em PDF com estratégias reais usadas por vendedores profissionais\n"
            "- Passo a passo ilustrado para criar loja no WhatsApp ou redes sociais\n"
            "- Dicas para começar HOJE, mesmo sem experiência\n\n"
            "Este é o plano perfeito para sair da crise e entrar no mundo do lucro digital.\n\n"
            "TUDO EM UM ARQUIVO ZIP PRONTO PARA BAIXAR assim que validar pagamento."
        )
    },
    "pdf": {
        "nome": "📘 Guia Premium: Como Usar Tudo",
        "preco": 10,
        "descricao": (
            "🎯 Quer dominar tudo em poucos minutos?\n\n"
            "Este pacote contém:\n"
            "- Um tutorial ilustrado com imagens passo a passo\n"
            "- Como configurar apps secretos, instalar VPNs, usar truques escondidos\n"
            "- Proteger suas contas e navegar anônimo\n\n"
            "Ideal tanto para iniciantes quanto para quem já conhece e quer melhorar.\n\n"
            "TUDO EM UM ARQUIVO ZIP PRONTO PARA BAIXAR assim que validar pagamento."
        )
    },
    "bonus": {
        "nome": "🎁 Bónus Surpresa Ultra VIP",
        "preco": 5,
        "descricao": (
            "🎉 Só os verdadeiros VIPs ganham este presente misterioso…\n\n"
            "Ao adquirir qualquer um dos pacotes acima, ganhas automaticamente:\n"
            "- Um app premium pago desbloqueado\n"
            "- Uma VPN rara de alta velocidade\n"
            "- Um jogo modificado\n"
            "- Ou outro conteúdo secreto especial\n\n"
            "É surpresa, mas é garantido: quem compra, ganha!\n\n"
            "TUDO EM UM ARQUIVO ZIP PRONTO PARA BAIXAR assim que validar pagamento."
        )
    },
    "pacote_completo": {
        "nome": "📦 PACOTE MÁGICO MOZ - TUDO EM UM ZIP!",
        "preco": 50,
        "descricao": (
            "🚀 VOCÊ ESTÁ A 1 PASSO DE UMA REVOLUÇÃO DIGITAL!\n\n"
            "Com este pacote completo você recebe:\n"
            "- 🔓 ACESSO ILIMITADO À INTERNET (VPN + GUIA)\n"
            "- 💸 COMO GANHAR DINHEIRO ONLINE SEM INVESTIR\n"
            "- 📘 TUTORIAL ILUSTRADO COMPLETO\n"
            "- 🎁 BÓNUS SURPRESAS EXCLUSIVOS\n\n"
            "✅ Todos os arquivos são compactados em um único ZIP super organizado.\n"
            "✅ Contém PDFs, apps, imagens, tutoriais completos e segredos exclusivos.\n"
            "✅ É só baixar e seguir as instruções — funciona até no seu primeiro dia!\n\n"
            "Transforme sua rotina hoje. Este pacote vai mudar sua vida digital pra sempre!\n\n"
            "Por apenas *50 MT*, você tem tudo que precisa para ser dono do seu futuro!"
        )
    }
}

# ========== MENSAGENS PERSONALIZADAS ==========
MENSAGEM_INICIAL = (
    "📡 *BEM-VINDO AOS PACOTES MÁGICOS MOZ! 🇲🇿*\n\n"
    "És um passo à frente dos outros… estás prestes a desbloquear os segredos que poucos conhecem!\n\n"
    "Olá {user}, este é o lugar onde vais encontrar ferramentas poderosas para:\n\n"
    "- 🌐 Navegar grátis na internet\n"
    "- 💰 Ganhar dinheiro online\n"
    "- 📘 Aprender tudo rápido\n"
    "- 🎁 Receber bónus surpresa\n\n"
    "Cada pacote está pronto para download em um único arquivo ZIP, com todos os documentos e apps necessários.\n\n"
    "💡 Mas se quiser o MAIOR VALOR, escolha o *PACOTE COMPLETO* por apenas *50 MT*. Vale mais que tudo!\n\n"
    "Escolhe com sabedoria e começa tua jornada mágica:"
)

MENSAGEM_AJUDA = (
    "❓ *Ajuda - Como funciona?*\n\n"
    "1️⃣ Escolha um pacote\n"
    "2️⃣ Faça o pagamento via M-Pesa para o número indicado\n"
    "3️⃣ Use `/comprovativo NOME VALOR`\n"
    "4️⃣ Envie a foto do pagamento\n"
    "5️⃣ Após aprovação, use `/receber` para baixar o ZIP com todo o conteúdo!\n\n"
    "Precisa de ajuda? É só perguntar 😊"
)

MENSAGEM_COMPROVATIVO_RECEBIDO = "📷 Comprovativo recebido! Agora envie o *screenshot* do pagamento."

MENSAGEM_FOTO_REPETIDA = "⚠️ Foto repetida ou possivelmente fraudada. Por favor, envie uma nova foto diferente."

MENSAGEM_ENVIO_MUITO_RAPIDO = "⏳ Você está enviando fotos muito rápido. Espere alguns segundos antes de tentar novamente."

MENSAGEM_COMPROVATIVO_FINAL = "✅ Comprovativo enviado. Em breve vamos verificar e liberar seu pacote!"

# ========== HANDLERS ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    teclado = [[InlineKeyboardButton(p["nome"], callback_data=key)] for key, p in PACOTES.items()]
    await update.message.reply_text(
        MENSAGEM_INICIAL.format(user=user),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(teclado)
    )

async def pacote_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data
    pacote = PACOTES.get(key)
    if not pacote:
        await query.edit_message_text("❌ Opção inválida.")
        return
    texto = (
        f"{pacote['nome']} 🎯\n\n"
        f"{pacote['descricao']}\n\n"
        f"💰 Preço: *{pacote['preco']} MT*\n\n"
        "📲 Para comprar, faça o pagamento via M-Pesa para:\n"
        "➡️ 852361783 (CARMÓNIO)\n\n"
        "📷 Depois envie o comprovativo com:\n"
        f"`/comprovativo CARMÓNIO {pacote['preco']}`\n"
        "E envie o *screenshot* do pagamento."
    )
    await query.edit_message_text(texto, parse_mode="Markdown")

async def comprovativo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        nome = context.args[0]
        valor = int(context.args[1])
        if valor not in [p["preco"] for p in PACOTES.values()]:
            await update.message.reply_text("❌ Valor não corresponde a nenhum pacote disponível.", parse_mode="Markdown")
            return
        comprovativos[user_id] = {"nome": nome, "valor": valor, "screenshot": False}
        await update.message.reply_text(MENSAGEM_COMPROVATIVO_RECEBIDO, parse_mode="Markdown")
    except:
        await update.message.reply_text("⚠️ Formato errado! Use: `/comprovativo NOME VALOR`", parse_mode="Markdown")

async def receber_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = time.time()

    # Bloqueio por tempo curto
    if user_id in ultimo_envio_foto and now - ultimo_envio_foto[user_id] < 5:
        await update.message.reply_text(MENSAGEM_ENVIO_MUITO_RAPIDO)
        return

    if user_id in comprovativos:
        photo = update.message.photo[-1]
        caminho = f"comprovativos/{user_id}.jpg"

        # Verifica se já existe foto antiga
        if os.path.exists(caminho):
            novo_caminho = f"comprovativos/{user_id}_novo.jpg"
            file = await photo.get_file()
            await file.download_to_drive(novo_caminho)

            # Comparação simples: tamanho do arquivo
            tam_antigo = os.path.getsize(caminho)
            tam_novo = os.path.getsize(novo_caminho)

            if abs(tam_antigo - tam_novo) < 1024:  # Menos de 1KB de diferença
                os.remove(novo_caminho)
                await update.message.reply_text(MENSAGEM_FOTO_REPETIDA)
                return
            else:
                os.rename(novo_caminho, caminho)  # Atualiza com nova foto
        else:
            file = await photo.get_file()
            await file.download_to_drive(caminho)

        # Encaminhar para admin
        try:
            await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=open(caminho, 'rb'), caption=f"📸 Comprovativo de {user_id}")
        except Exception as e:
            print(f"❌ Erro ao enviar foto para admin: {e}")

        comprovativos[user_id]["screenshot"] = True
        await update.message.reply_text(MENSAGEM_COMPROVATIVO_FINAL, parse_mode="Markdown")
        ultimo_envio_foto[user_id] = now
    else:
        await update.message.reply_text("⚠️ Antes use: `/comprovativo NOME VALOR`", parse_mode="Markdown")

async def receber(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    dados = comprovativos.get(user_id)
    if not dados:
        await update.message.reply_text("⚠️ Você ainda não enviou o comprovativo. Use /comprovativo primeiro.")
        return
    if dados["screenshot"]:
        if os.path.exists(PACOTE_PATH):
            await update.message.reply_document(document=InputFile(PACOTE_PATH))
        else:
            await update.message.reply_text("❌ Erro: Arquivo do pacote não encontrado.")
    else:
        await update.message.reply_text("⚠️ Comprovativo incompleto. Envie o valor e a foto.")

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENSAGEM_AJUDA, parse_mode="Markdown")

# ========== RESPOSTA AUTOMÁTICA E MODERAÇÃO ==========

async def handle_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = update.message.text.lower()
    user = update.effective_user

    if any(p in mensagem for p in PALAVRAS_PROIBIDAS):
        if update.message.chat.type != "private":
            try:
                await context.bot.ban_chat_member(chat_id=update.message.chat_id, user_id=user.id)
                await update.message.reply_text(f"🚫 {user.first_name}, você foi removido por linguagem inadequada.")
            except:
                await update.message.reply_text("⚠️ Preciso de permissão de administrador.")
        else:
            await update.message.reply_text("🚫 Linguagem inadequada detectada.")
        return

    if any(x in mensagem for x in ["todos", "completo", "todo", "tudo", "combo"]):
        await update.message.reply_text(PACOTES["pacote_completo"]["descricao"], parse_mode="Markdown")
    elif "vpn" in mensagem or "internet" in mensagem:
        await update.message.reply_text(PACOTES["vpn"]["descricao"], parse_mode="Markdown")
    elif "dinheiro" in mensagem or "venda" in mensagem:
        await update.message.reply_text(PACOTES["app"]["descricao"], parse_mode="Markdown")
    elif "tutorial" in mensagem or "pdf" in mensagem:
        await update.message.reply_text(PACOTES["pdf"]["descricao"], parse_mode="Markdown")
    elif "surpresa" in mensagem or "bônus" in mensagem:
        await update.message.reply_text(PACOTES["bonus"]["descricao"], parse_mode="Markdown")
    elif "ajuda" in mensagem or "como" in mensagem or "funciona" in mensagem:
        await update.message.reply_text(MENSAGEM_AJUDA, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "👋 Olá {user}, recebemos sua mensagem:\n\n"
            "“{mensagem}”\n\n"
            "Em breve nossa equipe irá responder 😄\n"
            "Ou digite /start para ver nossos pacotes disponíveis!".format(
                user=user.first_name, mensagem=mensagem
            ),
            parse_mode="Markdown"
        )

# ========== INICIAR BOT ==========

app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ajuda", ajuda))
app.add_handler(CommandHandler("comprovativo", comprovativo))
app.add_handler(CommandHandler("receber", receber))
app.add_handler(CallbackQueryHandler(pacote_callback))
app.add_handler(MessageHandler(filters.PHOTO, receber_foto))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mensagem))

print("🚀 BOT MÁGICO está online...")
app.run_polling()
