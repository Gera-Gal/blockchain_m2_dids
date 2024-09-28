import tkinter as tk
from tkinter import filedialog, messagebox
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image, ImageTk #, ImageOps, ImageFilter  # Para manejar imágenes
import pytesseract
import pymongo
import cv2

import requests
from dotenv import load_dotenv
import os

# Configuración de Tesseract (Asegúrate de cambiar la ruta si es necesario)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Conexión a MongoDB
MONGODB_URI = "mongodb+srv://geragal23:LCbU6JNeIaOLVMH9@cluster0.ywx5lpa.mongodb.net/blockchain?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(MONGODB_URI)
db = client["blockchain"]
users_collection = db["usuarios"]
dids_collection = db["dids"]

# Variable global para el contador
contador = "name6"

# Función de autenticación
def autenticar_usuario(username, password):
    user = users_collection.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        return True
    return False

# Ventana de autenticación
def ventana_login():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("500x400")

    # Cargar la imagen de fondo
    bg_image_login = Image.open("man_fingerprint.png")  # Reemplaza con la ruta de tu imagen de fondo
    bg_image_login = bg_image_login.resize((500, 400), Image.Resampling.LANCZOS)  # Redimensionar si es necesario
    bg_image_login = ImageTk.PhotoImage(bg_image_login)

    # Crear un canvas para colocar la imagen de fondo
    canvas = tk.Canvas(login_window, width=500, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_image_login)

    # Etiquetas y campos de entrada para login
    label_usuario = tk.Label(login_window, text="Usuario", font=("Helvetica", 12), bg="white")
    label_usuario.place(x=180, y=150)
    entry_usuario = tk.Entry(login_window, font=("Helvetica", 12))
    entry_usuario.place(x=180, y=180)

    label_password = tk.Label(login_window, text="Contraseña", font=("Helvetica", 12), bg="white")
    label_password.place(x=180, y=210)
    entry_password = tk.Entry(login_window, show="*", font=("Helvetica", 12))
    entry_password.place(x=180, y=240)

    def iniciar_sesion():
        username = entry_usuario.get()
        password = entry_password.get()

        if autenticar_usuario(username, password):
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            login_window.destroy()  # Cierra la ventana de login
            ventana_principal()  # Muestra la ventana principal
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    btn_login = tk.Button(login_window, text="Iniciar sesión", command=iniciar_sesion, font=("Helvetica", 12))
    btn_login.place(x=220, y=280)
    
    login_window.mainloop()

