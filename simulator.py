import pandas as pd
import random

Gender = ["Male", "Female"]
energy = 100
money_range = [
    50,
    200,  # poverty class
    300,
    800,  # middle class
    1000,
    2000,  # upper class
]
wage = [
    30,  # poverty_class
    60,  # working_class
    100,  # middle_class
    200,  # upper_class
]
class_prob = [
    30,  # poverty_class
    35,  # working_class
    25,  # middle_class
    10,  # upper_class
]


supplies_range = [
    10,
    40,  # poverty class
    40,
    80,  # middle class
    80,
    100,  # upper_class
]
residential_cord = [1, 10]  # 10x10grid
metabolism = [2, 3, 4, 5]
money = 1000
state = "NONE"
char_class_range = ["Poverty_class", "Middle_class", "Upper_class"]
factory_cord = [5, 5]
store_cord = [2, 8]


class character:
    def __init__(
        self,
        Name,
        Gender,
        energy,
        money,
        state,
        x_cord,
        y_cord,
        supplies,
        wage,
        metabolism,
        char_class,
    ):
        self.Name = Name
        self.Gender = Gender
        self.energy = energy
        self.money = money
        self.state = state
        self.location = [x_cord, y_cord]
        self.home = self.location.copy()
        self.supplies = supplies
        self.wage = wage
        self.metabolism = metabolism
        self.char_class = char_class

    def travel(self, target_cord):
        # for x cordinate
        self.energy -= 2
        self.supplies -= self.metabolism
        if self.energy < 0:
            self.energy = 0
        elif self.supplies < 0:
            self.supplies = 0

        if self.location[0] < target_cord[0]:
            self.location[0] += 1
        elif self.location[0] > target_cord[0]:
            self.location[0] -= 1

        # for y cordinate
        elif self.location[1] < target_cord[1]:
            self.location[1] += 1
        elif self.location[1] > target_cord[1]:
            self.location[1] -= 1

    def shopping(self):
        if self.money < 400:
            self.supplies += round(self.money / 4)
            self.money = 0
        else:
            self.supplies = 100
            self.money -= 400

    def sleeping(self):
        self.energy += 10

    def live(self):
        target_cord = factory_cord

        if (
            self.supplies <= self.metabolism * self.distance(store_cord) + 5
            and self.state != "sleep"
            and self.money != 0
        ):
            target_cord = store_cord
            if self.state != "shopping":
                self.state = "NONE"
        elif self.state == "shopping":  # and self.supplies != 0:
            self.state = "NONE"

        if self.energy <= 2 * self.distance(self.home) + 5 and self.state != "shopping":
            target_cord = self.home
            if self.state != "sleep":
                self.state = "NONE"
        elif self.state == "sleep" and self.energy >= 100:
            self.energy = 100
            self.state = "NONE"

        if self.state == "NONE":
            if self.location == target_cord:
                if target_cord == factory_cord:
                    self.state = "working"
                elif target_cord == store_cord:
                    self.state = "shopping"
                elif target_cord == self.home:
                    self.state = "sleep"

            else:
                self.state = "travelling"

        if self.state == "travelling":
            self.travel(target_cord)
            if self.location == target_cord:
                if target_cord == factory_cord:
                    self.state = "working"
                elif target_cord == store_cord:
                    self.state = "shopping"
                elif target_cord == self.home:
                    self.state = "sleep"

        elif self.state == "working":
            self.energy -= 5
            self.supplies -= self.metabolism
            self.money += self.wage
            if self.energy < 0:
                self.energy = 0
            elif self.supplies < 0:
                self.supplies = 0

        elif self.state == "sleep":
            self.sleeping()

        elif self.state == "shopping":
            self.shopping()

        return target_cord

    def distance(self, target_cord):
        x_dist = abs(self.location[0] - target_cord[0])
        y_dist = abs(self.location[1] - target_cord[1])

        return x_dist + y_dist


characters = {}


def character_generator(population):
    for i in range(population):
        wages = random.choices(wage, weights=class_prob)[0]
        if wages == wage[0]:
            money = random.randint(money_range[0], money_range[1])
            supplies = random.randint(supplies_range[0], supplies_range[1])
            char_class = char_class_range[0]
        elif wages == wage[3]:
            money = random.randint(money_range[4], money_range[5])
            supplies = random.randint(supplies_range[4], supplies_range[5])
            char_class = char_class_range[2]
        else:
            money = random.randint(money_range[2], money_range[3])
            supplies = random.randint(supplies_range[2], supplies_range[3])
            char_class = char_class_range[1]

        characters[f"agent_{i}"] = character(
            f"agent_{i}",
            random.choice(Gender),
            energy,
            money,
            state,
            random.randint(residential_cord[0], residential_cord[1]),
            random.randint(residential_cord[0], residential_cord[1]),
            supplies,
            wages,
            random.choice(metabolism),
            char_class,
        )


def run_sim():
    character_generator(50)

    end_hr = 48
    dic = {
        "HOUR": [],
        "NAME": [],
        "ENERGY": [],
        "MONEY": [],
        "STATE": [],
        "X_CORD": [],
        "Y_CORD": [],
        "DISTANCE": [],
        "SUPPLIES": [],
        "DESTINATION": [],
        "CLASS": [],
    }

    for char in characters:
        current_hr = 0

        while current_hr < end_hr:
            current_hr += 1

            target_cord = characters[char].live()
            distance = characters[char].distance(target_cord)

            dic["HOUR"].append(current_hr)
            dic["NAME"].append(characters[char].Name)
            dic["ENERGY"].append(characters[char].energy)
            dic["MONEY"].append(characters[char].money)
            dic["STATE"].append(characters[char].state)
            dic["X_CORD"].append(characters[char].location[0])
            dic["Y_CORD"].append(characters[char].location[1])
            dic["DISTANCE"].append(distance)
            dic["SUPPLIES"].append(characters[char].supplies)
            dic["DESTINATION"].append(target_cord)
            dic["CLASS"].append(characters[char].char_class)

    df = pd.DataFrame(dic)
    return df


df = run_sim()
df.to_csv("simulation_data.csv", index=False)
print(df.to_string())
