import socket
import struct
import time
from collections import deque

import numpy as np
import pygame

HOST = "127.0.0.1"
PORT = 5001
WINDOW_SIZE = (720, 720)


def recv_exact_into(sock: socket.socket, view: memoryview) -> None:
    """Read into a preallocated buffer or raise if the stream closes early."""
    total = 0
    while total < len(view):
        n = sock.recv_into(view[total:])
        if n == 0:
            raise ConnectionError("stream closed while reading")
        total += n


def read_frame(sock: socket.socket, buffer: bytearray | None) -> tuple[np.ndarray, bytearray]:
    header = bytearray(12)
    recv_exact_into(sock, memoryview(header))
    width, height, payload_size = struct.unpack("<III", header)

    if buffer is None or len(buffer) != payload_size:
        buffer = bytearray(payload_size)
    recv_exact_into(sock, memoryview(buffer))

    frame = np.frombuffer(buffer, dtype=np.uint8).reshape((height, width))
    return frame, buffer


def build_palette() -> list[tuple[int, int, int]]:
    # Brightened grayscale (built once) to add contrast.
    palette: list[tuple[int, int, int]] = []
    for i in range(255):
        v = min(255, int(i * 1.15) + 12)
        palette.append((v, v, v))
    palette.append((0, 0, 0))  # interior / max-iter tone
    return palette


def main() -> None:
    print(f"Connecting to {HOST}:{PORT} ...")
    with socket.create_connection((HOST, PORT)) as sock:
        print("Connected, streaming...")

        pygame.init()
        clock = pygame.time.Clock()
        window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Collatz fractal viewer")
        font = pygame.font.SysFont("monospace", 16)

        ticks = deque(maxlen=180)
        ticks.append(time.perf_counter())

        running = True
        buffer: bytearray | None = None
        palette = build_palette()
        pal_surface: pygame.Surface | None = None
        pal_pixels = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            try:
                frame, buffer = read_frame(sock, buffer)
            except (ConnectionError, OSError) as exc:
                print(f"Stream closed: {exc}")
                break

            if pal_surface is None or pal_surface.get_size() != (frame.shape[1], frame.shape[0]):
                pal_surface = pygame.Surface((frame.shape[1], frame.shape[0]), depth=8)
                pal_surface.set_palette(palette)
                pal_pixels = pygame.surfarray.pixels2d(pal_surface)

            pal_pixels[...] = frame  # direct write into 8-bit surface

            if pal_surface.get_size() != WINDOW_SIZE:
                blit_surface = pygame.transform.scale(pal_surface, WINDOW_SIZE)
            else:
                blit_surface = pal_surface

            window.blit(blit_surface, (0, 0))

            now = time.perf_counter()
            ticks.append(now)
            fps = (len(ticks) - 1) / (ticks[-1] - ticks[0]) if len(ticks) > 5 else 0.0
            fps_surface = font.render(f"{fps:4.1f} FPS", True, (255, 255, 255))
            window.blit(fps_surface, (10, 10))

            pygame.display.flip()
            clock.tick(165)

        pygame.quit()


if __name__ == "__main__":
    main()
