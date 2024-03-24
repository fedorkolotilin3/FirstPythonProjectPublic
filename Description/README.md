# Тренажер скоростной печати 

### Консольное приложение с возможностью дополнения графическим интерфейсом

#### Общий функционал
Тренировка скоростной печати, за счет выведения строки, которую надо напечатать и анализа ввода


### Анализ ввода:
Анализироваться будет количество ошибок и скорость печати,
в основном режиме ошибкочный ввод печататься не будет, 
ввод неправильного символа будет блокироваться, а счетчик ошибок будет увеличиваться

### Статистика 
Прогресс, результаты и прочая статистика будут видны после окончания [Printing Activity](#printing-activity), 
а также глобально сохраняться
в специальных файлах с данными, так что после нового старта приложения можно будет видеть рещультаты предыдущих 
попыток и глобальный прогресс


### Библиотеки и Генерация строки - цели (ту что надо напечатать) 
Текст **_строки - цели_** будет выбираться из выбранной пользователем библиотеки (условно папка с .txt файлами), которые пользователь
сможет добавлять в 
[Add Library Activity](#add-library-activity)

Изначально будет 6 встроенных библиотек: по 3 для руссского и английского языков
сложноостью **_easy_**, **_medium_** и **_hard_** соответсвенно


# User Expirience
(описание пользовательского опыта в приложении делится на блоки - активности, которыми он будет "заниматься"
во время использования)

## Активности:


### Start Activity (=Main Activity)
Первая активность, начинается при запуске приложения

Включает в себе меню выбора прочих активностей и минимальную информацию для старта в использовании приложения
Активности к выбору

1) [Printing Activity](#printing-activity) (если есть последняя ранее выбранная библиотека) 
1) [Choose Library](#choose-library-activity)
2) [Help](#helpactivity)
3) [Score Board](#score-board-activity))

### Choose Library Activity
Перед началом [Printing Activity](#printing-activity) надо выбрать библиотеку, откуда будет выбрана **_строка - цель_** 
Также можно добавить кастомную библиотеку, перейдя в [Add Library](#add-library-activity)

### Printing Activity
Ключевая Активность

Запускается от выбранной библиотеке, создавая строку из нее

Содержит минимум два объекта: **_строка - цель_** и **_введенная строка_**
Первая отвечает за то, что пользователь должен перепечатать, вторая показывает пользователю то, что он уже напечатал

Также возжможно дополнение онлайн статистикой текущей попытки, а также рекордов по данной библиотеке

Данную активность можно поставить на [паузу](#pause-activity), 

По окончанию активности 
#### Pause Activity
Здесь будет скрыты **_строка - цель_** и **_введенная строка_** для честности статистики

Зато появятся / сохранятся счетчики статистики и
появится меню для выхода в [главное меню](#start-activity-main-activity) или продолжения текущей попытки
Возможно дополнения функционала в последствии

### Add Library Activity
Содержит меню менеджмента имеющихся и добавления новых библиотек, также содержит правила того, как 
должна быть устроена корректная папка - библиотека

### Score Board Activity
Здесь пользователь может посмотреть свои результаты предыдущих попыток: 

1) библиотека
2) скорость
3) число ошибок 
4) число символов которые требовалось напечатать 

а также 2 - ю и 3 - ю метрики относительно числа символов 
условно 


    value / chars_count * chars_etalon_count  
Также может быть добавлена глобальная статистика, в которой описанная выше 
информация по попыткам будет агрегироваться в более компактную статистику

### HelpActivity
Осуществляет вывод правил приложения, общей информации а также деталей [Printing Activity](#printing-activity)


# Архитектура проекта (структура классов)

## Вспомогательные классы


* ### Attempt
  - attributes:  
    -   Library using_libray
    -   AttemptScore score
  - methods:
    
* ### AttemptScore
  - attributes:   
  - - int errors_count
  - - int chars_count
  - - int time
  - methods:   

* ### Library
  - attributes:
  - methods:
  - - GetText()
  - - ReadLibrary(string dir_path)     #локальные файлы приложения с папкой библиотеки, пересобранной  под мои нужды
  - - CreateLibrary(string dir_path)   #глобальные файлы пользователя, в спец. формате под создание библиотеки


* ### Activity (abstract)
  - attributes:  
  - - string activity_name
  - - ContentList content_list
  - methods:   
  - - PrintHelp()
  - - OnCreate() # вызывается при создании активности для иницализации переменных и т.д.
  - - Escape()   


* ### Content 
  - attributes: 
  - - Content parent
  - - string item_text
  - methods:      
  - - Action() #action that can do user by this item
  - - PrintContent()
                                          
* ### TextContent 
     - - - - #can be edited and reprinted after (example: **_введенная строка_**   )                                                  
  - 
  - attributes:                                                                                                                                
  - methods:
  - - Print()
  - - RePrint()
        

* ### ContentList : Content
  - attributes:
  - - is_active
  - - list[Content] items
  - - int current_item_number
  - methods:
  - - Activate() `enter`             
  - - Disable()  `esc`
  - - GoNext()
  - - GoPrevious()
  - - GetItem()
  - - AddItem(Content int pos = 0)




## User Experience классы   (сявязанные с взаимодействием с пользователем)

* ### StartActivity                                                        
  - attributes:
  - - Library previous_library
  - - ChooseLibraryActivity choose_library_activity
  - - HelpActivity help_activity
  - - PrintingActivity printing_activity
  - - ScoreBoardActivity score_board_activity
  - methods:             
                                                                     
* ### ChooseLibraryActivity                                                  
  - attributes:
  - - list[Library] existing_libs
  - methods:            
  - - SetLibrary()
  - - StartPrintingActivity()

* ### PrintingActivity                                          
  - attributes:
  - - Attempt attempt
  - - PauseActivity pause_activity
  - - TextContent text_to_print
  - - TextContent printed_text
  - methods
  - - ReadKeyboard()   # проверка введенных сиволов и соотв. логика
  - - SaveAttempt() 
                                                                     
* ### PauseActivity       
  - attributes:  
  - - StartActivity start_activity
  - methods:      

* ### AddLibraryActivity                             
  - attributes:                                 
  - - string path_to_library
  - methods:                             
  - - PrintInfo()   # выводит правила папки которая прочтется как библиотека
  - - ReadPath()    # считывает путь до добавляемой библиотеки
  - - AddLibrary()  # создает библиотеку по указанному пути  
                                                
* ### ScoreBoardActivity                     
  - attributes:
  - - list[Attempt] previous_attempts
  - methods:        
  - - PrintBoard()  # выводит доску результатов

* ### HelpActivity                        
  - attributes:  
  - methods:
  - - PrintInfo()   #выводит текст подсказки
                                                                                                