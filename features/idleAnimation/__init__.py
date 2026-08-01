from config import IDLE_ANIMATION_TYPE as CONFIG_ANIMATION_TYPE
from constants import IDLE_ANIMATION_TYPE
from features.idleAnimation.animations.snake_along_the_border import SnakeAlongTheBorder
from features.idleAnimation.animations.barber_pole import BarberPole
from features.idleAnimation.idle_animation import IdleAnimation

if CONFIG_ANIMATION_TYPE == IDLE_ANIMATION_TYPE.SNAKE_ALONG_THE_BORDER:
    current_animation = SnakeAlongTheBorder()
elif CONFIG_ANIMATION_TYPE == IDLE_ANIMATION_TYPE.BARBER_POLE:
    current_animation = BarberPole()
else:
    current_animation = IdleAnimation()

def tick():
    return current_animation.tick()

def notify_activity():
    current_animation.notify_activity()
