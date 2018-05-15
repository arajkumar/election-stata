It is a simple web scrapper which gets Election result data from [ECI official site](http://eciresults.nic.in).

### Limitations
As of now it can display only Karnataka 2018 Assembly Election results, it should be made generic to work with any ECI results.

### Dependencies
```
pip install BeautifulSoup4
pip install lxml
```

### To Run
```
python parse.py
```

### TODO
1. Dump as JSON/XML result
2. Print all candidates info instead of just a winner and trailer
3. Few more statistics :)
