from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
TOKEN = "7776230374:AAFnc1cJfMb40Pqa1QrZiEBzzbER_jo1U5o"
AUTHOR = "@deinchris"

grammar_exercise = [
    {
        "sentence": "Er _____ gestern einen neuen Anzug.",
        "options": ["kauft", "kaufte", "kauftet"],
        "correct": "kaufte"
    },
    {
        "sentence": "Ich _____ das Buch schon gelesen.",
        "options": ["habe", "hat", "hast"],
        "correct": "habe"
    },
    {
        "sentence": "Sie _____ sehr früh auf.",
        "options": ["stand", "stande", "steht"],
        "correct": "stand"
    },
    {
        "sentence": "Wir _____ den Weg nicht.",
        "options": ["kannten", "wussten", "wissen"],
        "correct": "kannten"
    },
    {
        "sentence": "Er _____ den Apfel in zwei Teile.",
        "options": ["schnitt", "schnittet", "schneidet"],
        "correct": "schnitt"
    },
    {
        "sentence": "Ich _____ gestern einen Film.",
        "options": ["sehe", "sah", "seht"],
        "correct": "sah"
    },
    {
        "sentence": "Sie _____ sehr schnell.",
        "options": ["liefe", "lief", "laufte"],
        "correct": "lief"
    },
    {
        "sentence": "Wir _____ die Aufgabe gemacht.",
        "options": ["haben", "habe", "hat"],
        "correct": "haben"
    },
    {
        "sentence": "Du _____ den Ball zu weit.",
        "options": ["warfst", "werfen", "warfen"],
        "correct": "warfst"
    },
    {
        "sentence": "Er _____ lange im Ausland.",
        "options": ["war", "ist", "wäre"],
        "correct": "war"
    },
    {
        "sentence": "Ich _____ ihm nicht.",
        "options": ["glaube", "glaubte", "glauben"],
        "correct": "glaubte"
    },
    {
        "sentence": "Sie _____ mir einen Brief.",
        "options": ["schrieb", "schreibt", "schreibte"],
        "correct": "schrieb"
    },
    {
        "sentence": "Wir _____ das Auto gestern.",
        "options": ["fuhren", "fahren", "fuhrt"],
        "correct": "fuhren"
    },
    {
        "sentence": "Du _____ die Antwort schon.",
        "options": ["kanntest", "kennst", "wissen"],
        "correct": "kanntest"
    },
    {
        "sentence": "Ich _____ das Fenster zu.",
        "options": ["machte", "machst", "machten"],
        "correct": "machte"
    },
    {
        "sentence": "Sie _____ nicht zu Hause.",
        "options": ["war", "ist", "seid"],
        "correct": "war"
    },
    {
        "sentence": "Wir _____ den ganzen Tag.",
        "options": ["arbeiteten", "arbeitete", "arbeitet"],
        "correct": "arbeiteten"
    },
    {
        "sentence": "Du _____ sehr viel.",
        "options": ["lernte", "lernst", "lerntest"],
        "correct": "lerntest"
    },
    {
        "sentence": "Er _____ mir das Buch.",
        "options": ["gab", "gebe", "gegeben"],
        "correct": "gab"
    },
    {
        "sentence": "Ich _____ meine Tasche verloren.",
        "options": ["habe", "hat", "hast"],
        "correct": "habe"
    }
]


# Hilfsfunktion, die eine zufällige Frage sendet
async def send_random_question(update: Update=None, context: ContextTypes.DEFAULT_TYPE=None):
    if "copy_questions" not in context.user_data:
        context.user_data["copy_questions"] = grammar_exercise.copy()    
    copy_questions = context.user_data.get("copy_questions") #Holt die lokale Fragenkopie.
    if not copy_questions: #Prüft, ob sie leer ist.
        await update.message.reply_text("🎉 All questions are answered!") #Wenn ja → Nachricht anzeigen und keine neue Frage senden. Wenn nicht → wie gehabt zufällig auswählen.
        return "end"

    q = random.choice(copy_questions)
    context.user_data["current_q"] = q
    opts = q["options"][:]   # Kopie der Optionen, [:] alles einschreiben
    random.shuffle(opts)     # mischen für Abwechslung
    kb = ReplyKeyboardMarkup([opts, ["Back","Reset"]], resize_keyboard=True)
    await update.message.reply_text(q["sentence"], reply_markup=kb)
        
    print(q["sentence"])
    print(q["options"][:3])

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    #Asynchrone Startfunktion, wird aufgerufen, wenn der User /start sendet.
    #Мы создали параметр update и вложили туда метод Update из библиотеки Python telegram bot
    # context:ContextTypes.DEFAULT_TYPE мы в переменную передадим контекст полученных сообщений и поддерживаем только дефолтные - текст и комманды
    context.user_data["copy_questions"] = grammar_exercise.copy()
    #Damit bekommt jeder Nutzer seine eigene Kopie der für den Nutzer editierbaren Fragenliste, wenn er /start verwendet.
    keyboard = [["Start", "Start training!"],["Contact me"]] #Definiert ein 2-spaltiges Tastenfeld mit zwei Buttons.
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    #Erzeugt eine benutzerdefinierte Tastatur mit den Buttons oben. resize_keyboard=True sorgt dafür, dass die Tastatur auf die Bildschirmgröße angepasst wird.
    await update.message.reply_text("Welcome and choose your action.", reply_markup=reply_markup)
    #Antwortet dem User mit dem Begrüßungstext und zeigt die Tastatur mit den Buttons an.

