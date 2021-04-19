# Ідентифікація сторінки по малюнку
Для отримання точок розпізнавання и вирахування опису використовується алгоритм “BRISK” (“Binary Robust Invariant Scalable Keypoints”).

__Головні елементи проекту__:

1. Всі вимоги для запуску зібрані у файлі [requirements.txt](/requirements.txt).
	Структура папок проекту розпізнавання (окрім модулів):
	- images
		- covers (назви книг скорочено латиниця без пробілів)
			- файл з назвою книги з розширенням "pickle"
			- файл current_book.txt,куди записується інфо про поточну книгу
		- папки з назвами книг (важливо зберігати унікальне ім'я в латиниці по назвам маркерів в папці covers)
			- файл з назвою книги з розширенням "pickle"
   
	**після створення 'pickle' зберігання файлів маркерів-картинок не обов'язкове, в розпізнаванні використовується тільки файл 'pickle'
	
2. Запуск отримання маркерів з pdf-файлів відбувається шляхом запуску з папки проекту:

```bash
python cut_marker.py --folder_name <folder includes pdf pages> --marker_name <short name of book>
```    
Приклад:    
    
```bash    
\Books_images> python cut_marker.py --folder_name images\20_minut_Germany-ukr --marker_name germ_20_ukr
```
   Функція знаходить картинки у pdf, аналізує кількість точок для розпізнавання, вибирає 
   з найбільшою кількістю тщточок. 
   Всі картинки по сторінках зберігаються у папці з ім'ям pdf у загальній папці "images". Якщо папку не знайдено, функція її створить.
   Папка з pdf повинна включати в себе тільки сторінки для аналізу (тобто 1,2,3...). 
    
   Маркери треба перевірити, деякі обрізати. При необхідності створити вручну. Система попереджає, якщо не 
   знаходить потрібної для розпізнавання картинки. Тоді можна підставити іншу сторінку з глави. Краще перед 
   автоматичним витягуванням картинки пересвідчитися, що у файлі є окрема картинка, не змішана с текстом,
   не бліда. 

3. Запуск отримання дескріпторів відбувається шляхом запуску з папки проекту:

```bash
python get_descriptors.py --folder_name <name of book>
```
   <name of book> - це назва папки (директорії) з маркерами-картинками окремої книги у форматі 'jpg', отримані з pdf-файлів.
   Приклад:

```bash
python get_descriptors.py --folder_name covers
```
   Функція збирає точки для розпізнавання та записує опис по кожній картинці в файл <folder_name>.pickle (файл з дескрипторами)
	
   У файлі [specifications.json](/settings/specifications.json) на кожну книгу прописуются параметри отримання дексрипторів. 
   Ці параметри залежаль від типу зображень. В проекті є GRAY та CMYK зображення, в залежності від цього
   встановлювалися параметри.


4. Запуск отримання результату пошуку розпізнавання відбувається шляхом запуску з папки проекту у командному рядку:

```bash
python get_marker.py --folder_name <folder/image> / --cover <true>
```
   Приклади:

```bash
	python get_marker.py --folder_name test\pages
	python get_marker.py --folder_name test\pages\20201028_203639.jpg
	python get_marker.py --folder_name test\20201028_203639.jpg --cover true
```
   Передається папка чи файл в аргументі --folder_name. Якщо це обкладинка передається додатковий параметр --cover True, в іншому впадку він не об'язковий.
   Файли приймаються у форматі jpg.

   Алгоритм функції пошуку обкладинки чи поточної сторінки:
	Це обкладинка (так/ні):
		- так - знаходить книгу (так/ні):
			- так - виводить повідомлення з назвою книги, встановлює як поточну
			- ні - виводить повідомлення з негативним результатом пошуку
		- ні - перевіряє чи є обрана поточна книга (так/ні):
			- так - це папка(так/ні):
				- так - шукає сторінки поточної книги по прикладах в папці, виводить повідомлення з результатами
				- ні - шукає сторінку поточної книги по прикладу, виводить повідомлення з результатами
			- ні - завершує виконання с пропозицією передати обкладинку книги
	
   **можливість запуску перевірки пакою зроблена тільки для тесту пачкою. в реальності потрібно аналізувати лише одну подану картинку.


Питання:
при виборі книжки у апі, апка пам'ятає вже доступні книжки?
апка пам'ятає поточну книжку, яку проходить користувач?
при передачі картинка система повинна розуміти чи це обкладинка
