import matplotlib.pyplot as plt

# Leer datos de las listas guardadas
with open("datos_graficas.txt", "r") as f:
    exec(f.read())

# Crear figura y ejes para los subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Graficar supervivientes por generación
axs[0, 0].plot(supervivientes_por_generacion, marker='o')
axs[0, 0].set_title('Supervivientes (ganadores) por Generación')
axs[0, 0].set_xlabel('Generación')
axs[0, 0].set_ylabel('Número de Supervivientes')
axs[0, 0].grid(True)

# Graficar hijos generados por generación
axs[0, 1].plot(hijos_generados_por_generacion, marker='o', color='g')
axs[0, 1].set_title('Hijos Generados por Generación')
axs[0, 1].set_xlabel('Generación')
axs[0, 1].set_ylabel('Número de Hijos Generados')
axs[0, 1].grid(True)

# Graficar asesinados por generación
axs[1, 0].plot(asesinados_por_generacion, marker='o', color='r')
axs[1, 0].set_title('eliminados por Generación')
axs[1, 0].set_xlabel('Generación')
axs[1, 0].set_ylabel('Número de eliminados')
axs[1, 0].grid(True)

# Graficar media de la probabilidad a la derecha por generación
axs[1, 1].plot(media_probabilidad_derecha_por_generacion, marker='o', color='m')
axs[1, 1].set_title('Media de la Probabilidad a la Derecha por Generación')
axs[1, 1].set_xlabel('Generación')
axs[1, 1].set_ylabel('Media de la Probabilidad a la Derecha')
axs[1, 1].grid(True)

# Ajustar diseño y mostrar gráficos
plt.tight_layout()
plt.savefig('graficas.png')
plt.show()
