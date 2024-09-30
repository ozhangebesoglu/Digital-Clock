from tkinter import *
from tkinter.font import Font
from tkinter import colorchooser, simpledialog, messagebox
import time
import pystray
from PIL import Image, ImageDraw
import sys
import threading
import winsound  # Alarm sesi için

# Sistem tepsisi simgesi oluşturma
def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle([(10, 10), (width - 10, height - 10)], fill=(0, 0, 0))
    return image

def on_quit(icon, item):
    icon.stop()
    app_window.quit()  # Tkinter uygulamasını kapat

# Sistem tepsisi simgesi
icon = pystray.Icon("clock", create_image(), "Digital Clock", menu=pystray.Menu(
    pystray.MenuItem("Renk Değiştir", lambda: change_text_color()),
    pystray.MenuItem("Alarm Kur", lambda: set_alarm()),
    pystray.MenuItem("Çıkış", on_quit)
))

def setup_tray_icon():
    icon.run_detached()

# Alarm kurma fonksiyonu
def set_alarm():
    alarm_time = simpledialog.askstring("Alarm Kur", "Alarm zamanı giriniz (Saat ve Dakika)")
    if alarm_time:
        threading.Thread(target=check_alarm, args=(alarm_time,), daemon=True).start()

# Alarm kontrolü ve ses çalma
def check_alarm(alarm_time):
    while True:
        current_time = time.strftime('%H:%M')
        if current_time == alarm_time:
            play_alarm_sound()
            messagebox.showinfo("Alarm", "Alarm!")
            break
        time.sleep(1)

# Alarm sesi çalma
def play_alarm_sound():
    duration = 2000  # 2 saniye
    freq = 440  # Ses frekansı (440Hz bir "A" notasını temsil eder)
    winsound.Beep(freq, duration)

# Tkinter penceresi oluşturma
app_window = Tk()
app_window.title("Digital Clock")
app_window.overrideredirect(1)  # Pencere başlığını gizle
app_window.geometry("300x300")  # Pencere boyutu
app_window.resizable(0, 0)

# Transparan renk olarak '#2D353B' ayarladık
gray_color = '#2D353B'
app_window.config(bg=gray_color)
app_window.wm_attributes('-transparentcolor', gray_color)

text_font = Font(
    family= "Cascadia Code",
    size=36,
    weight='bold'
)
background = gray_color
foreground = 'white'
border_width = 10

# Pencereyi hareket ettirmek için gerekli fonksiyonlar
def start_move(event):
    app_window.x = event.x_root  # Global X koordinatı
    app_window.y = event.y_root  # Global Y koordinatı

def move_window(event):
    # Pencerenin yeni pozisyonunu hesapla
    x = event.x_root - app_window.x
    y = event.y_root - app_window.y
    app_window.geometry(f'+{app_window.winfo_x() + x}+{app_window.winfo_y() + y}')

    # Başlangıç koordinatlarını güncelle
    app_window.x = event.x_root
    app_window.y = event.y_root

# Pencereyi tüm alanda sürüklenebilir yapmak için bağlama
app_window.bind("<Button-1>", start_move)
app_window.bind("<B1-Motion>", move_window)

# Renk seçici fonksiyonu
def change_text_color():
    color = colorchooser.askcolor(title="Rengi Seçiniz")
    if color[1]:  # Kullanıcı bir renk seçtiyse
        label.config(fg=color[1])
        date_label.config(fg=color[1])

# Sağ tık menüsü oluşturma
def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

# Uygulamayı kapatma fonksiyonu
def close_app():
    icon.stop()  # Sistem tepsisindeki simgeyi durdur
    app_window.quit()  # Tkinter uygulamasını kapat




# Sağ tık menüsü oluşturma
context_menu = Menu(app_window, tearoff=0)
context_menu.add_command(label="Renk Değiştir", command=change_text_color)  # Renk değiştirme seçeneği
context_menu.add_command(label="Alarm Kur", command=set_alarm)  # Alarm kurma seçeneği
context_menu.add_command(label="Kapat", command=close_app) # Uygulamayı kapatma seçeneği

# Sağ tıklama menüsünü fare sağ tuşuna bağla
app_window.bind("<Button-3>", show_context_menu)

def digital_clock():
    time_live = time.strftime('%H:%M:%S')
    date_live = time.strftime('%d/%m/%Y')
    label.config(text=time_live)
    date_label.config(text=date_live)
    app_window.after(200, digital_clock)

# Saat etiketi
label = Label(app_window, font=text_font, bg=background, fg=foreground, bd=border_width)
label.place(relx=0.5, rely=0.25, anchor=CENTER)

# Tarih etiketi
date_label = Label(app_window, font=text_font, bg=background, fg=foreground, bd=border_width)
date_label.place(relx=0.5, rely=0.5, anchor=CENTER)

digital_clock()

# Sistem tepsisi simgesini başlatma
setup_tray_icon()

app_window.mainloop()