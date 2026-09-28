import random
import sys
import time
from typing import Dict, Tuple


STOP_WORD = 'СТОП'


def load_words(filename: str = 'words.txt') -> Dict[str, str]:
    """Загружает словарь пар «слово — перевод» из файла."""
    dictionary = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) == 2:
                    word, translation = parts[0], parts[1]
                    if word and translation:
                        dictionary[word] = translation
        return dictionary
    except FileNotFoundError:
        print(f'Файл {filename} не найден.')
        sys.exit(1)


def print_statistics(score: int, total_time: float) -> None:
    """Выводит итоговую статистику по завершении игры"""
    if score > 0:
        average_time = total_time / score
        average_time_str = f'{average_time:.2f} сек.'
    else:
        average_time_str = '—'
    print(f'Ваш итоговый счет: {score}')
    time_line = (
        f'Время игры: {total_time:.2f} секунд '
        f'(среднее время: {average_time_str})'
    )
    print(time_line)


def ask_and_check(word: str, correct: str) -> Tuple[bool, bool, float]:
    """
    Спрашивает у пользователя перевод заданного слова,
    возвращает необходимость выхода, правильность ответа и время,
    затраченное на ответ.
    """
    print(f'Ваше слово: {word}')
    start_time = time.time()
    user_translate = input('Ваш перевод: ').strip().lower()
    end_time = time.time()
    if user_translate == STOP_WORD.lower():
        return True, False, 0.0
    answer_time = end_time - start_time
    is_answer_correct = user_translate == correct.strip().lower()
    return False, is_answer_correct, answer_time


def start_game(words: Dict[str, str]) -> None:
    """
    Запускает игровой режим, в котором пользователь переводит случайные слова.
    """
    total_time = 0.0
    score = 0
    if not words:
        print('Словарь пуст')
        return
    print('Чтобы закончить, введите СТОП')
    words_keys = list(words.keys())
    while True:
        random_word = random.choice(words_keys)
        correct_translate = words[random_word]
        exit_flag, is_correct, answer_time = ask_and_check(
            random_word, correct_translate
        )
        if exit_flag:
            break
        total_time += answer_time
        if is_correct:
            score += 1
            print(f'Верно! Время на ответ: {answer_time:.2f} секунд')
        else:
            fail_message = (
                f'Неправильно, правильный ответ: {correct_translate} '
                f'(Время на ответ: {answer_time:.2f} секунд)'
            )
            print(fail_message)
    print_statistics(score, total_time)


def train_until_mistake(words: Dict[str, str]) -> None:
    """Запускает игровой режим «до первой ошибки»."""
    if not words:
        print('Словарь пуст')
        return
    print('Режим: игра до первой ошибки! Чтобы выйти вручную, введите СТОП')
    total_time = 0.0
    score = 0
    words_keys = list(words.keys())
    while True:
        random_word = random.choice(words_keys)
        correct_translate = words[random_word]
        exit_flag, is_correct, answer_time = ask_and_check(
            random_word, correct_translate
        )
        if exit_flag:
            print('Выход из режима по запросу пользователя.')
            break
        total_time += answer_time
        if is_correct:
            score += 1
            success_message = (
                f'Верно! Всего очков: {score} '
                f'(ответ за {answer_time:.2f} секунд)'
            )
            print(success_message)
        else:
            print(f'Ошибка! Неверно. Правильный ответ: {correct_translate}')
            break
    print_statistics(score, total_time)


def show_all_words(words: Dict[str, str]) -> None:
    """Вывести на экран все пары «слово — перевод» из словаря."""
    pairs = (f'{word} - {translate}' for word, translate in words.items())
    result = '; '.join(pairs)
    print(result)


def add_words(words: Dict[str, str]) -> None:
    """Добавляет новые пары «слово — перевод» в словарь."""
    print('Чтобы закончить, введите СТОП')
    while True:
        word = input('Введите слово: ').strip()
        if word.lower() == STOP_WORD.lower():
            break
        translate = input('Введите перевод: ').strip()
        if translate.lower() == STOP_WORD.lower():
            break
        words[word] = translate


def save_words(
    words: Dict[str, str],
    filename: str = 'words.txt'
) -> None:
    """Сохраняет все пары «слово, перевод» из словаря в текстовый файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        for word, translate in words.items():
            f.write(f'{word},{translate}\n')
    print(f'Было сохранено {len(words)} слов в файл {filename}.')


def main() -> None:
    """Запускает основной цикл работы программы-тренажёра для изучения слов."""
    dictionary = load_words()
    print(f'Было загружено {len(dictionary)} слов из файла words.txt')
    menu_dict = {
        '1': start_game,
        '2': add_words,
        '3': train_until_mistake,
        '4': show_all_words,
    }
    while True:
        menu = (
            'Меню:\n'
            '    1. Начать игру\n'
            '    2. Добавить слова\n'
            '    3. Тренировка до первой ошибки\n'
            '    4. Вывод всех слов\n'
            '    5. Выход'
        )
        print(menu)
        menu_choice = input('Пункт меню: ').strip()
        if menu_choice in menu_dict:
            menu_dict[menu_choice](dictionary)
        elif menu_choice == '5':
            save_words(dictionary)
            sys.exit()
        else:
            print('Неизвестный пункт меню')


if __name__ == '__main__':
    main()
