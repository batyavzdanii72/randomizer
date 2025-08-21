import json
import random
from pathlib import Path

DATA_FILE = Path("pool.json")

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"items": [], "history": [], "seed": None}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()
items = data["items"]         
history = data["history"]     
seed = data.get("seed")

if seed is not None:
    random.seed(seed)

def find_item(name):
    name_norm = name.strip().lower()
    for i, it in enumerate(items):
        if it["name"].strip().lower() == name_norm:
            return i
    return None

def show_items():
    if not items:
        print("List is empty.")
        return
    print("\n--- ITEMS ---")
    for i, it in enumerate(items, 1):
        print(f"{i}. {it['name']}  (weight={it['weight']})")

def show_history():
    if not history:
        print("History is empty.")
        return
    print("\n--- HISTORY ---")
    for i, h in enumerate(history[-20:], 1): 
        print(f"{i}. {', '.join(h['pick'])}")

def add_item():
    name = input("Enter option name: ").strip()
    if not name:
        print("Empty name is not allowed.")
        return
    idx = find_item(name)
    if idx is not None:
        print("This option already exists. Updating weight.")
    try:
        w = float(input("Weight (default 1.0): ") or "1")
        if w <= 0:
            print("Weight must be > 0.")
            return
    except ValueError:
        print("Weight must be a number.")
        return

    if idx is None:
        items.append({"name": name, "weight": w})
    else:
        items[idx]["weight"] = w
    print(f"✅ Added/updated: {name} (weight={w})")

def remove_item():
    name = input("Enter option name to remove: ").strip()
    idx = find_item(name)
    if idx is None:
        print("Not found.")
        return
    removed = items.pop(idx)
    print(f"🗑 Removed: {removed['name']}")

def pick_one():
    if not items:
        print("No options available.")
        return
    names = [it["name"] for it in items]
    weights = [it["weight"] for it in items]
    choice = random.choices(names, weights=weights, k=1)[0]
    history.append({"pick": [choice]})
    print(f"🎯 Pick: {choice}")

def pick_many():
    if not items:
        print("No options available.")
        return
    try:
        k = int(input("How many unique items to pick? "))
    except ValueError:
        print("Enter a valid integer.")
        return
    if k <= 0:
        print("k must be > 0.")
        return
    if k > len(items):
        print("k is larger than the number of items.")
        return

    pool = items.copy()
    picks = []
    for _ in range(k):
        names = [it["name"] for it in pool]
        weights = [it["weight"] for it in pool]
        choice = random.choices(names, weights=weights, k=1)[0]
        picks.append(choice)
        pool = [it for it in pool if it["name"] != choice]

    history.append({"pick": picks})
    print("🎯 Picks:", ", ".join(picks))

def shuffle_items():
    if not items:
        print("No options available.")
        return
    names = [it["name"] for it in items]
    random.shuffle(names)
    print("🔀 Shuffled:", ", ".join(names))

def set_seed():
    global seed
    s = input("Seed (empty to reset): ").strip()
    if s == "":
        seed = None
        random.seed()
        data["seed"] = None
        print("Seed reset.")
        return
    try:
        seed = int(s)
    except ValueError:
        seed = s  
    random.seed(seed)
    data["seed"] = seed
    print(f"Seed set to: {seed}")

def clear_history():
    history.clear()
    print("History cleared.")

def autosave():
    data["items"] = items
    data["history"] = history
    save_data(data)

def main_menu():
    while True:
        print("\n=== RANDOMIZER ===")
        print("1) Show items")
        print("2) Add/update item")
        print("3) Remove item")
        print("4) Pick one item")
        print("5) Pick N unique items")
        print("6) Shuffle items")
        print("7) Show history")
        print("8) Clear history")
        print("9) Set seed")
        print("0) Save and exit")

        choice = input("Choose: ").strip()
        if choice == "1":
            show_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            remove_item()
        elif choice == "4":
            pick_one()
        elif choice == "5":
            pick_many()
        elif choice == "6":
            shuffle_items()
        elif choice == "7":
            show_history()
        elif choice == "8":
            clear_history()
        elif choice == "9":
            set_seed()
        elif choice == "0":
            autosave()
            print("💾 Saved. Bye!")
            break
        else:
            print("Invalid choice.")

        autosave()

if __name__ == "__main__":
    main_menu()

