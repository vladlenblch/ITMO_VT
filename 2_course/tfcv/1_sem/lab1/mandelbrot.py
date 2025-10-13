import numpy as np
import matplotlib.pyplot as plt # type: ignore

def mandelbrot(c, max_iter):
    z = np.zeros_like(c, dtype=np.complex128)
    diverge = np.zeros(c.shape, dtype=bool)  # Отслеживает какие точки уже разошлись
    iterations = np.zeros(c.shape, dtype=int)  # Хранит количество итераций
    
    for i in range(max_iter):
        mask = ~diverge  # Работаем только с точками, которые еще не разошлись
        z[mask] = z[mask]**2 + c[mask]  # Основная формула Мандельброта
        
        new_diverge = np.abs(z) > 2  # Точки, которые разошлись на этой итерации
        diverge_now = new_diverge & ~diverge  # Точки, которые только что разошлись
        iterations[diverge_now] = i  # Записываем номер итерации расхождения
        diverge = diverge | new_diverge  # Обновляем маску расходимости
        
    return iterations

def show_mandelbrot_25_iterations():
    max_iter = 25
    
    # Создаем фигуру с тремя подграфиками
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    
    # Основной вид
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    width, height = 400, 400
    
    # Создаем сетку комплексных чисел
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y  # Комплексная плоскость
    
    # Вычисляем множество Мандельброта
    iterations = mandelbrot(C, max_iter)
    
    # Визуализация основного вида
    im1 = ax1.imshow(iterations, extent=[x_min, x_max, y_min, y_max], 
                    cmap='hot', origin='lower')
    ax1.set_title('Множество Мандельброта\n25 итераций - Основной вид')
    ax1.set_xlabel('Re(c)')
    ax1.set_ylabel('Im(c)')
    plt.colorbar(im1, ax=ax1, label='Количество итераций')
    
    # ПРИБЛИЖЕНИЕ 1: Фрактальные ветви
    x_min_zoom1, x_max_zoom1 = -0.6, -0.4
    y_min_zoom1, y_max_zoom1 = -0.7, -0.5
    
    x_zoom1 = np.linspace(x_min_zoom1, x_max_zoom1, width)
    y_zoom1 = np.linspace(y_min_zoom1, y_max_zoom1, height)
    X_zoom1, Y_zoom1 = np.meshgrid(x_zoom1, y_zoom1)
    C_zoom1 = X_zoom1 + 1j * Y_zoom1
    
    iterations_zoom1 = mandelbrot(C_zoom1, max_iter)
    
    im2 = ax2.imshow(iterations_zoom1, extent=[x_min_zoom1, x_max_zoom1, y_min_zoom1, y_max_zoom1], 
                    cmap='hot', origin='lower')
    ax2.set_title('Множество Мандельброта\n25 итераций - Фрактальные ветви')
    ax2.set_xlabel('Re(c)')
    ax2.set_ylabel('Im(c)')
    plt.colorbar(im2, ax=ax2, label='Количество итераций')
    
    # ПРИБЛИЖЕНИЕ 2: Верхний кластер
    x_min_zoom2, x_max_zoom2 = -0.1, 0.1
    y_min_zoom2, y_max_zoom2 = 0.6, 0.8
    
    x_zoom2 = np.linspace(x_min_zoom2, x_max_zoom2, width)
    y_zoom2 = np.linspace(y_min_zoom2, y_max_zoom2, height)
    X_zoom2, Y_zoom2 = np.meshgrid(x_zoom2, y_zoom2)
    C_zoom2 = X_zoom2 + 1j * Y_zoom2
    
    iterations_zoom2 = mandelbrot(C_zoom2, max_iter)
    
    im3 = ax3.imshow(iterations_zoom2, extent=[x_min_zoom2, x_max_zoom2, y_min_zoom2, y_max_zoom2], 
                    cmap='hot', origin='lower')
    ax3.set_title('Множество Мандельброта\n25 итераций - Верхний кластер')
    ax3.set_xlabel('Re(c)')
    ax3.set_ylabel('Im(c)')
    plt.colorbar(im3, ax=ax3, label='Количество итераций')
    
    plt.tight_layout()
    plt.show()