correct_count = 10
wrong_count = 0
    
async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
    #Funktion zum Verarbeiten beliebiger Textnachrichten, die nicht mit einem / anfangen (also keine Befehle sind).
    text = update.message.text
    #Speichert den Inhalt der empfangenen Nachricht in text.
    global correct_count
    context.user_data["correct_count"] = correct_count
    context.user_data["wrong_count"] = wrong_count
    correct = context.user_data["correct_count"]
    wrong = context.user_data["wrong_count"]    

    if text == "Start":
        await update.message.reply_text("Thanks for choosing Start.")
    elif text == "Start training!":
        training_keyboard = [["Choose exercises", "Help"],["Back"]]
        reply_markup_training = ReplyKeyboardMarkup(training_keyboard, resize_keyboard=True)
        await update.message.reply_text("Choose your actions", reply_markup=reply_markup_training)
    elif text == "Back":
        keyboard = [["Start", "Start training!"]] #Definiert ein 2-spaltiges Tastenfeld mit zwei Buttons.
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        #Erzeugt eine benutzerdefinierte Tastatur mit den Buttons oben. resize_keyboard=True sorgt dafür, dass die Tastatur auf die Bildschirmgröße angepasst wird.
        await update.message.reply_text("Welcome and choose your action.", reply_markup=reply_markup)
        #Antwortet dem User mit dem Begrüßungstext und zeigt die Tastatur mit den Buttons an.
    elif text == "Contact me":
        contact_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Contact me", url=f"https://t.me/{AUTHOR.lstrip('@')}")]])
        await update.message.reply_text("Click button in order to contact me.", reply_markup=contact_keyboard)

    elif text == "Choose exercises":
        exercise_keyboard = [["Grammar", "Vocabulary"],["Back"]]
        reply_markup_exercise = ReplyKeyboardMarkup(exercise_keyboard, resize_keyboard=True)
        await update.message.reply_text("Choose your actions", reply_markup=reply_markup_exercise)

    elif text == "Grammar":
        if "copy_questions" not in context.user_data:
            context.user_data["copy_questions"] = grammar_exercise.copy()

            await update.message.reply_text(f"Punktestand: ✅ {correct} | ❌ {wrong}")
            await send_random_question(update, context)
##        if not copy_questions:
##            correct = context.user_data.get("correct_count", 0)
##            wrong = context.user_data.get("wrong_count", 0)
##            await update.message.reply_text("🎉 All questions answered!")
##            await update.message.reply_text(f"🏁 Final state:\n✅ Correct: {correct}\n❌ Wrong: {wrong}")
##            return

    elif text == "Reset":
        context.user_data["copy_questions"] = grammar_exercise.copy()
        context.user_data["correct_count"] = 0
        context.user_data["wrong_count"] = 0   
        await update.message.reply_text("✅ Die Fragen wurden zurückgesetzt.")
        await send_random_question(update, context)
        
    elif context.user_data.get("current_q"):
        q = context.user_data["current_q"]
        if text == q["correct"]:
            await update.message.reply_text("✅ Richtig! Weiter so...")
##            context.user_data["correct_count"] += 1
            correct_count +=1
            context.user_data["copy_questions"].remove(q)
            await update.message.reply_text(f"Punktestand: ✅ {correct} | ❌ {wrong}")
            await send_random_question(update, context)  # nächste Frage
        elif text in q["options"]:
            await update.message.reply_text("❌ Falsch. Versuch’s nochmal.")
            context.user_data["wrong_count"] += 1
            await update.message.reply_text(f"Punktestand: ✅ {correct} | ❌ {wrong}")            


    else:
        await update.message.reply_text("Ich habe dich nicht verstanden. Wähle bitte eine Option.")        
        
        

def main():
    #Hauptfunktion, die den Bot initialisiert und startet.
    application = Application.builder().token(TOKEN).build()
    # Wir rufen mit unserer Methode die Methode der Bibliothek auf, dann Methode builder, uebergeben den Token und rufen die Methode build auf
    application.add_handler(CommandHandler("start", start)) #Добавляет обработчик, через метод CommandHandler стартует работа бота
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) #обработка сообщений пользователя
    application.run_polling()
main()