# Función para abrir la ventana principal (Carga documental y biométrica)
def ventana_principal():
    global contador

    # Función para crear DID en polygon
    def crear_did(name):
        load_dotenv()

        tatum_api_key = os.getenv("TATUM_API_KEY")
        private_key = os.getenv("PRIVATE_KEY")

        url = "https://api.tatum.io/v3/polygon/smartcontract"

        payload = {
        "contractAddress": "0xE13D6ED71e86135CbbC60A0cb8659b0EAa758488",
        "methodName": "createDID",
        "methodABI": {
            "constant": "false",
            "inputs": [
            { "name": "did", "type": "string" },
            { "name": "metadata", "type": "string" }
            ],
            "name": "createDID",
            "outputs": [],
            "payable": "false",
            "stateMutability": "nonpayable",
            "type": "function"
        },
        "params": [f"did:0xE835e17D3276c14554014d5F96eb90672d73b201:{contador}", name],
        "fromPrivateKey": private_key
        }

        headers = {
            "x-api-key": tatum_api_key,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            transaction_id = result.get("txId", "No transaction ID found")
            """ num = int(contador[-1])
            contador = contador[0:-1] + str(num + 1)
            db.dids.update({
                "field": "name",
                "$set": {
                    "value": contador
                }
            }) """
            return transaction_id
        else:
            return f"Error en la solicitud: {response.status_code} - {response.text}"

    # Función para extraer texto de una imagen utilizando Tesseract
    def cargar_documento():
        file_path = filedialog.askopenfilename(filetypes=[("Imagen PNG", "*.png"), ("Imagen JPEG", "*.jpeg"), ("Imagen JPG", "*.jpg")])
        if file_path:
            try:
                # Extraer texto usando Tesseract OCR
                config = '-l spa'
                image = Image.open(file_path)
                """ gray_image = ImageOps.grayscale(image)
                scale_factor = 2
                resized_image = gray_image.resize(
                    (gray_image.width * scale_factor, gray_image.height * scale_factor),
                    resample=Image.LANCZOS
                )
                thresholded_image = resized_image.filter(ImageFilter.FIND_EDGES)
                thresholded_image.show() """
                text = pytesseract.image_to_string(image, config=config)
                # Guardar texto extraído en un archivo de texto
                with open("documento_extraido.txt", "w", encoding="utf-8") as f:
                    f.write(text)

                #Buscar nombre en el texto
                lines = text.split('\n')
                name = ""
                state = "none"
                for counter in range(len(lines)):
                    if "NOMBRE" in lines[counter]:
                        state = "surname1"
                        continue
                    if state == "surname1" and lines[counter] != "\n":
                        name += lines[counter].split(" ")[0] + " "
                        state = "surname2"
                        continue
                    if state == "surname2" and lines[counter] != "\n":
                        name += lines[counter].split(" ")[0] + " "
                        state = "name"
                        continue
                    if state == "name" and lines[counter] != "\n":
                        name = lines[counter].split(" ")[0] + " " + name
                        break
                #print(f"Nombre extraído: {name}")
                result = crear_did(name)
                if result.split(" ")[0] == "Error":
                    messagebox.showerror("Error", result)
                else:
                    text_resultado.config(state=tk.NORMAL)  # Permite editar el Text widget
                    text_resultado.delete(1.0, tk.END)  # Limpia el contenido previo
                    text_resultado.insert(tk.END, f"Aquí está tu hash: {result}")  # Inserta el hash
                    text_resultado.tag_add("underline", 1.16, tk.END)  # Subraya solo el hash
                    text_resultado.config(state=tk.DISABLED)  # Desactiva la edición
                    messagebox.showinfo("Éxito", f'Transacción exitosa.')
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar el documento: {str(e)}")

    # Función para procesar imagen biométrica utilizando OpenCV
    def cargar_biometrico():
        file_path = filedialog.askopenfilename(filetypes=[("Imagen PNG", "*.png"), ("Imagen JPEG", "*.jpeg"), ("Imagen JPG", "*.jpg")])
        if file_path:
            try:
                # Cargar imagen usando OpenCV
                img = cv2.imread(file_path)
                # Convertir a escala de grises
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Detectar rostros usando Haar Cascades
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if len(faces) == 0:
                    messagebox.showinfo("Información", "No se detectaron rostros en la imagen.")
                else:
                    # Dibujar rectángulos en los rostros detectados
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

                    # Mostrar imagen con detección de rostros
                    cv2.imshow("Rostros detectados", img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar la imagen biométrica: {str(e)}")

    root = tk.Tk()
    root.title("Identificadores descentralizados")
    root.geometry("500x450")
    
    # Etiqueta de título
    label_title = tk.Label(root, text="Identificadores descentralizados", font=("Helvetica", 16, "bold"))
    label_title.pack(pady=20)

    # Etiqueta de frase de cabecera
    label_subtitle = tk.Label(root, text="Elije el tipo de datos que deseas registrar", font=("Helvetica", 12))
    label_subtitle.pack(pady=10)

    # Botón para carga documental
    btn_documental = tk.Button(root, text="Carga documental", width=20, command=cargar_documento)
    btn_documental.pack(pady=10)

    # Botón para carga biométrica
    btn_biometrico = tk.Button(root, text="Carga biométrica", width=20, command=cargar_biometrico)
    btn_biometrico.pack(pady=10)

    # Crear un Text widget para mostrar el resultado del hash del NFT
    text_resultado = tk.Text(root, height=3, width=50)
    text_resultado.pack(pady=20)
    text_resultado.tag_configure("underline", underline=True)  # Configura el subrayado
    text_resultado.config(state=tk.DISABLED)  # Desactiva la edición inicialmente

    # Función para copiar hash
    def copy_to_clipboard():
        """Copy current contents of text_entry to clipboard."""
        root.clipboard_clear()  # Optional.
        resultado = text_resultado.get('1.0', tk.END).rstrip()
        root.clipboard_append(resultado.split(' ')[4])
        messagebox.showinfo("Resultado", "Se copió el hash al clipboard")

    # Copiar el hash de resultado
    clp = tk.Button(root, text="Copiar resultado", command=copy_to_clipboard, width=20, height=2)
    clp.pack(pady=10)

    # Función para cerrar sesión
    def cerrar_sesion():
        root.destroy()  # Cerrar la ventana principal
        ventana_login()  # Volver a la ventana de login
    
    # Botón de logout
    btn_logout = tk.Button(root, text="Cerrar sesión", width=20, command=cerrar_sesion)
    btn_logout.pack(pady=20)

    # Iniciar la aplicación
    root.mainloop()

# Iniciar aplicación con la ventana de login
ventana_login()