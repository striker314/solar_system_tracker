#!/usr/bin/env python3
import pygame
import math
from datetime import datetime, timezone

# Initialize Pygame
pygame.init()

# Start as a normal window instead of full monitor size.
WIDTH, HEIGHT = 1200, 900

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Real-Time Solar System Tracker")

# Visual Constants
SUN_SIZE = 35
PLANET_SCALE_FACTOR = 1.8
ORBIT_SPACING = 55

# Colors
BLACK = (5, 5, 12)
SUN_COLOR = (255, 215, 0)
WHITE = (250, 250, 250)
ORBIT_COLOR = (40, 40, 50)
TEXT_COLOR = (0, 255, 0)
MOON_COLOR = (200, 200, 200)

# Planet Data
PLANETS = [
    {"name": "Mercury", "dist": 1, "size": 6,  "color": (169, 169, 169), "L": 252.25, "P": 87.97},
    {"name": "Venus",   "dist": 2, "size": 10, "color": (230, 190, 130), "L": 181.98, "P": 224.7},
    {"name": "Earth",   "dist": 3, "size": 11, "color": (46, 139, 87),   "L": 100.46, "P": 365.25},
    {"name": "Mars",    "dist": 4, "size": 8,  "color": (255, 69, 0),    "L": 355.45, "P": 686.98},
    {"name": "Jupiter", "dist": 5, "size": 22, "color": (210, 180, 140), "L": 34.35,  "P": 4332.59},
    {"name": "Saturn",  "dist": 6, "size": 19, "color": (234, 214, 184), "L": 50.08,  "P": 10759.22},
    {"name": "Uranus",  "dist": 7, "size": 14, "color": (173, 216, 230), "L": 314.05, "P": 30685.4},
    {"name": "Neptune", "dist": 8, "size": 14, "color": (65, 105, 225),  "L": 304.35, "P": 60189.0},
    {"name": "Pluto",   "dist": 9, "size": 5,  "color": (150, 150, 150), "L": 238.93, "P": 90560.0},
]


def build_background(width, height):
    cx, cy = width // 2, height // 2
    surface = pygame.Surface((width, height))
    surface.fill(BLACK)

    pygame.draw.circle(surface, SUN_COLOR, (cx, cy), SUN_SIZE)

    for p in PLANETS:
        orbit_r = SUN_SIZE + (p["dist"] * ORBIT_SPACING)
        pygame.draw.circle(surface, ORBIT_COLOR, (cx, cy), orbit_r, 1)

    return surface, cx, cy


def get_current_angle(l_j2000, period_days):
    """Calculates real-time heliocentric longitude based on UTC."""
    j2000 = datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    delta_days = (now - j2000).total_seconds() / 86400.0
    angle_deg = (l_j2000 + (360.0 / period_days) * delta_days) % 360
    return math.radians(angle_deg)


bg_surface, cx, cy = build_background(WIDTH, HEIGHT)

# Fonts
font_label = pygame.font.SysFont("monospace", 18, bold=True)
font_ui = pygame.font.SysFont("monospace", 24)

# Main Loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            bg_surface, cx, cy = build_background(WIDTH, HEIGHT)

    screen.blit(bg_surface, (0, 0))

    # Draw Planets and Moon
    for p in PLANETS:
        orbit_r = SUN_SIZE + (p["dist"] * ORBIT_SPACING)
        angle = get_current_angle(p["L"], p["P"])

        px = cx + math.cos(angle) * orbit_r
        py = cy - math.sin(angle) * orbit_r

        scaled_size = int(p["size"] * PLANET_SCALE_FACTOR)
        pygame.draw.circle(screen, p["color"], (int(px), int(py)), scaled_size)

        if p["name"] == "Earth":
            moon_dist = 35
            moon_period = 27.32
            moon_angle = get_current_angle(218.3, moon_period)

            mx = px + math.cos(moon_angle) * moon_dist
            my = py - math.sin(moon_angle) * moon_dist

            pygame.draw.circle(screen, (30, 30, 40), (int(px), int(py)), moon_dist, 1)
            pygame.draw.circle(screen, MOON_COLOR, (int(mx), int(my)), 4)

            txt = font_label.render(p["name"], True, WHITE)
            screen.blit(txt, (px - scaled_size - 60, py + scaled_size + 5))

        else:
            txt = font_label.render(p["name"], True, WHITE)
            screen.blit(txt, (px + scaled_size + 5, py - scaled_size - 5))

    # Dynamic UI
    now_utc = datetime.now(timezone.utc)
    dt_str = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    timer_txt = font_ui.render(dt_str, True, TEXT_COLOR)
    screen.blit(timer_txt, (20, 20))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
