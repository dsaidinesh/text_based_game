import random
import collections
from textwrap import wrap

# Game data
locations = {
    "Jungle Entrance": {
        "description": "You are standing at the edge of a dense jungle. The air is thick with humidity and the sound of exotic birds fills the air.",
        "exits": {"north": "Jungle Path"},
        "items": [],
    },
    "Jungle Path": {
        "description": "You are on a narrow path winding through the jungle. Vines hang from the towering trees and sunlight filters through the dense foliage.",
        "exits": {"north": "Ancient Ruins", "south": "Jungle Entrance"},
        "items": ["rusty machete"],
    },
    "Ancient Ruins": {
        "description": "You have stumbled upon the ruins of an ancient temple. Crumbling stone walls and moss-covered statues stand as remnants of a forgotten civilization.",
        "exits": {"east": "Hidden Cave", "south": "Jungle Path"},
        "items": [],
    },
    "Hidden Cave": {
        "description": "You have entered a dark and damp cave. The air is cold and the only sound is the dripping of water.",
        "exits": {"west": "Ancient Ruins", "north": ""},
        "items": ["golden key"],
    },
    "Lost Temple": {
        "description": "You stand before a magnificent stone temple, adorned with intricate carvings and guarded by imposing statues. The entrance is locked with a large golden keyhole.",
        "exits": {},
        "items": [],
    },
    "Hidden Waterfall": {
        "description": "You have discovered a hidden waterfall cascading into a crystal-clear pool. The air is filled with a refreshing mist.",
        "exits": {"south": "Jungle Path"},
        "items": [],
    },
}

player_inventory = []
player_location = "Jungle Entrance"
story_state = {
    "visited_ruins": False,
    "found_key": False,
    "met_guardian": False,
    "discovered_waterfall": False,
}

# Game loop
while True:
    # Display location description
    print("\n" + "\n".join(wrap(locations[player_location]["description"], 70)))


    # Show available exits
    available_exits = ", ".join(locations[player_location]["exits"].keys())
    print("Available exits:", available_exits)

    # Get player input
    player_action = input("> ").lower().strip()

    # Handle player actions
    if player_action in ["north", "south", "east", "west"]:
        if player_action in locations[player_location]["exits"]:
            player_location = locations[player_location]["exits"][player_action]
        else:
            print("You cannot go that way.")
    elif player_action == "look":
        # Look around current location
        print(locations[player_location]["description"])
        if locations[player_location]["items"]:
            print("You see:", ", ".join(locations[player_location]["items"]))
    elif player_action.startswith("take"):
    # Take an item
        words = player_action.split()
        if len(words) > 1:
            item_to_take = " ".join(words[1:])  # Capture the entire item name including spaces
            if item_to_take in locations[player_location]["items"]:
                player_inventory.append(item_to_take)
                locations[player_location]["items"].remove(item_to_take)
                print("You took the", item_to_take)
            else:
                print("There is no such item here.")
        else:
            print("Specify an item to take.")

    elif player_action.startswith("use"):
        # Use an item from inventory
        item_to_use = player_action.split()[1]
        if item_to_use in player_inventory:
            if item_to_use == "rusty machete" and player_location == "Hidden Cave":
                print("You cut through the thick vines blocking the entrance to the Lost Temple.")
                locations["Hidden Cave"]["exits"]["north"] = "Lost Temple"
                player_inventory.remove(item_to_use)
            elif item_to_use == "golden key" and player_location == "Lost Temple":
                print("You unlock the door to the Lost Temple!")
                # Check if all conditions are met for the specific endings
            else:
                print("You can't use that here.")
        else:
                print("You don't have that item.")
                if story_state["visited_ruins"] and not story_state["met_guardian"]:
                    # Guardian's Favor Ending
                    print("As you continue your journey through the jungle, a deep sense of reverence lingers from your time at the ancient ruins.")
                    print("You become aware of a subtle change in the atmosphere, and a mystical presence envelops the surroundings.")
                    print("The air shimmers, and suddenly, a majestic guardian of the jungle materializes before you.")
                    print("It appears to be the protector of this sacred land, and its gaze meets yours with a mixture of curiosity and wisdom.")
                    print("This encounter may hold the key to an extraordinary outcome.")

                elif story_state["visited_ruins"] and story_state["met_guardian"]:
                    # Unexpected Journey Ending
                    print("As you enter the Lost Temple, you discover a hidden passage that leads to a realm of wonders beyond imagination.")
                    print("Your journey takes an unexpected turn, and you find yourself in a place you could have never anticipated.")
                    print("Congratulations! You've experienced an unexpected journey!")
                    break  # End the game

                elif not story_state["visited_ruins"]:
                    # Treasure Hunter Ending
                    print("You enter the Lost Temple and find it filled with unimaginable treasures!")
                    print("As you gather the riches, the walls start to shake, and you barely manage to escape before the temple collapses.")
                    print("You may have faced danger, but the treasure is now yours.")
                    print("Congratulations! You've successfully claimed the Lost Temple's treasure!")
                    break  # End the game

    elif player_action == "inventory":
        # Display player's inventory
        if player_inventory:
            print("Your inventory:", ", ".join(player_inventory))
        else:
            print("Your inventory is empty.")
    else:
        print("Invalid command. Type 'north', 'south', 'east', 'west', 'look', 'take [item]', 'use [item]', or 'inventory'.")

    # Check for special events based on the player's location
    if player_location == "Ancient Ruins" and not story_state["visited_ruins"]:
        print("You have discovered ancient ruins!")
        story_state["visited_ruins"] = True

    elif player_location == "Hidden Cave" and "golden key" in player_inventory and not story_state["found_key"]:
        print("You sense a mystical presence. The guardian of the jungle appears and grants you a special reward.")
        story_state["met_guardian"] = True

    elif player_location == "Hidden Waterfall" and not story_state["discovered_waterfall"]:
        print("Behind the waterfall, you find a hidden passage that leads to a mysterious location.")
        story_state["discovered_waterfall"] = True

    # Check for game termination conditions
    if player_location == "Lost Temple" and "golden key" in player_inventory:
        print("You've successfully unlocked the Lost Temple! Now, it's time to explore and uncover its secrets.")
        break  # End the game

