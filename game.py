"""
Текстовая игра с нелинейным сюжетом.
Игрок делает выборы, которые влияют на параметры персонажа и приводят к разным концовкам.
Реализована как граф сценариев с алгоритмами поиска путей (BFS/DFS).
"""

class GameEngine:
    """Основной движок игры, управляющий сюжетом, состоянием игрока и переходами"""
    
    def __init__(self):
        """Инициализация игры с начальными параметрами"""
        self.current_scene = "start"  # Текущая сцена
        self.visited_scenes = set()   # Посещенные сцены
        self.choice_history = []      # История выборов игрока
        self.player_name = ""         # Имя игрока
        self.health = 100             # Здоровье (от 0 до 150)
        self.karma = 0                # Карма (от -100 до 100)
        self.experience = 0           # Опыт (от 0)
        self.luck = 50                # Удача (от 0 до 100)
        
        self.story = self.load_story()  # Загрузка структуры сюжета

    def load_story(self):
        """
        Каждая сцена содержит:
        - text: описание сцены
        - choices: варианты выбора с эффектами
        - is_ending: флаг концовки
        - ending_name: название концовки (если is_ending=True)
        """
        # Базовые сцены
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
            },
            
            "row_faster": {
                "text": "Вы гребли изо всех сил и достигли противоположного берега! Лодка тонет,\n"
                       "но вы успеваете выскочить на берег. Перед вами хижина.",
                "choices": [
                    {"text": "Войти в хижину", "next": "hut", "effects": {"experience": 20}},
                    {"text": "Обойти хижину", "next": "around_hut", "effects": {"luck": 10}},
                    {"text": "Отдохнуть на берегу", "next": "shore_rest", "effects": {"health": 20}}
                ]
            },
            
            "bail_water": {
                "text": "Вы вычерпываете воду и успеваете добраться до берега.\n"
                       "Вы мокрые, но живы. Перед вами тропинка, ведущая в лес.",
                "choices": [
                    {"text": "Идти по тропинке", "next": "forest_path", "effects": {"health": -10}},
                    {"text": "Обследовать берег", "next": "shore_explore", "effects": {"experience": 15}},
                    {"text": "Вернуться к реке", "next": "river", "effects": {"health": 5}}
                ]
            },
            
            "jump_water": {
                "text": "Вы прыгнули в воду и поплыли к берегу. Течение сильное,\n"
                       "но вы справляетесь и выбираетесь на сушу.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Отважный пловец"
            },
            
            "river_item": {
                "text": "Вы достаёте из воды старый меч в ножнах.\n"
                       "Он выглядит древним, но хорошо сохранившимся.",
                "choices": [
                    {"text": "Взять меч", "next": "take_sword", "effects": {"experience": 30, "luck": 10}},
                    {"text": "Оставить меч", "next": "ford", "effects": {"karma": 15}},
                    {"text": "Осмотреть тщательнее", "next": "examine_sword", "effects": {"experience": 20}}
                ]
            },
            
            "look_around": {
                "text": "Вы осматриваетесь и замечаете на берегу следы животных.\n"
                       "Похоже, здесь часто приходят на водопой.",
                "choices": [
                    {"text": "Пойти по следам", "next": "animal_tracks", "effects": {"experience": 10}},
                    {"text": "Вернуться к броду", "next": "ford", "effects": {}},
                    {"text": "Продолжить путь", "next": "other_side", "effects": {"health": 10}}
                ]
            },
            
            "leave_crystal": {
                "text": "Вы решаете не брать кристалл. Внезапно появляется дух древнего хранителя,\n"
                       "который благодарит вас за мудрость.",
                "choices": [
                    {"text": "Поговорить с духом", "next": "talk_spirit", "effects": {"karma": 40, "experience": 30}},
                    {"text": "Попросить награду", "next": "ask_reward", "effects": {"karma": -20, "luck": 30}},
                    {"text": "Поклониться и уйти", "next": "ruins", "effects": {"karma": 10}}
                ]
            },
            
            "study_inscription": {
                "text": "Вы изучаете надпись и понимаете, что это заклинание защиты.\n"
                       "Теперь вы можете использовать его в битве.",
                "choices": [
                    {"text": "Запомнить заклинание", "next": "remember_spell", "effects": {"experience": 40}},
                    {"text": "Записать в дневник", "next": "write_spell", "effects": {"experience": 35}},
                    {"text": "Вернуться к алтарю", "next": "altar", "effects": {"experience": 10}}
                ]
            },
            
            "find_key": {
                "text": "Вы находите ключ под камнем! Он подходит к сундуку.",
                "choices": [
                    {"text": "Открыть сундук", "next": "open_chest", "effects": {"luck": 20}},
                    {"text": "Оставить сундук закрытым", "next": "search_ruins", "effects": {"karma": 25}},
                    {"text": "Взять ключ с собой", "next": "take_key", "effects": {"luck": 15}}
                ]
            },
            
            "use_magic": {
                "text": "Вы используете магию, и волк отступает! Он смотрит на вас с уважением.",
                "choices": [
                    {"text": "Добить волка", "next": "finish_wolf", "effects": {"experience": 50, "karma": -20}},
                    {"text": "Отпустить волка", "next": "release_wolf", "effects": {"karma": 50}},
                    {"text": "Попытаться подружиться", "next": "befriend_wolf", "effects": {"luck": 30, "karma": 40}}
                ]
            },
            
            "statue_fight": {
                "text": "Вы сражаетесь с ожившими статуями. Это очень тяжелая битва!",
                "choices": [],
                "is_ending": True,
                "ending_name": "Герой Руин"
            }
        }

        # Добавление финальных сцен
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
            },
            
            "avoid_wolf": {
                "text": "Вы попытались обойти волка, но он вас заметил и напал сзади.\n"
                       "К счастью, охотники услышали шум и спасли вас.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Спасённый охотниками"
            },
            
            "scroll_found": {
                "text": "Вы нашли древний магический свиток! Он содержит могущественные заклинания.\n"
                       "Теперь вы можете стать великим магом.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Великий Маг"
            },
            
            "treasure_map": {
                "text": "Вы нашли карту сокровищ! Она указывает на скрытые богатства.\n"
                       "Ваши поиски только начинаются...",
                "choices": [],
                "is_ending": True,
                "ending_name": "Искатель Сокровищ"
            },
            
            "take_amulet": {
                "text": "Вы взяли амулет с собой. Его магия защищает вас в путешествиях.\n"
                       "Вы становитесь известным искателем приключений.",
                "choices": [],
                "is_ending": True,
                "ending_name": "Странствующий Искатель"
            }
        })
        return story
    
    def get_current_scene(self):
        """
        Получает текущую сцену из словаря сюжета
        """
        return self.story.get(self.current_scene, None)
    
    def display_status(self):
        """Выводит текущие параметры игрока"""
        print(f"Здоровье: {self.health}\nКарма: {self.karma}\nОпыт: {self.experience}\nУдача: {self.luck}")

    def is_ending(self):
        """
        Проверяет, является ли текущая сцена концовкой.
        """
        scene = self.get_current_scene()
        return scene.get("is_ending", False) if scene else False

    def get_ending(self):
        """
        Получает название текущей концовки.
        """
        scene = self.get_current_scene()
        if (scene and scene.get("is_ending", False)):
            return scene.get("ending_name", "Неизвестная концовка")
        return None

    def make_choice(self, choice_index):
        """
        Обрабатывает выбор игрока, обновляет состояние и переходит к следующей сцене.
        """
        scene = self.get_current_scene()
        if ((not scene) or choice_index < 0 or choice_index >= len(scene["choices"])):
            return False

        choice = scene["choices"][choice_index]
        # Сохраняем выбор в историю
        self.choice_history.append({
            "scene": self.current_scene,
            "choice": choice["text"],
            "next": choice["next"]
        })

        # Применяем эффекты выбора
        self.apply_effects(choice.get("effects", {}))
        # Отмечаем сцену как посещенную
        self.visited_scenes.add(self.current_scene)
        # Переходим к следующей сцене
        self.current_scene = choice["next"]
        return True

    def apply_effects(self, effects):
        """
        Применяет эффекты выбора к параметрам игрока с ограничениями диапазонов.
        """
        for param, val in effects.items():
            if param == "health":
                self.health = max(0, min(150, self.health + val))
            elif param == "karma":
                self.karma = max(-100, min(100, self.karma + val))
            elif param == "experience":
                self.experience = max(0, self.experience + val)
            elif param == "luck":
                self.luck = max(0, min(100, self.luck + val))

    def calculate_score(self):
        """
        Вычисляет итоговый счет игрока на основе параметров и статистики.
        """
        base_score = self.experience * 2 + self.health + self.karma + self.luck
        # Бонусы за достижения
        if len(self.visited_scenes) >= 5:
            base_score += 50  # Бонус за исследование
        if self.health >= 100:
            base_score += 30  # Бонус за сохранение здоровья
        if self.karma >= 50:
            base_score += 40  # Бонус за хорошую карму
        return base_score

    def build_graph(self):
        """
        Строит граф переходов между сценами для алгоритмов поиска.
        """
        graph = {}
        for scene_id, scene_data in self.story.items():
            choices = scene_data.get("choices", [])
            graph[scene_id] = [choice["next"] for choice in choices]
        return graph

    def find_paths_to_ending(self, target_ending):
        """
        Находит все возможные пути к указанной концовке с использованием BFS.
        """
        graph = self.build_graph()
        paths = []
        # Очередь для BFS: (текущий_путь, текущая_вершина)
        queue = [(["start"], "start")]

        while queue:
            path, current = queue.pop(0)
            # Если достигли искомой концовки
            if (current in self.story and 
                self.story[current].get("is_ending", False) and
                self.story[current].get("ending_name") == target_ending):
                paths.append(path + [current])
                continue

            # Добавляем соседей в очередь
            for neighbor in graph.get(current, []):
                if neighbor not in path:  # Избегаем циклов
                    queue.append((path + [neighbor], neighbor))
        return paths

    def dfs(self, current, visited, endings_counter):
        """
        Рекурсивный DFS для подсчета всех возможных концовок.
        """
        if current in visited:
            return
            
        visited.add(current)

        # Если текущая сцена - концовка, увеличиваем счетчик
        if (current in self.story and 
            self.story[current].get("is_ending", False)):
            ending_name = self.story[current].get("ending_name", "Неизвестно")
            endings_counter[ending_name] = endings_counter.get(ending_name, 0) + 1
            return
        
        # Рекурсивно обходим все варианты выбора
        scene = self.story.get(current, {})
        for choice in scene.get("choices", []):
            next_scene = choice["next"]
            if next_scene not in visited:
                self.dfs(next_scene, visited.copy(), endings_counter)
    
    def count_all_endings(self):
        """
        Подсчитывает все возможные концовки в игре с помощью DFS
        """
        endings_counter = {}
        self.dfs("start", set(), endings_counter)
        return endings_counter
    
    def save_results(self):
        """
        Сохраняет результаты игры в текстовый файл game_results.txt.
        Записывает имя игрока, выборы, параметры и концовку.
        """
        filename = "game_results.txt"
        ending = self.get_ending()
        final_score = self.calculate_score()
        
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"\n")
                f.write(f"Игра завершена\n")
                f.write(f"Имя игрока: {self.player_name}\n")
                f.write(f"Концовка: {ending}\n")
                f.write(f"Финальный счет: {final_score}\n")
                f.write(f"Параметры: Здоровье={self.health}, Карма={self.karma}, "
                       f"Опыт={self.experience}, Удача={self.luck}\n")
                f.write(f"Посещено сцен: {len(self.visited_scenes)}\n")
                f.write("История выборов:\n")
                
                for i, choice in enumerate(self.choice_history, 1):
                    f.write(f"  {i}. В сцене '{choice['scene']}' выбрано: {choice['choice']}\n")
                
                f.write("\n\n")
            
            print(f"\nРезультаты сохранены в файл '{filename}'")
            
        except Exception as e:
            print(f"\nОшибка при сохранении результатов: {e}")

