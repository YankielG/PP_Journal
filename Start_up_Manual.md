# INSTRUKCJA – Jak Uruchomić Aplikacje:

Aplikacja to projekt w Django znajduję się na gicie w prywatnym repozytorium:
https://github.com/YankielG/PP_Journal

Ta sama wersja aplikacji prawdopodomnie zostanie umieszczona na darmowym serwerze - jak taki znajdę.
https://google.com


------------

1.	Proszę o pobranie „Clona” z git - repozytorium, rozpakowanie go w dowolnym miejscu.

2.	Zaimportować projekt do IDE, najlepiej PyCharm 2024 (Professional Edition), oraz poczekać aż rozwiążą się zależności (requirements.txt).

*   Krok 1-2 można zamienić na bezpośredni import z git poprzez wybranie opcji "Project from Version Control" i wklejenie linku.

3.	Opcjonalnie proszę o utworzenie dowolnej bazy, zalecana POSTGRESQL lub MS SQL – gdyż są już dodane dependencje w settings.py
    lub pozostanie przy wbudowanej bazie db.sqlite3.

4.	Włączyć – od haszować odpowiednią dependencje – domyślnie włączona dla db.sqlite3.

5.	Stworzyć i wypełnić danymi plik ‘.env’ na wzór ‘.env_template. 
    Wypełnić pierwszą lub drugą część zależności od wybranej bazy POSTGRESQL lub MS SQL, pominać dla wbudowanej bazy.
    
6.	W przypadku gdy zostanie wybrana zewnetrzna baza danych, prosze o wykonanie migracji tak aby powstała struktura danych.

7.	Uruchomić przeglądarkę internetową podając adres :  https://localhost:8000

8.	Zarejestrować się w aplikacji. Podając odpowiednio wymagane dane, potem zalogować się korzystając z niej mormalnie.

9.	Wbudowana baza db.sqlite3 ma gotową strukturę danych:

	- UŻYTKOWNIK:  grzes 	TYP: ADMIN          HASŁO:  ***100
	- UŻYTKOWNIK:  Ala 	    TYP: Uzytkownik     HASŁO:  ***200
	- UŻYTKOWNIK:  Tom  	TYP: Uzytkownik     HASŁO:  ***300
	- UŻYTKOWNIK:  Monika 	TYP: Uzytkownik     HASŁO:  ***400
	***400 - końcówka hasła, początek zostanie podany

10.	Niema różnic między zastosowana bazą danych.

------------