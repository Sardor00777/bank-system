import json
from abc import ABC, abstractmethod
from datetime import datetime



class MalumotlarBoshqaruvchisi:
    FAYL_NOMI = "bank_malumotlar.json"

    @staticmethod
    def yuklash():
        try:
            with open(MalumotlarBoshqaruvchisi.FAYL_NOMI, "r") as fayl:
                return json.load(fayl)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"mijozlar": []}

    @staticmethod
    def saqlash(malumotlar):
        with open(MalumotlarBoshqaruvchisi.FAYL_NOMI, "w") as fayl:
            json.dump(malumotlar, fayl, indent=4)




class BankEntity(ABC):
    @abstractmethod
    def malumot_korsat(self):
        pass



class Mijoz(BankEntity):
    def __init__(self, ism, id_raqam, hisoblar=None):
        self.ism = ism
        self.id_raqam = id_raqam
        self.hisoblar = hisoblar if hisoblar else []

    def hisob_qosh(self, hisob):
        self.hisoblar.append(hisob)

    def malumot_korsat(self):
        return f"Mijoz: {self.ism}, ID: {self.id_raqam}"



class BankHisobi(BankEntity):
    def __init__(self, hisob_raqami, balans=0):
        self.hisob_raqami = hisob_raqami
        self.balans = balans
        self.tranzaktsiyalar = []

    def pul_qoyish(self, summa):
        self.balans += summa
        self.tranzaktsiyalar.append(Tranzaktsiya("Pul qo'yish", summa))
        return f"{summa} so'm qo'shildi. Yangi balans: {self.balans}"

    def pul_yechish(self, summa):
        if summa > self.balans:
            return "Hisobda yetarli mablag' yo'q!"
        self.balans -= summa
        self.tranzaktsiyalar.append(Tranzaktsiya("Pul yechish", summa))
        return f"{summa} so'm yechildi. Yangi balans: {self.balans}"

    def malumot_korsat(self):
        return f"Hisob raqami: {self.hisob_raqami}, Balans: {self.balans}"



class Tranzaktsiya:
    def __init__(self, turi, summa):
        self.turi = turi
        self.summa = summa
        self.sana = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def malumot_ol(self):
        return f"{self.sana} - {self.turi}: {self.summa} so'm"



class BankTizimi:
    def __init__(self):
        print("📌 Bank tizimi yuklanmoqda...")
        self.malumotlar = MalumotlarBoshqaruvchisi.yuklash()
        self.mijozlar = [
            Mijoz(m["ism"], m["id_raqam"], [BankHisobi(h["hisob_raqami"], h["balans"]) for h in m["hisoblar"]])
            for m in self.malumotlar["mijozlar"]
        ]
        print("✅ Bank tizimi yuklandi!")

    def mijoz_qosh(self, ism, id_raqam):
        mijoz = Mijoz(ism, id_raqam)
        self.mijozlar.append(mijoz)
        self.malumotlar["mijozlar"].append({"ism": ism, "id_raqam": id_raqam, "hisoblar": []})
        MalumotlarBoshqaruvchisi.saqlash(self.malumotlar)
        print("✅ Mijoz qo'shildi!")

    def hisob_qosh(self, id_raqam, hisob_raqami, balans):
        mijoz = next((m for m in self.mijozlar if m.id_raqam == id_raqam), None)
        if not mijoz:
            print("❌ Mijoz topilmadi!")
            return
        hisob = BankHisobi(hisob_raqami, balans)
        mijoz.hisob_qosh(hisob)
        for m in self.malumotlar["mijozlar"]:
            if m["id_raqam"] == id_raqam:
                m["hisoblar"].append({"hisob_raqami": hisob_raqami, "balans": balans})
        MalumotlarBoshqaruvchisi.saqlash(self.malumotlar)
        print("✅ Hisob ochildi!")

    def mijozlar_korsat(self):
        for mijoz in self.mijozlar:
            print(mijoz.malumot_korsat())

    def hisob_balans_korsat(self, hisob_raqami):
        for mijoz in self.mijozlar:
            for hisob in mijoz.hisoblar:
                if hisob.hisob_raqami == hisob_raqami:
                    print(hisob.malumot_korsat())
                    return
        print("❌ Hisob topilmadi!")

    def tranzaktsiya_amal(self, hisob_raqami, summa, amal):
        for mijoz in self.mijozlar:
            for hisob in mijoz.hisoblar:
                if hisob.hisob_raqami == hisob_raqami:
                    if amal == "qoyish":
                        print(hisob.pul_qoyish(summa))
                    elif amal == "yechish":
                        print(hisob.pul_yechish(summa))
                    MalumotlarBoshqaruvchisi.saqlash(self.malumotlar)
                    return
        print("❌ Hisob topilmadi!")



if __name__ == "__main__":
    bank = BankTizimi()
    while True:
        print("\n--- 📌  JAYDARI BANK TIZIMI 📌 ---")
        print("1. Mijoz qo'shish")
        print("2. Hisob ochish")
        print("3. Mijozlarni ko'rish")
        print("4. Hisob balansini ko'rish")
        print("5. Hisobga pul qo'yish")
        print("6. Hisobdan pul yechish")
        print("7. Chiqish")
        tanlov = input("🎯 Tanlang: ").strip()

        if tanlov == "1":
            ism = input("📝 Mijoz ismi: ")
            id_raqam = input("🔢 ID raqam: ")
            bank.mijoz_qosh(ism, id_raqam)
        elif tanlov == "2":
            id_raqam = input("🔢 Mijoz ID raqami: ")
            hisob_raqami = input("🏦 Hisob raqami: ")
            balans = float(input("💰 Boshlang'ich balans: "))
            bank.hisob_qosh(id_raqam, hisob_raqami, balans)
        elif tanlov == "3":
            bank.mijozlar_korsat()
        elif tanlov == "4":
            hisob_raqami = input("🏦 Hisob raqami: ")
            bank.hisob_balans_korsat(hisob_raqami)
        elif tanlov in ["5", "6"]:
            hisob_raqami = input("🏦 Hisob raqami: ")
            summa = float(input("💵 Summani kiriting: "))
            bank.tranzaktsiya_amal(hisob_raqami, summa, "qoyish" if tanlov == "5" else "yechish")
        elif tanlov == "7":
            break
        else:
            print("⚠️ Noto‘g‘ri tanlov!")
