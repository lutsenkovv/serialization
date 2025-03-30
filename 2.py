
#виправила помилки в основній програмі


import pickle
import shelve
import json

class Wine:
    def __init__(self, brand, description, strength):
        self.brand = brand
        self.description = description  
        self.strength = strength
        
    def __str__(self):
        return f"{self.brand} ({self.description}) - {self.strength}%"

    def __repr__(self):
        return f"Wine('{self.brand}', '{self.description}', {self.strength})"

    def matches_type(self, wine_type):
        return wine_type in self.description

    def __lt__(self, other):
        return self.strength < other.strength


class BottledWine(Wine):
    def __init__(self, brand, description, strength, volume, container):
        super().__init__(brand, description, strength)
        self.volume = volume  
        self.container = container 

    def __str__(self):
        return f"{super().__str__()}, {self.volume}л, {self.container}"

    def __repr__(self):
        return f"BottledWine('{self.brand}', '{self.description}', {self.strength}, {self.volume}, '{self.container}')"

    def change_container(self):
        self.container = "тетрапак" if self.container == "скло" else "скло"

    def __truediv__(self, factor):
        if factor > 0:
            return BottledWine(self.brand, self.description, self.strength, self.volume / factor, self.container)
        raise ValueError("Factor must be greater than zero")


class WineCollection:
    def __init__(self):
        self.wines = []

    def add_wine(self, wine):
        if isinstance(wine, BottledWine):
            self.wines.append(wine)

    def load_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                brand, description, strength, volume, container = line.strip().split(', ')
                self.add_wine(BottledWine(brand, description, float(strength), float(volume), container))

    def display_wines(self):
        for wine in sorted(self.wines, reverse=True):  
            print(wine)

    def total_volume_by_color(self):
        color_volumes = {}
        for wine in self.wines:
            color = wine.description.split()[0]  
            color_volumes[color] = color_volumes.get(color, 0) + wine.volume
        return color_volumes

# приклади серіалізації
    def save_pickle(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.wines, file)

    def load_pickle(self, filename):
        with open(filename, 'rb') as file:
            self.wines = pickle.load(file)

    def save_shelve(self, filename):
        with shelve.open(filename) as db:
            db['wines'] = self.wines

    def load_shelve(self, filename):
        with shelve.open(filename) as db:
            self.wines = db.get('wines', [])

    def save_text(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(repr(self.wines))

    def load_text(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            self.wines = eval(file.read())

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump([wine.__dict__ for wine in self.wines], file, ensure_ascii=False, indent=4)

    def load_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            wines_data = json.load(file)
            self.wines = [BottledWine(**data) for data in wines_data]


# приклади використання
A = BottledWine("Аліготе", "біле сухе", 10.5, 0.75, "скло")
B = BottledWine("Каберне", "червоне напівсолодке", 12.0, 0.7, "тетрапак")
print(A, B)

L = [
    BottledWine("Мерло", "червоне сухе", 13.0, 0.75, "скло"),
    BottledWine("Совіньйон", "біле напівсолодке", 11.5, 1.0, "тетрапак"),
    BottledWine("Розе", "рожеве сухе", 12.5, 0.5, "скло")
]
for s in L:
    print(s)

print(L)

# текстова серіалізація з repr/eval
txt = repr(L)
copy = eval(txt)
print(copy)

# Pickle серіалізація
F = open('wines.pkl', 'wb')
pickle.dump(L, F)
F.close()
F = open('wines.pkl', 'rb')
E = pickle.load(F)
F.close()
print(E)

# Shelve серіалізація
S = shelve.open('wines.shelve')
S['first'] = L[0]
S['second'] = L[1]
S['third'] = L[2]
S.sync()
S.close()

S = shelve.open('wines.shelve')
R = [S['third'], S['second'], S['first']]
S.close()
print(R)