def show_mandelbrot_50_iterations():
    max_iter = 50
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    
    # Основной вид
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    width, height = 400, 400
    
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    iterations = mandelbrot(C, max_iter)
    
    im1 = ax1.imshow(iterations, extent=[x_min, x_max, y_min, y_max], 
                    cmap='hot', origin='lower')
    ax1.set_title('Множество Мандельброта\n50 итераций - Основной вид')
    ax1.set_xlabel('Re(c)')
    ax1.set_ylabel('Im(c)')
    plt.colorbar(im1, ax=ax1, label='Количество итераций')
    
    # Приближение 1: Фрактальные ветви
    x_min_zoom1, x_max_zoom1 = -0.6, -0.4
    y_min_zoom1, y_max_zoom1 = -0.7, -0.5
    
    x_zoom1 = np.linspace(x_min_zoom1, x_max_zoom1, width)
    y_zoom1 = np.linspace(y_min_zoom1, y_max_zoom1, height)
    X_zoom1, Y_zoom1 = np.meshgrid(x_zoom1, y_zoom1)
    C_zoom1 = X_zoom1 + 1j * Y_zoom1
    
    iterations_zoom1 = mandelbrot(C_zoom1, max_iter)
    
    im2 = ax2.imshow(iterations_zoom1, extent=[x_min_zoom1, x_max_zoom1, y_min_zoom1, y_max_zoom1], 
                    cmap='hot', origin='lower')
    ax2.set_title('Множество Мандельброта\n50 итераций - Фрактальные ветви')
    ax2.set_xlabel('Re(c)')
    ax2.set_ylabel('Im(c)')
    plt.colorbar(im2, ax=ax2, label='Количество итераций')
    
    # Приближение 2: Верхний кластер
    x_min_zoom2, x_max_zoom2 = -0.1, 0.1
    y_min_zoom2, y_max_zoom2 = 0.6, 0.8
    
    x_zoom2 = np.linspace(x_min_zoom2, x_max_zoom2, width)
    y_zoom2 = np.linspace(y_min_zoom2, y_max_zoom2, height)
    X_zoom2, Y_zoom2 = np.meshgrid(x_zoom2, y_zoom2)
    C_zoom2 = X_zoom2 + 1j * Y_zoom2
    
    iterations_zoom2 = mandelbrot(C_zoom2, max_iter)
    
    im3 = ax3.imshow(iterations_zoom2, extent=[x_min_zoom2, x_max_zoom2, y_min_zoom2, y_max_zoom2], 
                    cmap='hot', origin='lower')
    ax3.set_title('Множество Мандельброта\n50 итераций - Верхний кластер')
    ax3.set_xlabel('Re(c)')
    ax3.set_ylabel('Im(c)')
    plt.colorbar(im3, ax=ax3, label='Количество итераций')
    
    plt.tight_layout()
    plt.show()

def show_mandelbrot_100_iterations():
    max_iter = 100
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    
    # Основной вид
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    width, height = 400, 400
    
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    iterations = mandelbrot(C, max_iter)
    
    im1 = ax1.imshow(iterations, extent=[x_min, x_max, y_min, y_max], 
                    cmap='hot', origin='lower')
    ax1.set_title('Множество Мандельброта\n100 итераций - Основной вид')
    ax1.set_xlabel('Re(c)')
    ax1.set_ylabel('Im(c)')
    plt.colorbar(im1, ax=ax1, label='Количество итераций')
    
    # Приближение 1: Фрактальные ветви
    x_min_zoom1, x_max_zoom1 = -0.6, -0.4
    y_min_zoom1, y_max_zoom1 = -0.7, -0.5
    
    x_zoom1 = np.linspace(x_min_zoom1, x_max_zoom1, width)
    y_zoom1 = np.linspace(y_min_zoom1, y_max_zoom1, height)
    X_zoom1, Y_zoom1 = np.meshgrid(x_zoom1, y_zoom1)
    C_zoom1 = X_zoom1 + 1j * Y_zoom1
    
    iterations_zoom1 = mandelbrot(C_zoom1, max_iter)
    
    im2 = ax2.imshow(iterations_zoom1, extent=[x_min_zoom1, x_max_zoom1, y_min_zoom1, y_max_zoom1], 
                    cmap='hot', origin='lower')
    ax2.set_title('Множество Мандельброта\n100 итераций - Фрактальные ветви')
    ax2.set_xlabel('Re(c)')
    ax2.set_ylabel('Im(c)')
    plt.colorbar(im2, ax=ax2, label='Количество итераций')
    
    # Приближение 2: Верхний кластер
    x_min_zoom2, x_max_zoom2 = -0.1, 0.1
    y_min_zoom2, y_max_zoom2 = 0.6, 0.8
    
    x_zoom2 = np.linspace(x_min_zoom2, x_max_zoom2, width)
    y_zoom2 = np.linspace(y_min_zoom2, y_max_zoom2, height)
    X_zoom2, Y_zoom2 = np.meshgrid(x_zoom2, y_zoom2)
    C_zoom2 = X_zoom2 + 1j * Y_zoom2
    
    iterations_zoom2 = mandelbrot(C_zoom2, max_iter)
    
    im3 = ax3.imshow(iterations_zoom2, extent=[x_min_zoom2, x_max_zoom2, y_min_zoom2, y_max_zoom2], 
                    cmap='hot', origin='lower')
    ax3.set_title('Множество Мандельброта\n100 итераций - Верхний кластер')
    ax3.set_xlabel('Re(c)')
    ax3.set_ylabel('Im(c)')
    plt.colorbar(im3, ax=ax3, label='Количество итераций')
    
    plt.tight_layout()
    plt.show()

