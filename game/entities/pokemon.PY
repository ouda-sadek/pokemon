class Pokemon:
    def __init__(self, name, hp, level, attack, defense, types):
        self.name = name
        self.hp = hp
        self.level = level
        self.attack = attack
        self.defense = defense
        self.types = types
    def __str__(self):
        return {self.name, self.hp, self.level,self.attack, self.defense, self.types}
    def tackle(self):
        # Attack logic
        pass

    def suffer_damage(self, damage):
        self.hp -= damage

    def is_alive(self):
        return self.hp > 0
    
pokemon=[]
pokemon.append(grahyene=Pokemon("Grahyène",100,1,10,10,"ténèbres"))
pokemon.append(medhyena=Pokemon("Medhyène",100,1,10,10,"ténèbres"))
pokemon.append(kyureme=Pokemon("Kyureme",100,1,10,10,"dragon""glace"))
pokemon.append(bulbizarre=Pokemon("Bulbizarre",100,1,10,10,"plante""poison"))
pokemon.append(herbizare=Pokemon("Herbizarre",100,1,10,10,"plante""posion"))
pokemon.append(florizarre=Pokemon("Florizarre",100,1,10,10,"plante""poison"))
pokemon.append(pikachu=Pokemon("Pikachu",100,1,10,10,"electrik"))
pokemon.append(zekrom=Pokemon("Zekrom",100,1,10,10,"electrik""dragon"))
pokemon.append(salameche=Pokemon("Salameche",100,1,10,10,"feu"))
pokemon.append(reptincel=Pokemon("Reptincel",100,1,10,10,"feu"))
pokemon.append(dracaufeu=Pokemon("Dracaufeu",100,1,10,10,"feu""vol"))
pokemon.append(carapuce=Pokemon("Carapuce",100,1,10,10,"eau"))
pokemon.append(carabaffe=Pokemon("carabaffe",100,1,10,10,"eau"))
pokemon.append(tortank=Pokemon("Tortank",100,1,10,10,"eau"))
pokemon.append(machoc=Pokemon("Machoc",100,1,10,10,"combat"))
pokemon.append(machopeur=Pokemon("Machopeur",100,1,10,10,"combat"))
pokemon.append(mackogneur=Pokemon("Mackogneur",100,1,10,10,"combat"))
pokemon.append(anorith=Pokemon("Anorith",100,1,10,10,"roche""insecte"))
print(pokemon)