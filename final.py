"""
Scrapping Version 3.0
"""
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
import requests

class Usuario:
    """ID del usuario para su busqueda"""
    def __init__(self, id_user):
        self.id_user=id_user

    def return_id(self):
        """retorna la ID del usuario"""
        id_usuario=self.id_user
        return id_usuario

    def buscar_datos(self):
        """Se buscan los datos del usuario en stackoverflow"""
        url = f'https://es.stackoverflow.com/users/{self.id_user}?tab=tags'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Scrapping de etiquetas
        etq = soup.find_all('a', class_='post-tag')
        frec = soup.find_all('td')

        # lista etiqueta
        etiquetas = list()
        for i in etq:
            etiquetas.append(i.text)

        # Eliminacion de etiqueta repetida inicial
        if etiquetas[0] == etiquetas[1]:
            etiquetas.pop(0)

        # lista frecuencia de etiquetas
        frecuencia = list()
        for i in frec:
            if i.text[-1:] != '\n':
                if i.text[-4].isdigit() == 1:
                    frecuencia.append(int(i.text[-4:]))
                elif i.text[-3].isdigit() == 1:
                    frecuencia.append(int(i.text[-3:]))
                else:
                    frecuencia.append(int(i.text[-2:]))
            else:
                frecuencia.append(1)
        print(frecuencia)

        # Aquí utilizamos zip para unir las etiquetas con sus repsectivas frecuencias
        etfrecuencias = dict(zip(etiquetas, frecuencia))
        print(etfrecuencias)
        return etfrecuencias

class WC(Usuario):
    """ID del usuario para su busqueda"""
    def __init__(self, id_user):
        Usuario.__init__(self, id_user)

    def crear_wc(self):
        """Se crea y guarda la imagen del WC"""
        cloud = WordCloud(background_color="black", contour_width=1, contour_color='steelblue')\
            .generate_from_frequencies(self.id_user.buscar_datos())
        cloud.to_file('wcloud.png')
        return cloud

    def mostrar_wc(self):
        """Se muestra el WC"""
        plt.figure()
        plt.title("user: " + self.id_user.return_id())
        plt.imshow(self.crear_wc(), interpolation= "bilinear")
        plt.axis('off')
        plt.show()

print("Introduzca la ID del usuario: ")
IDusuario= input()
user_=Usuario(IDusuario)
Nube=WC(user_)
Nube.mostrar_wc()