def show_mandelbrot_200_iterations():
    max_iter = 200
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    
    # Основной вид
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    width, height = 400, 400
    
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    iterations = mandelbrot(C, max_iter)
    
    im1 = ax1.imshow(iterations, extent=[x_min, x_max, y_min, y_max], 
                    cmap='hot', origin='lower')
    ax1.set_title('Множество Мандельброта\n200 итераций - Основной вид')
    ax1.set_xlabel('Re(c)')
    ax1.set_ylabel('Im(c)')
    plt.colorbar(im1, ax=ax1, label='Количество итераций')
    
    # Приближение 1: Фрактальные ветви
    x_min_zoom1, x_max_zoom1 = -0.6, -0.4
    y_min_zoom1, y_max_zoom1 = -0.7, -0.5
    
    x_zoom1 = np.linspace(x_min_zoom1, x_max_zoom1, width)
    y_zoom1 = np.linspace(y_min_zoom1, y_max_zoom1, height)
    X_zoom1, Y_zoom1 = np.meshgrid(x_zoom1, y_zoom1)
    C_zoom1 = X_zoom1 + 1j * Y_zoom1
    
    iterations_zoom1 = mandelbrot(C_zoom1, max_iter)
    
    im2 = ax2.imshow(iterations_zoom1, extent=[x_min_zoom1, x_max_zoom1, y_min_zoom1, y_max_zoom1], 
                    cmap='hot', origin='lower')
    ax2.set_title('Множество Мандельброта\n200 итераций - Фрактальные ветви')
    ax2.set_xlabel('Re(c)')
    ax2.set_ylabel('Im(c)')
    plt.colorbar(im2, ax=ax2, label='Количество итераций')
    
    # Приближение 2: Верхний кластер
    x_min_zoom2, x_max_zoom2 = -0.1, 0.1
    y_min_zoom2, y_max_zoom2 = 0.6, 0.8
    
    x_zoom2 = np.linspace(x_min_zoom2, x_max_zoom2, width)
    y_zoom2 = np.linspace(y_min_zoom2, y_max_zoom2, height)
    X_zoom2, Y_zoom2 = np.meshgrid(x_zoom2, y_zoom2)
    C_zoom2 = X_zoom2 + 1j * Y_zoom2
    
    iterations_zoom2 = mandelbrot(C_zoom2, max_iter)
    
    im3 = ax3.imshow(iterations_zoom2, extent=[x_min_zoom2, x_max_zoom2, y_min_zoom2, y_max_zoom2], 
                    cmap='hot', origin='lower')
    ax3.set_title('Множество Мандельброта\n200 итераций - Верхний кластер')
    ax3.set_xlabel('Re(c)')
    ax3.set_ylabel('Im(c)')
    plt.colorbar(im3, ax=ax3, label='Количество итераций')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    show_mandelbrot_25_iterations()
    # show_mandelbrot_50_iterations()
    # show_mandelbrot_100_iterations()
    # show_mandelbrot_200_iterations()
