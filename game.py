class GameEngine:
    def __init__(self):
        self.current_scene = "start"
        self.visited_scenes = set()
        self.choice_history = []
        self.player_name = ""
        self.health = 100
        self.karma = 0
        self.experience = 0
        self.luck = 50

        self.story = self.load_story()

    def load_story(self):
        story = {
            "start": {
                "text": "Вы стоите на развилке трёх дорог в древнем лесу. Перед вами три пути:\n"
                       "1. Тропа вглубь тёмного леса\n"
                       "2. Дорога к загадочным руинам\n"
                       "3. Тропинка к шумной реке",
                "choices": [
                    {"text": "Пойти в тёмный лес", "next": "dark_forest", "effects": {"luck": -5}},
                    {"text": "Исследовать руины", "next": "ruins", "effects": {"experience": 10}},
                    {"text": "Отправиться к реке", "next": "river", "effects": {"health": 10}}
                ]
            },
            
            "dark_forest": {
                "text": "Вы входите в густой тёмный лес. Воздух холодный, деревья скрипят.\n"
                       "Вдалеке виден странный свет. Что будете делать?",
                "choices": [
                    {"text": "Идти на свет", "next": "mysterious_light", "effects": {"luck": 5}},
                    {"text": "Искать другой путь", "next": "forest_path", "effects": {"health": -10}},
                    {"text": "Вернуться назад", "next": "start", "effects": {"karma": -5}}
                ]
            },
            
            "ruins": {
                "text": "Перед вами древние руины. Камни покрыты мхом, чувствуется магия.\n"
                       "В центре стоит алтарь с странными символами.",
                "choices": [
                    {"text": "Исследовать алтарь", "next": "altar", "effects": {"experience": 20}},
                    {"text": "Обыскать руины", "next": "search_ruins", "effects": {"luck": 10}},
                    {"text": "Уйти прочь", "next": "start", "effects": {}}
                ]
            },
            
            "river": {
                "text": "Вы у быстрой реки. Вода чистая и холодная. На другом берегу виднеется хижина.\n"
                       "Рядом старая лодка.",
                "choices": [
                    {"text": "Переплыть на лодке", "next": "boat_crossing", "effects": {"health": -20, "luck": 15}},
                    {"text": "Поискать брод", "next": "ford", "effects": {"health": -10, "experience": 15}},
                    {"text": "Отдохнуть у реки", "next": "rest_river", "effects": {"health": 30}}
                ]
            },
            
            "mysterious_light": {
                "text": "Вы подходите к свету. Это светлячки ведут к старому дереву с дуплом.\n"
                       "Внутри что-то блестит.",
                "choices": [
                    {"text": "Заглянуть в дупло", "next": "tree_hollow", "effects": {"luck": 20}},
                    {"text": "Игнорировать и идти дальше", "next": "deep_forest", "effects": {"karma": 10}},
                    {"text": "Вернуться", "next": "dark_forest", "effects": {}}
                ]
            },
            
            "forest_path": {
                "text": "Вы идёте по заросшей тропе. Внезапно путь преграждает огромный волк!",
                "choices": [
                    {"text": "Сражаться", "next": "wolf_fight", "effects": {"health": -40, "experience": 30}},
                    {"text": "Попытаться обойти", "next": "avoid_wolf", "effects": {"luck": -20, "karma": -10}},
                    {"text": "Бежать", "next": "run_away", "effects": {"health": -20}}
                ]
            },
            
            "altar": {
                "text": "На алтаре лежит древний артефакт - сияющий кристалл.\n"
                       "Рядом надпись: 'Только достойный может взять'.",
                "choices": [
                    {"text": "Взять кристалл", "next": "take_crystal", "effects": {"karma": -30, "experience": 50}},
                    {"text": "Оставить кристалл", "next": "leave_crystal", "effects": {"karma": 30}},
                    {"text": "Изучить надпись", "next": "study_inscription", "effects": {"experience": 25}}
                ]
            },
            
            "search_ruins": {
                "text": "Вы находите старый сундук под обломками. Он заперт.",
                "choices": [
                    {"text": "Попытаться взломать", "next": "break_chest", "effects": {"luck": -10, "experience": 20}},
                    {"text": "Поискать ключ", "next": "find_key", "effects": {"experience": 15}},
                    {"text": "Оставить сундук", "next": "ruins", "effects": {}}
                ]
            },
            
            "boat_crossing": {
                "text": "Лодка старая и течёт. Посередине реки она начинает тонуть!",
                "choices": [
                    {"text": "Грести быстрее", "next": "row_faster", "effects": {"health": -30, "luck": 25}},
                    {"text": "Вычерпывать воду", "next": "bail_water", "effects": {"health": -15, "experience": 20}},
                    {"text": "Прыгать в воду", "next": "jump_water", "effects": {"health": -40}}
                ]
            },
            
            "ford": {
                "text": "Вы нашли мелкий брод. Переходя реку, замечаете что-то в воде.",
                "choices": [
                    {"text": "Достать предмет", "next": "river_item", "effects": {"luck": 15}},
                    {"text": "Продолжить путь", "next": "other_side", "effects": {"experience": 10}},
                    {"text": "Осмотреться", "next": "look_around", "effects": {"health": 5}}
                ]
            },
            
            "tree_hollow": {
                "text": "В дупле вы находите магический амулет! Он излучает тепло.",
                "choices": [
                    {"text": "Надеть амулет", "next": "wear_amulet", "effects": {"health": 50, "luck": 30}},
                    {"text": "Взять с собой", "next": "take_amulet", "effects": {"luck": 20}},
                    {"text": "Оставить на месте", "next": "mysterious_light", "effects": {"karma": 20}}
                ]
            },
            
            "wolf_fight": {
                "text": "Вы сражаетесь с волком. Это тяжёлая битва!",
                "choices": [
                    {"text": "Ударить мечом", "next": "wolf_victory", "effects": {"health": -30, "experience": 40}},
                    {"text": "Использовать магию", "next": "use_magic", "effects": {"health": -10, "experience": 35}},
                    {"text": "Попытаться приручить", "next": "tame_wolf", "effects": {"karma": 40, "luck": 10}}
                ]
            },
            
            "take_crystal": {
                "text": "Вы взяли кристалл. Внезапно руины оживают! Статуи начинают двигаться.",
                "choices": [
                    {"text": "Сражаться со статуями", "next": "statue_fight", "effects": {"health": -50}},
                    {"text": "Бежать с кристаллом", "next": "escape_with_crystal", "effects": {"luck": 40}},
                    {"text": "Вернуть кристалл", "next": "altar", "effects": {"karma": 50}}
                ]
            },
            
            "break_chest": {
                "text": "Вам удаётся открыть сундук! Внутри вы находите...",
                "choices": [
                    {"text": "Старинные монеты", "next": "coins_found", "effects": {"experience": 30}},
                    {"text": "Магический свиток", "next": "scroll_found", "effects": {"experience": 40}},
                    {"text": "Карту сокровищ", "next": "treasure_map", "effects": {"luck": 50}}
                ]
            }
        }

        story.update({
            "deep_forest": {
                "text": "Вы заблудились в глубинах леса... Ваше приключение закончилось здесь.\n"
                       "Но может быть, в другой раз вам повезёт больше.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Заблудившийся"
            },
            
            "run_away": {
                "text": "Вы успешно сбежали от волка, но потерялись в лесу.\n"
                       "Через несколько дней вас нашли местные жители.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Спасшийся бегством"
            },
            
            "wolf_victory": {
                "text": "Вы победили волка! Теперь вы - настоящий герой этих земель.\n"
                       "Жители деревни празднуют вашу победу.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Победитель Волка"
            },
            
            "tame_wolf": {
                "text": "Волк признал в вас хозяина! Теперь у вас есть верный спутник.\n"
                       "Вместе вы продолжаете свои приключения.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Друзья животных"
            },
            
            "escape_with_crystal": {
                "text": "Вы сбежали с кристаллом! Его магия делает вас могущественным.\n"
                       "Вы становитесь легендой, о которой будут слагать песни.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Властелин Кристалла"
            },
            
            "coins_found": {
                "text": "Монеты оказываются древними и очень ценными!\n"
                       "Вы возвращаетесь домой богачом и живёте в достатке.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Богатый кладоискатель"
            },
            
            "wear_amulet": {
                "text": "Амулет дарует вам магические силы! Вы становитесь хранителем леса\n"
                       "и защитником всех живых существ в нём.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Хранитель Леса"
            },
            
            "rest_river": {
                "text": "Отдых у реки восстановил ваши силы, но время ушло.\n"
                       "Вы возвращаетесь домой, полный воспоминаний о приключении.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Умиротворённый путешественник"
            },
            
            "other_side": {
                "text": "Вы достигли другого берега и нашли путь домой.\n"
                       "Это путешествие многому вас научило.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Мудрый странник"
            }
        })

        return story
    
    def get_current_scene(self):
        return self.story.get(self.current_scene, None)
    
    def display_status(self):
        print(f"Здоровье: {self.health}\nКарма: {self.karma}\nОпыт: {self.experience}\nУдача: {self.luck}")

    def is_ending(self):
        scene = self.get_current_scene()
        if not scene:
            return scene.get("is_ending", False)

    def get_ending(self):
        scene = self.get_current_scene()
        if (scene and scene.get("is_ending", False)):
            return scene.get("ending_name", "Неизвестная концовка")
        return None

    def make_choice(self, choice_index):
        scene = self.get_current_scene()
        if ((not scene) or choice_index < 0 or choice_index >= len(scene["choices"])):
            return False

        choice = scene["choices"][choice_index]
        self.choice_history.append({
            "scene": self.current_scene,
            "choice": choice["text"],
            "next": choice["next"]
        })

        self.apply_effects(choice.get("effects", {}))
        self.visited_scenes.add(self.current_scene)
        self.current_scene = choice["next"]
        return True

    def apply_effects(self, effects):
        for param, val in effects.items():
            if param == "health":
                self.health = max(0, min(150, self.health + val))
            elif param == "karma":
                self.karma = max(-100, min(100, self.karma + val))
            elif param == "experience":
                self.experience = max(0, self.experience + val)
            elif param == "luck":
                self.luck = max(0, min(100, self.luck + val))

def main():
    print("Добро пожаловать в игру!\n")

    engine = GameEngine()
    engine.player_name = input("Введите ваше имя: \n").strip() or "Игрок"

    print(f"\nДобро пожаловать, {engine.player_name}!\n")
    print("Ваше приключение начинается...\n")

    while 1:
        scene = engine.get_current_scene()
        print(scene["text"])
        engine.display_status()

        if engine.is_ending():
            ending = engine.get_ending()
            print(f"Вы достигли концовки: {ending} !\n")

if __name__ == "__main__":
    main()