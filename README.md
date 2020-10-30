# Books_images
 macthing picturies
 
 Для отримання точок розпізнавання и вирахування опису використовується алгоритм “BRISK” (“Binary Robust Invariant Scalable Keypoints”).


1. Всі вимоги для запуску зібрані у файлі requirements.txt.
	Структура папок проекту розпізнавання:
	- images
		- covers (назви книг скорочено латиниця без пробілів)
			- файл з назвою книги з розширенням "pickle"
		- папки з назвами книг (важливо зберігати унікальне ім'я в латиниці по назвам маркерів в папці covers)
			- файл з назвою книги з розширенням "pickle"

	**після створення 'pickle' зберігання файлів маркерів-картинок не обов'язкове, в розпізнаванні використовується тільки файл 'pickle'

2. Запуск отримання дескріпторів відбувається шляхом запуску з папки проекту:

	python get_descriptors.py --folder_name <name of book>

		<name of book> - це назва папки (директорії) з маркерами-картинками окремої книги у форматі png, отримані з pdf-файлів.

	Приклад:

	\Books_images> python get_descriptors.py --folder_name covers

	Функція збирає точки для розпізнавання та записує опис по кожній картинці в файл <folder_name>.pickle (файл з дескрипторами)


3. Запуск отримання результату пошуку розпізнавання відбувається шляхом запуску з папки проекту в командній строці:

	\Books_images> python get_marker.py --folder_name <folder/image> / --cover <true>

	
	Приклади:

	\Books_images> python get_marker.py --folder_name test\pages
	\Books_images> python get_marker.py --folder_name test\pages\20201028_203639.jpg
	\Books_images> python get_marker.py --folder_name test\20201028_203639.jpg --cover true


	Передається папка чи файл в аргументі --folder_name. Якщо це обкладинка передається додатковий параметр --cover True, в іншому впадку він не об'язковий.
	Файли приймаються у форматі jpg або png.

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
