import numpy as np
import matplotlib.pyplot as plt # type: ignore

def julia(z, c, max_iter):
    diverge = np.zeros(z.shape, dtype=bool)
    iterations = np.zeros(z.shape, dtype=int)
    
    for i in range(max_iter):
        mask = ~diverge
        z[mask] = z[mask]**2 + c
        new_diverge = np.abs(z) > 2
        diverge_now = new_diverge & ~diverge
        iterations[diverge_now] = i
        diverge = diverge | new_diverge
        
    return iterations

def show_julia_c1():
    c = complex(-0.5251993, 0.5251993)
    max_iter = 200
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Основной вид
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    width, height = 400, 400
    
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    iterations = julia(Z, c, max_iter)
    
    im1 = ax1.imshow(iterations, extent=[x_min, x_max, y_min, y_max], 
                    cmap='hot', origin='lower')
    ax1.set_title(f'Множество Жюлиа\nc = {c.real:.4f} + {c.imag:.4f}i\n{max_iter} итераций - Основной вид')
    ax1.set_xlabel('Re(z)')
    ax1.set_ylabel('Im(z)')
    plt.colorbar(im1, ax=ax1, label='Количество итераций')
    
    # Приближение: Центральная спираль
    x_min_zoom, x_max_zoom = -0.5, 0.5
    y_min_zoom, y_max_zoom = -0.5, 0.5
    
    x_zoom = np.linspace(x_min_zoom, x_max_zoom, width)
    y_zoom = np.linspace(y_min_zoom, y_max_zoom, height)
    X_zoom, Y_zoom = np.meshgrid(x_zoom, y_zoom)
    Z_zoom = X_zoom + 1j * Y_zoom
    
    iterations_zoom = julia(Z_zoom, c, max_iter)
    
    im2 = ax2.imshow(iterations_zoom, extent=[x_min_zoom, x_max_zoom, y_min_zoom, y_max_zoom], 
                    cmap='hot', origin='lower')
    ax2.set_title(f'Множество Жюлиа\nПриближение - Центральная спираль')
    ax2.set_xlabel('Re(z)')
    ax2.set_ylabel('Im(z)')
    plt.colorbar(im2, ax=ax2, label='Количество итераций')
    
    plt.tight_layout()
    plt.show()

def show_julia_c2():
    c = complex(-0.7, 0.27015)
    max_iter = 200
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Основной вид
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    width, height = 400, 400
    
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    iterations = julia(Z, c, max_iter)
    
    im1 = ax1.imshow(iterations, extent=[x_min, x_max, y_min, y_max], 
                    cmap='hot', origin='lower')
    ax1.set_title(f'Множество Жюлиа\nc = {c.real:.4f} + {c.imag:.4f}i\n{max_iter} итераций - Основной вид')
    ax1.set_xlabel('Re(z)')
    ax1.set_ylabel('Im(z)')
    plt.colorbar(im1, ax=ax1, label='Количество итераций')
    
    # Приближение: Центральная область
    x_min_zoom, x_max_zoom = -0.3, 0.3
    y_min_zoom, y_max_zoom = -0.3, 0.3
    
    x_zoom = np.linspace(x_min_zoom, x_max_zoom, width)
    y_zoom = np.linspace(y_min_zoom, y_max_zoom, height)
    X_zoom, Y_zoom = np.meshgrid(x_zoom, y_zoom)
    Z_zoom = X_zoom + 1j * Y_zoom
    
    iterations_zoom = julia(Z_zoom, c, max_iter)
    
    im2 = ax2.imshow(iterations_zoom, extent=[x_min_zoom, x_max_zoom, y_min_zoom, y_max_zoom], 
                    cmap='hot', origin='lower')
    ax2.set_title(f'Множество Жюлиа\nПриближение - Центральная область')
    ax2.set_xlabel('Re(z)')
    ax2.set_ylabel('Im(z)')
    plt.colorbar(im2, ax=ax2, label='Количество итераций')
    
    plt.tight_layout()
    plt.show()

def show_julia_c3():
    c = complex(-0.8, 0.156)
    max_iter = 200
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Основной вид
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    width, height = 400, 400
    
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    iterations = julia(Z, c, max_iter)
    
    im1 = ax1.imshow(iterations, extent=[x_min, x_max, y_min, y_max], 
                    cmap='hot', origin='lower')
    ax1.set_title(f'Множество Жюлиа\nc = {c.real:.4f} + {c.imag:.4f}i\n{max_iter} итераций - Основной вид')
    ax1.set_xlabel('Re(z)')
    ax1.set_ylabel('Im(z)')
    plt.colorbar(im1, ax=ax1, label='Количество итераций')
    
    # Приближение: Фрактальные узоры
    x_min_zoom, x_max_zoom = -0.4, 0.4
    y_min_zoom, y_max_zoom = -0.4, 0.4
    
    x_zoom = np.linspace(x_min_zoom, x_max_zoom, width)
    y_zoom = np.linspace(y_min_zoom, y_max_zoom, height)
    X_zoom, Y_zoom = np.meshgrid(x_zoom, y_zoom)
    Z_zoom = X_zoom + 1j * Y_zoom
    
    iterations_zoom = julia(Z_zoom, c, max_iter)
    
    im2 = ax2.imshow(iterations_zoom, extent=[x_min_zoom, x_max_zoom, y_min_zoom, y_max_zoom], 
                    cmap='hot', origin='lower')
    ax2.set_title(f'Множество Жюлиа\nПриближение - Фрактальные узоры')
    ax2.set_xlabel('Re(z)')
    ax2.set_ylabel('Im(z)')
    plt.colorbar(im2, ax=ax2, label='Количество итераций')
    
    plt.tight_layout()
    plt.show()

def show_julia_c4():
    c = complex(0.285, 0.01)
    max_iter = 200
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Основной вид
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    width, height = 400, 400
    
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    iterations = julia(Z, c, max_iter)
    
    im1 = ax1.imshow(iterations, extent=[x_min, x_max, y_min, y_max], 
                    cmap='hot', origin='lower')
    ax1.set_title(f'Множество Жюлиа\nc = {c.real:.4f} + {c.imag:.4f}i\n{max_iter} итераций - Основной вид')
    ax1.set_xlabel('Re(z)')
    ax1.set_ylabel('Im(z)')
    plt.colorbar(im1, ax=ax1, label='Количество итераций')
    
    # Приближение: Дендритная структура
    x_min_zoom, x_max_zoom = -0.6, 0.6
    y_min_zoom, y_max_zoom = -0.6, 0.6
    
    x_zoom = np.linspace(x_min_zoom, x_max_zoom, width)
    y_zoom = np.linspace(y_min_zoom, y_max_zoom, height)
    X_zoom, Y_zoom = np.meshgrid(x_zoom, y_zoom)
    Z_zoom = X_zoom + 1j * Y_zoom
    
    iterations_zoom = julia(Z_zoom, c, max_iter)
    
    im2 = ax2.imshow(iterations_zoom, extent=[x_min_zoom, x_max_zoom, y_min_zoom, y_max_zoom], 
                    cmap='hot', origin='lower')
    ax2.set_title(f'Множество Жюлиа\nПриближение - Дендритная структура')
    ax2.set_xlabel('Re(z)')
    ax2.set_ylabel('Im(z)')
    plt.colorbar(im2, ax=ax2, label='Количество итераций')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":    
    show_julia_c1()  # c = -0.5251993 + 0.5251993i
    # show_julia_c2()  # c = -0.7 + 0.27015i
    # show_julia_c3()  # c = -0.8 + 0.156i
    # show_julia_c4()  # c = 0.285 + 0.01i
