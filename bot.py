import telebot
from telebot import types

BOT_TOKEN = ""

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start']) #receiving /start
def start(message):
    chat_id = message.chat.id; client_first_name = message.from_user.first_name
    print(f"{client_first_name} ({chat_id}) deu /start no @d2is_cliques_bot")
    
    bot.send_message(chat_id, f"<i>Bem-vindo, <b>{client_first_name}</b>!</i>", reply_markup=main_menu_markup())

@bot.callback_query_handler(lambda call: call.data == "main_menu")
def main_menu(call):
    chat_id = call.message.chat.id; message_id = call.message.message_id
    
    bot.send_message(chat_id, f"<i>Selecione uma das opções abaixo</i>", reply_markup=main_menu_markup())
    bot.delete_message(chat_id, message_id)

def main_menu_markup():
    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton("Galeria de fotos", callback_data="photo_gallery, 0"))
    markup_inline.add(types.InlineKeyboardButton("Proposta de ensaio", callback_data="photo_essay_proposal, 0"))
    markup_inline.add(types.InlineKeyboardButton("Quem somos", callback_data="about_us, 0"))
    return markup_inline

@bot.callback_query_handler(lambda call: "photo_gallery" in call.data)
def photo_gallery(call):
    chat_id = call.message.chat.id; photo_id = int(((call.data).split(", "))[1])
    photo_name_list = ["0","1","2","3","4","5","6","7","8","9"]

    if photo_id < 0: photo_id = len(photo_name_list)-1
    if photo_id >= len(photo_name_list): photo_id = 0

    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton("<-- Anterior", callback_data=f"photo_gallery, {photo_id-1}"), types.InlineKeyboardButton("Próximo -->", callback_data=f"photo_gallery, {photo_id+1}"))
    markup_inline.add(types.InlineKeyboardButton("Voltar", callback_data="main_menu"))

    bot.send_photo(chat_id, photo=open(f'./assets/gallery/{photo_name_list[photo_id]}.jpg', 'rb'), reply_markup=markup_inline)
    bot.delete_message(chat_id, call.message.message_id)
    # bot.edit_message_media(chat_id=chat_id, media=types.InputMediaPhoto(f"./images/{photo_name_list[photo_id]}.jpg"), message_id=call.message.message_id)

@bot.callback_query_handler(lambda call: "photo_essay_proposal" in call.data)
def photo_essay_proposal(call):
    chat_id = call.message.chat.id; package_id = int(((call.data).split(", "))[1])
    package_list = [{"type": "Básico", "price": 300, "extra_photo_price": 18, "num_photos": 10, "duration": 100, "num_looks": 2, "num_locations": 1, "makeup": False, "hair": False}, {"type": "Na medida", "price": 380, "extra_photo_price": 12, "num_photos": 20, "duration": 130, "num_looks": 2, "num_locations": 1, "makeup": True, "hair": False}, {"type": "Completo", "price": 450, "extra_photo_price": 9, "num_photos": 30, "duration": 200, "num_looks": 2, "num_locations": 2, "makeup": True, "hair": True}]
    
    if package_id < 0: package_id = len(package_list)-1
    if package_id >= len(package_list): package_id = 0
    
    package = package_list[package_id]
    makeup_value = "\U00002705" if package.get('makeup') == True else "\U0000274C"; hair_value = "\U00002705" if package.get('hair') == True else "\U0000274C"

    package_msg = f"<b>—-—-—-—-—-— {(str(package.get('type'))).upper()} —-—-—-—-—-—</b>\n\n- Duração: <b>{package.get('duration')} min.</b>\n- Quant. de fotos: <b>{package.get('num_photos')}</b>\n- Quant. de locais: <b>{package.get('num_locations')}</b>\n- Quant. de looks: <b>{package.get('num_looks')}</b>\n- Maquiagem: {makeup_value}\n- Cabelo: {hair_value}\n\n- Preço da foto extra: <b>R$ {package.get('extra_photo_price')}</b> \n- Preço: <b>R$ {package.get('price')}</b>"
    
    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton("<-- Anterior", callback_data=f"photo_essay_proposal, {package_id-1}"), types.InlineKeyboardButton("Escolher", callback_data=f"null"), types.InlineKeyboardButton("Próximo -->", callback_data=f"photo_essay_proposal, {package_id+1}"))
    markup_inline.add(types.InlineKeyboardButton("Voltar", callback_data="main_menu"))

    bot.edit_message_text(f"{package_msg}\n\n<i>Escolha dentre os nossos pacotes de fotos o que mais se encaixa com você.</i>", chat_id=chat_id,message_id=call.message.message_id, reply_markup=markup_inline)

@bot.callback_query_handler(lambda call: "about_us" in call.data)
def about_us(call):
    chat_id = call.message.chat.id; about_id = int(((call.data).split(", "))[1])
    about_list = [{"photo_name": "d2is", "instagram": "https://www.instagram.com/d2is.cliques/", "facebook": "https://www.facebook.com/d2is.cliques", "website": "http://www.d2iscliques.cf/", "caption": "Se quiser entrar em contato com a para tirar alguma dúvida ou fazer alguma sugestão, você pode enviar um email para d2is.cliques@gmail.com ou clicar em um dos botões abaixo"}, {"photo_name": "vinicius", "instagram": "https://www.instagram.com/antonio_vmoura/", "facebook": "https://www.facebook.com/avmoura.r/", "telegram": "https://t.me/antonio_vmoura", "caption": "Me chamo Antônio Vinicius tenho 20 anos e estou cursando ciência da computação na UnB. Sempre curti utilizar de maneira distraída ferramentas de design. Hoje me aprofundo em tais ferramentas junto de técnicas fotograficas de maneira profissional."}, {"photo_name": "henrique", "instagram": "https://www.instagram.com/tonirrau/", "facebook": "https://www.facebook.com/tonirrau", "telegram": "https://t.me/tonirrau", "caption": "Me chamo Antônio Henrique, tenho 26 anos. Apaixonado por tecnologia e com uma certa inclinação para a área de softwares de computadores, acabei conhecendo o Photoshop, que foi minha entrada no mundo fotográfico. Daí surgiu a vontade por fotografar."}]

    if about_id < 0: about_id = len(about_list)-1
    if about_id >= len(about_list): about_id = 0

    about = about_list[about_id]
    markup_inline = types.InlineKeyboardMarkup()

    if about.get('photo_name') == "d2is":
        markup_inline.add(types.InlineKeyboardButton(text = "Instagram", url=f"{about.get('instagram')}"), types.InlineKeyboardButton(text = "Facebook", url=f"{about.get('facebook')}"), types.InlineKeyboardButton(text = "Site", url=f"{about.get('website')}"))
    else:
        markup_inline.add(types.InlineKeyboardButton(text = "Instagram", url=f"{about.get('instagram')}"), types.InlineKeyboardButton(text = "Facebook", url=f"{about.get('facebook')}"), types.InlineKeyboardButton(text = "Telegram", url=f"{about.get('telegram')}"))

    markup_inline.add(types.InlineKeyboardButton("<-- Anterior", callback_data=f"about_us, {about_id-1}"), types.InlineKeyboardButton("Próximo -->", callback_data=f"about_us, {about_id+1}"))
    markup_inline.add(types.InlineKeyboardButton("Voltar", callback_data="main_menu"))

    bot.send_photo(chat_id, photo=open(f"./assets/about/{about.get('photo_name')}.jpg", "rb"),  caption =f"{about.get('caption')}", reply_markup=markup_inline)
    bot.delete_message(chat_id, call.message.message_id)

bot.polling(none_stop=True, interval=0, timeout=15)