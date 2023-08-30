from Armas.WeaponClass import Weapon
from Armas.ProjectileClass import Projectile
import pygame

class Pistol(Weapon):
    DAMAGE = 3
    COOLDOWN = 300  # 1000 milissegundos = 1 segundo

    def attack(self, position, target_position):
        # Cria um projétil se estiver fora do cooldown
        if self.can_attack(pygame.time.get_ticks()):
            self.last_attack_time = pygame.time.get_ticks()
            return [Projectile(position, target_position, damage=self.DAMAGE)]
        return []

    def can_attack(self, current_time):
        return current_time - self.last_attack_time > self.COOLDOWN