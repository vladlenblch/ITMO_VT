import numpy as np
import matplotlib.pyplot as plt # type: ignore
import math

def draw_pythagoras_tree(ax, x, y, length, angle, depth, max_depth, angle_change=45):
    if depth > max_depth or length < 1:
        return
    
    x_end = x + length * math.cos(math.radians(angle))
    y_end = y + length * math.sin(math.radians(angle))
    
    color = plt.cm.hot(depth / max_depth)
    ax.plot([x, x_end], [y, y_end], color=color, linewidth=max_depth - depth + 1)
    
    new_length = length * 0.7
    
    draw_pythagoras_tree(ax, x_end, y_end, new_length, angle - angle_change, depth + 1, max_depth, angle_change)
    draw_pythagoras_tree(ax, x_end, y_end, new_length, angle + angle_change, depth + 1, max_depth, angle_change)

def show_pythagoras_tree_5_iterations():
    max_depth = 5
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    fig.patch.set_facecolor('#f0f0f0')
    ax.set_facecolor('#6d6d6d')
    
    ax.set_aspect('equal')
    ax.set_xlim(-150, 150)
    ax.set_ylim(-10, 250)
    
    draw_pythagoras_tree(ax, 0, 0, 80, 90, 0, max_depth, 45)
    ax.set_title(f'Дерево Пифагора\n{max_depth} итераций - Основной вид')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def show_pythagoras_tree_7_iterations():
    max_depth = 7
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    fig.patch.set_facecolor('#f0f0f0')
    ax.set_facecolor('#6d6d6d')
    
    ax.set_aspect('equal')
    ax.set_xlim(-200, 200)
    ax.set_ylim(-10, 300)
    
    draw_pythagoras_tree(ax, 0, 0, 100, 90, 0, max_depth, 45)
    ax.set_title(f'Дерево Пифагора\n{max_depth} итераций - Основной вид')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def show_pythagoras_tree_9_iterations():
    max_depth = 9
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    fig.patch.set_facecolor('#f0f0f0')
    ax.set_facecolor('#6d6d6d')
    
    ax.set_aspect('equal')
    ax.set_xlim(-300, 300)
    ax.set_ylim(-10, 400)
    
    draw_pythagoras_tree(ax, 0, 0, 120, 90, 0, max_depth, 45)
    ax.set_title(f'Дерево Пифагора\n{max_depth} итераций - Основной вид')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def show_pythagoras_tree_11_iterations():
    max_depth = 11
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    fig.patch.set_facecolor('#f8f8f8')
    ax.set_facecolor('#6d6d6d')
    
    ax.set_aspect('equal')
    ax.set_xlim(-400, 400)
    ax.set_ylim(-10, 500)
    
    draw_pythagoras_tree(ax, 0, 0, 140, 90, 0, max_depth, 45)
    ax.set_title(f'Дерево Пифагора\n{max_depth} итераций - Основной вид')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    show_pythagoras_tree_5_iterations()
    # show_pythagoras_tree_7_iterations()
    # show_pythagoras_tree_9_iterations()
    # show_pythagoras_tree_11_iterations()
