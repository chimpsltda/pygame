class Weapon:
    def __init__(self):
        self.last_attack_time = 0

    def attack(self, position, target_position):
        raise NotImplementedError()

    def can_attack(self, current_time):
        raise NotImplementedError()