def main():
    """
    Основная функция игры. Управляет игровым циклом и взаимодействием с пользователем.
    """
    print("Добро пожаловать в игру!\n")
    
    engine = GameEngine()
    engine.player_name = input("Введите ваше имя: ").strip() or "Игрок"

    print(f"\nДобро пожаловать, {engine.player_name}!")
    print("Ваше приключение начинается...\n")

    # Основной игровой цикл
    while True:
        scene = engine.get_current_scene()
        if not scene:
            print("Ошибка: сцена не найдена!")
            break

        print("\n")
        print(scene["text"])
        print("\nТекущие параметры:")
        engine.display_status()

        # Проверка на достижение концовки
        if engine.is_ending():
            ending = engine.get_ending()
            print(f"\nВы достигли концовки: {ending} ")
            final_score = engine.calculate_score()
            print(f"Ваш итоговый счет: {final_score}")

            # Вывод статистики
            print("\nСтатистика игры:")
            print(f"Посещено сцен: {len(engine.visited_scenes)}")
            print(f"Сделано выборов: {len(engine.choice_history)}")
            print(f"Финальные параметры:")
            print(f"  Здоровье: {engine.health}")
            print(f"  Карма: {engine.karma}")
            print(f"  Опыт: {engine.experience}")
            print(f"  Удача: {engine.luck}")
            
            # Сохранение результатов
            engine.save_results()
            
            # Показ всех возможных концовок
            print("\nВсе возможные концовки в игре:")
            all_endings = engine.count_all_endings()
            for ending_name, count in all_endings.items():
                print(f"   {ending_name}: {count} способов достижения")
            
            print("\nСпасибо за игру!")
            break
        
        # Отображение вариантов выбора
        print("\nВаши варианты:")
        for i, choice in enumerate(scene["choices"], 1):
            effects_text = ""
            effects = choice.get("effects", {})
            if effects:
                effects_parts = []
                for param, value in effects.items():
                    # Преобразование названий параметров на русский
                    if param == "health":
                        param_name = "Здоровье"
                    elif param == "karma":
                        param_name = "Карма"
                    elif param == "experience":
                        param_name = "Опыт"
                    elif param == "luck":
                        param_name = "Удача"
                    else:
                        param_name = param
                    
                    # Форматирование значений (+/-)
                    if value > 0:
                        effects_parts.append(f"+{value} {param_name}")
                    elif value < 0:
                        effects_parts.append(f"{value} {param_name}")
                if effects_parts:
                    effects_text = f" ({', '.join(effects_parts)})"
            
            print(f"{i}. {choice['text']}{effects_text}")

        # Обработка ввода пользователя
        while True:
            try:
                choice = input("\nВаш выбор (введите номер): ").strip()
                if not choice:
                    print("Пожалуйста, сделайте выбор!")
                    continue
                    
                choice_index = int(choice) - 1
                
                if not engine.make_choice(choice_index):
                    print("Неверный выбор! Попробуйте снова.")
                else:
                    break
                    
            except ValueError:
                print("Пожалуйста, введите число!")
            except KeyboardInterrupt:
                print("\n\nИгра прервана.")
                return

if __name__ == "__main__":
    main()