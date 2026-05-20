# --- File: bot.py ---
import os
import tempfile
import re  # Added for better ID extraction
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from ingest import extract_text, chunk_text
from embeddings import embed_texts
from retriever import store_chunks, retrieve_relevant_chunks
from llm import answer_question

# --- CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "8837941348:AAGdhkMvc007HOlM2poH9aI9coMCfd3_3oE"
ADMIN_CHAT_ID = 2110277018  # <--- Your numeric ID from @userinfobot

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Upload a document and ask me anything. If I can't find the answer, I'll ask my human manager!")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    ext = os.path.splitext(update.message.document.file_name)[1].lower()
    
    if ext not in [".pdf", ".docx", ".txt"]:
        await update.message.reply_text("❌ Unsupported file type.")
        return

    await update.message.reply_text("⏳ Learning document...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        await file.download_to_drive(tmp.name)
        tmp_path = tmp.name

    try:
        raw_text = extract_text(tmp_path)
        chunks = chunk_text(raw_text)
        doc_name = update.message.document.file_name.replace(" ", "_")
        store_chunks(chunks, doc_name)
        await update.message.reply_text(f"✅ Learned '{update.message.document.file_name}'!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        os.unlink(tmp_path)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # =========================================================================
    # ADMIN SECTION: Only allow replies to forwarded questions
    # =========================================================================
    if user_id == ADMIN_CHAT_ID:
        # Check if the admin is replying to a message
        if update.message.reply_to_message:
            original_text = update.message.reply_to_message.text
            
            # Use Regular Expressions to find the User ID in the text "User 12345678: Question"
            match = re.search(r"User (\d+):", original_text)
            
            if match:
                target_user_id = match.group(1) # This extracts just the number
                answer_text = update.message.text
                
                try:
                    # Send the response back to the user
                    await context.bot.send_message(
                        chat_id=target_user_id, 
                        text=f"🔔 **Response from Human Expert:**\n\n{answer_text}", 
                        parse_mode="Markdown"
                    )
                    await update.message.reply_text(f"✅ Response delivered to User {target_user_id}.")
                except Exception as e:
                    await update.message.reply_text(f"❌ Failed to send message to user: {e}")
            else:
                await update.message.reply_text("❌ I couldn't find a valid User ID in the message you are replying to.")
        else:
            # Admin sent a message that is NOT a reply. 
            # We ignore this so the admin cannot "ask" the bot questions.
            print("Admin sent a non-reply message. Ignoring.")
        
        return # STOP HERE. The admin logic is finished. Do not go to AI logic.

    # =========================================================================
    # USER SECTION: AI and RAG Logic
    # =========================================================================
    query = update.message.text
    relevant_chunks = retrieve_relevant_chunks(query)
    
    if not relevant_chunks:
        await update.message.reply_text("I don't have any documents in my memory yet.")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    answer = answer_question(query, relevant_chunks)

    if "I don't have that information in my knowledge base" in answer:
        await update.message.reply_text("Hmm, I'm not sure about that. I've forwarded your question to my human manager. They will get back to you soon! ⏳")
        
        # Forward the question to the Admin with a very clear format
        admin_message = f"User {user_id}: {query}"
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID, 
            text=f"🚨 **Human Intervention Needed!**\n\n{admin_message}"
        )
    else:
        await update.message.reply_text(answer)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running... Waiting for users.")
    app.run_polling()
