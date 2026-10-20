"""Shared volume configuration for the Mushoku Tensei reader pipeline."""

from __future__ import annotations

from pathlib import Path

BASE = Path("/home/aufvim/Documents/Mushoku_Tensei/musoku tensei/cannon")


def _epub(number: int) -> Path:
    return BASE / f"Mushoku Tensei - Jobless Reincarnation Volume-{number}.epub"


VOLUMES = {
    15: {
        "number": 15,
        "slug": "vol15",
        "epub": _epub(15),
        "title": "Mushoku Tensei: Jobless Reincarnation Vol. 15",
        "label": "The Diary and the Summons",
        "blurb": (
            "The diary, the summons, and the choices that follow. Every line of "
            "dialogue is labeled by speaker, from Rudeus’s household to the Sword "
            "Sanctum and beyond."
        ),
        "chapters": [
            ("ch01", 1, "The Diary (Part 1)", "section-0005.html", "Rudeus", "main"),
            ("ch02", 2, "The Diary (Part 2)", "section-0006.html", "Rudeus", "main"),
            ("ch03", 3, "Resolve", "section-0007.html", "Sylphiette", "main"),
            ("ch04", 4, "Nanahoshi's Hypothesis", "section-0008.html", "Rudeus", "main"),
            ("ch05", 5, "A Letter from Afar", "section-0009.html", "Eris", "main"),
            ("ch06", 6, "Preparations", "section-0010.html", "Rudeus", "main"),
            ("ch07", 7, "Readying for Battle", "section-0011.html", "Rudeus", "main"),
            ("ch08", 8, "Quagmire vs. Dragon God", "section-0012.html", "Orsted", "main"),
            ("ch09", 9, "Berserker Sword King vs. Dragon God", "section-0013.html", "Eris", "main"),
            ("ch10", 10, "Eris Greyrat (Part 1)", "section-0014.html", "Rudeus", "main"),
            ("ch11", 11, "Eris Greyrat (Part 2)", "section-0015.html", "Rudeus", "main"),
            ("ch12", 12, "The Summons", "section-0016.html", "Rudeus", "main"),
            ("ch13", 13, "Explanations", "section-0017.html", "Rudeus", "main"),
            ("ch14", "extra", "Extra Chapter: A Wild Blade Finds Its Sheath", "section-0018.html", "Eris", "extra"),
        ],
        "diary_ranges": {
            "ch01": [("ch01-p0010", "ch01-p0018"), ("ch01-p0026", "ch01-p0158")],
            "ch02": [("ch02-p0016", "ch02-p0259")],
        },
        "letter_ranges": {
            "ch05": [
                ("ch05-p0129", "ch05-p0144", "Rudeus", "Eris", "main"),
                ("ch05-p0158", "ch05-p0159", "Rudeus", "Eris", "postscript"),
            ],
            "ch12": [("ch12-p0002", "ch12-p0006", "Orsted", "Rudeus", "main")],
        },
        "inscriptions": {"ch08-p0023"},
    },
    16: {
        "number": 16,
        "slug": "vol16",
        "epub": _epub(16),
        "title": "Mushoku Tensei: Jobless Reincarnation Vol. 16",
        "label": "Rudeus's First Mission",
        "blurb": (
            "Rudeus takes his first mission for Orsted, meets a Guardian Beast, "
            "and sets out for the Asura Kingdom with old friends and new dangers."
        ),
        "chapters": [
            ("ch01", 1, "The First Mission", "section-0005.html", "Rudeus", "main"),
            ("ch02", 2, "Guardian Beast", "section-0006.html", "Rudeus", "main"),
            ("ch03", 3, "Opening Move", "section-0007.html", "Rudeus", "main"),
            ("ch04", 4, "Mind Made Up", "section-0008.html", "Rudeus", "main"),
            ("ch05", 5, "Working Together", "section-0009.html", "Rudeus", "main"),
            ("ch06", 6, "Orsted's Suggestion", "section-0010.html", "Rudeus", "main"),
            ("ch07", 7, "Library Labyrinth", "section-0011.html", "Rudeus", "main"),
            ("ch08", 8, "The Armored Dragon King and the Second Princess", "section-0012.html", "Rudeus", "main"),
            ("ch09", 9, "Before Traveling to Asura Kingdom", "section-0013.html", "Rudeus", "main"),
            ("ch10", "extra", "Extra Chapter: The Black Wolf Sword King", "section-0014.html", "Ghislaine", "extra"),
        ],
        "diary_ranges": {},
        "letter_ranges": {},
        "inscriptions": set(),
    },
    17: {
        "number": 17,
        "slug": "vol17",
        "epub": _epub(17),
        "title": "Mushoku Tensei: Jobless Reincarnation Vol. 17",
        "label": "The Road to Asura",
        "blurb": (
            "The road to Asura is paved with old suspicions, new alliances, and "
            "a deadly duel that will decide the fate of a kingdom."
        ),
        "chapters": [
            ("ch01", 1, "The Road to Asura", "section-0005.html", "Rudeus", "main"),
            ("ch02", 2, "The Red Wyrm's Upper Jaw", "section-0006.html", "Rudeus", "main"),
            ("ch03", 3, "Suspicions and Theories", "section-0007.html", "Rudeus", "main"),
            ("ch04", 4, "Ariel's Choice", "section-0008.html", "Rudeus", "main"),
            ("ch05", 5, "Tristina", "section-0009.html", "Rudeus", "main"),
            ("ch06", 6, "On the Road", "section-0010.html", "Rudeus", "main"),
            ("ch07", 7, "Ars, the Royal Capital", "section-0011.html", "Rudeus", "main"),
            ("ch08", 8, "Duel at Dusk", "section-0012.html", "Rudeus", "main"),
            ("ch09", 9, "Ariel's Battlefield", "section-0013.html", "Rudeus", "main"),
            ("ch10", 10, "Rudeus's Battlefield", "section-0014.html", "Rudeus", "main"),
            ("ch11", 11, "The Madness of Luke", "section-0015.html", "Luke", "main"),
            ("ch12", 12, "Ten Days in the Capital and the Truth About Orsted", "section-0016.html", "Rudeus", "main"),
            ("ch13", 13, "Farewells and Changes", "section-0017.html", "Rudeus", "main"),
            ("ch14", 14, "Home Again", "section-0018.html", "Rudeus", "main"),
            ("ch15", "extra", "Extra Chapter: ???", "section-0019.html", "Bartender", "extra"),
        ],
        "diary_ranges": {},
        "letter_ranges": {},
        "inscriptions": set(),
    },
    18: {
        "number": 18,
        "slug": "vol18",
        "epub": _epub(18),
        "title": "Mushoku Tensei: Jobless Reincarnation Vol. 18",
        "label": "Home in Sharia",
        "blurb": (
            "Back home in Sharia, Rudeus juggles work, family, school, and a new "
            "business while the next battle gathers on the horizon."
        ),
        "chapters": [
            ("ch00", "diary", "Rudeus's Diary", "section-0005.html", "Rudeus", "diary"),
            ("ch01", 1, "One Job Among Many", "section-0006.html", "Rudeus", "main"),
            ("ch02", 2, "The Borrowed Cat", "section-0007.html", "Rudeus", "main"),
            ("ch03", 3, "The Entrance Ceremony and the Student Council President", "section-0008.html", "Rudeus", "main"),
            ("ch04", 4, "Research Progress", "section-0009.html", "Rudeus", "main"),
            ("ch05", 5, "Signs of a Family Falling Apart", "section-0010.html", "Rudeus", "main"),
            ("ch06", 6, "Starting a Business", "section-0011.html", "Rudeus", "main"),
            ("ch07", 7, "A Company Venture", "section-0012.html", "Rudeus", "main"),
            ("ch08", 8, "Revisiting the Doldia Village", "section-0013.html", "Rudeus", "main"),
            ("ch09", 9, "The Case of the Jerky Thief", "section-0014.html", "Rudeus", "main"),
            ("ch10", 10, "The Other Slave (Part 1)", "section-0015.html", "Rudeus", "main"),
            ("ch11", 11, "The Other Slave (Part 2)", "section-0016.html", "Rudeus", "main"),
            ("ch12", 12, "The Next Battle", "section-0017.html", "Rudeus", "main"),
        ],
        "diary_ranges": {},
        "letter_ranges": {},
        "inscriptions": set(),
    },
    19: {
        "number": 19,
        "slug": "vol19",
        "epub": _epub(19),
        "title": "Mushoku Tensei: Jobless Reincarnation Vol. 19",
        "label": "Zanoba's Decision",
        "blurb": (
            "A royal hostage, a war at Fort Karon, and the road Zanoba chooses "
            "for himself when a crown is offered."
        ),
        "chapters": [
            ("ch01", 1, "Zanoba's Decision", "section-0005.html", "Rudeus", "main"),
            ("ch02", 2, "Bad Omens", "section-0006.html", "Rudeus", "main"),
            ("ch03", 3, "The Return to Shirone", "section-0007.html", "Rudeus", "main"),
            ("ch04", 4, "King Pax", "section-0008.html", "Rudeus", "main"),
            ("ch05", 5, "Fort Karon", "section-0009.html", "Rudeus", "main"),
            ("ch06", 6, "Preparations for War", "section-0010.html", "Rudeus", "main"),
            ("ch07", 7, "The Battle", "section-0011.html", "Rudeus", "main"),
            ("ch08", 8, "An Urgent Message, and Zanoba's True Feelings", "section-0012.html", "Rudeus", "main"),
            ("ch09", 9, "To Pax's Side", "section-0013.html", "Rudeus", "main"),
            ("ch10", 10, "Wasted Effort All Around", "section-0014.html", "Rudeus", "main"),
            ("ch11", 11, "Aftermath", "section-0015.html", "Rudeus", "main"),
            ("ch12", 12, "Zanoba's Chosen Path", "section-0016.html", "Zanoba", "main"),
            ("ch13", 13, "It's All Right to Be Happy", "section-0017.html", "Rudeus", "main"),
            ("ch14", "extra", "Extra Chapter: The Death God and the Gluttonous Prince", "section-0018.html", "Rudeus", "extra"),
        ],
        "diary_ranges": {},
        "letter_ranges": {},
        "inscriptions": set(),
    },
    20: {
        "number": 20,
        "slug": "vol20",
        "epub": _epub(20),
        "title": "Mushoku Tensei: Jobless Reincarnation Vol. 20",
        "label": "Graduation and the Millis Church",
        "blurb": (
            "Cliff and Zanoba graduate, the household grows, and the story "
            "turns toward the Millis Church and its cardinals."
        ),
        "chapters": [
            ("ch01", 1, "Plans for the Future and Cliff's Concerns", "section-0005.html", "Rudeus", "main"),
            ("ch02", 2, "The Zanoba Store", "section-0006.html", "Rudeus", "main"),
            ("ch03", 3, "Cliff and the Institute of Magic Student Council", "section-0007.html", "Rudeus", "main"),
            ("ch04", 4, "Cliff and Zanoba's Graduation Ceremony", "section-0008.html", "Rudeus", "main"),
            ("ch05", "interlude", "Interlude: A Country Bumpkin Visits the City", "section-0009.html", "Nina", "interlude"),
            ("ch06", "interlude", "Interlude: Coming-of-Age Ceremony", "section-0010.html", "Rudeus", "interlude"),
            ("ch07", 5, "Growth and New Horizons", "section-0011.html", "Rudeus", "main"),
            ("ch08", 6, "Onward, to Millishion…", "section-0012.html", "Rudeus", "main"),
            ("ch09", 7, "Cliff's Homecoming", "section-0013.html", "Rudeus", "main"),
            ("ch10", 8, "The House of Latria", "section-0014.html", "Rudeus", "main"),
            ("ch11", 9, "Headquarters of the Millis Church", "section-0015.html", "Rudeus", "main"),
            ("ch12", 10, "The Pope, and…", "section-0016.html", "Rudeus", "main"),
        ],
        "diary_ranges": {},
        "letter_ranges": {},
        "inscriptions": set(),
    },
    21: {
        "number": 21,
        "slug": "vol21",
        "epub": _epub(21),
        "title": "Mushoku Tensei: Jobless Reincarnation Vol. 21",
        "label": "A Chess Problem with the Pope",
        "blurb": (
            "Hardball negotiations with the Church, a chess problem set for "
            "Rudeus by the Pope, and a reunion nobody expected."
        ),
        "chapters": [
            ("ch01", 1, "Playing Dumb", "section-0005.html", "Rudeus", "main"),
            ("ch02", 2, "A Chess Problem", "section-0006.html", "Rudeus", "main"),
            ("ch03", 3, "Flip the Board and Take the King", "section-0007.html", "Rudeus", "main"),
            ("ch04", 4, "Hardball Negotiations", "section-0008.html", "Rudeus", "main"),
            ("ch05", 5, "What's Stopping You?", "section-0009.html", "Rudeus", "main"),
            ("ch06", 6, "For the Good of My Daughter and My Family", "section-0010.html", "Rudeus", "main"),
            ("ch07", 7, "What is Owed", "section-0011.html", "Rudeus", "main"),
            ("ch08", 8, "The Traitor Gets Away", "section-0012.html", "Rudeus", "main"),
            ("ch09", "extra", "Extra Chapter: The Berserker Sword King and the Blessed Child", "section-0013.html", "Eris", "extra"),
            ("ch10", "extra", "Extra Chapter: Therese Looks for a Husband", "section-0014.html", "Therese", "extra"),
            ("ch11", "extra", "Extra Chapter: The Monkey and the Wolf", "section-0015.html", "Geese", "extra"),
        ],
        "diary_ranges": {},
        "letter_ranges": {},
        "inscriptions": set(),
    },
    22: {
        "number": 22,
        "slug": "vol22",
        "epub": _epub(22),
        "title": "Mushoku Tensei: Jobless Reincarnation Vol. 22",
        "label": "Politics, Marriage, and Atofe",
        "blurb": (
            "A homecoming and a report, the politics of the King Dragon Realm, "
            "and a clash with the demon king Atofe."
        ),
        "chapters": [
            ("ch01", 1, "Coming Home and Making Reports", "section-0005.html", "Lilia", "main"),
            ("ch02", 2, "Randolph's Woes", "section-0006.html", "Rudeus", "main"),
            ("ch03", 3, "The Politics of the King Dragon Realm", "section-0007.html", "Rudeus", "main"),
            ("ch04", 4, "The Naughtiest Kid", "section-0008.html", "Rudeus", "main"),
            ("ch05", 5, "The King of the King Dragon Realm", "section-0009.html", "Rudeus", "main"),
            ("ch06", "interlude", "Interlude: Blue and Red", "section-0010.html", "Roxy", "interlude"),
            ("ch07", 6, "Infiltrating Fort Necross", "section-0011.html", "Rudeus", "main"),
            ("ch08", 7, "Dueling Atofe's Ultimate Four", "section-0012.html", "Rudeus", "main"),
            ("ch09", 8, "Imprisoned in Fort Necross", "section-0013.html", "Rudeus", "main"),
            ("ch10", 9, "Princess Rudeus Enters the Fray", "section-0014.html", "Rudeus", "main"),
            ("ch11", 10, "Clash with Demon King Atofe", "section-0015.html", "Rudeus", "main"),
            ("ch12", "interlude", "Interlude: We Got Married", "section-0016.html", "Rudeus", "interlude"),
            ("ch13", 11, "Number Four", "section-0017.html", "Rudeus", "main"),
            ("ch14", "extra", "Extra Chapter: The Monkey and the Dreaming Youth", "section-0018.html", "Geese", "extra"),
        ],
        "diary_ranges": {},
        "letter_ranges": {},
        "inscriptions": set(),
    },
    23: {
        "number": 23,
        "slug": "vol23",
        "epub": _epub(23),
        "title": "Mushoku Tensei: Jobless Reincarnation Vol. 23",
        "label": "The Green-Haired Baby",
        "blurb": (
            "A green-haired baby, a journey to the Divine Continent, and a "
            "hunt for the Second Eye of the Demon Continent."
        ),
        "chapters": [
            ("ch01", 1, "The Green-Haired Baby", "section-0005.html", "Sylphiette", "main"),
            ("ch02", 2, "Path to the Divine Continent", "section-0006.html", "Sylphiette", "main"),
            ("ch03", 3, "Aluce, City of the Divine Continent", "section-0007.html", "Rudeus", "main"),
            ("ch04", 4, "Christening", "section-0008.html", "Rudeus", "main"),
            ("ch05", 5, "Teleportation Device to Another World", "section-0009.html", "Rudeus", "main"),
            ("ch06", 6, "Nanahoshi's Fate", "section-0010.html", "Rudeus", "main"),
            ("ch07", 7, "The Mad Dog's Old Stomping Grounds", "section-0011.html", "Eris", "main"),
            ("ch08", 8, "A North God, an Adventurer, and More…", "section-0012.html", "Rudeus", "main"),
            ("ch09", 9, "A North God, a Mercenary, and More…", "section-0013.html", "Rudeus", "main"),
            ("ch10", 10, "The Second Eye", "section-0014.html", "Rudeus", "main"),
            ("ch11", "extra", "Extra Chapter: Geese and His Final Ally", "section-0015.html", "Geese", "extra"),
        ],
        "diary_ranges": {},
        "letter_ranges": {},
        "inscriptions": set(),
    },
    24: {
        "number": 24,
        "slug": "vol24",
        "epub": _epub(24),
        "title": "Mushoku Tensei: Jobless Reincarnation Vol. 24",
        "label": "The Superd Village and the Plague",
        "blurb": (
            "The Superd village, the Abyssal King Vita, and a plague that "
            "will not stop spreading."
        ),
        "chapters": [
            ("ch01", 1, "A Strategy Meeting", "section-0005.html", "Rudeus", "main"),
            ("ch02", 2, "A Sought-After Item", "section-0006.html", "Rudeus", "main"),
            ("ch03", 3, "A Sought-After Person", "section-0007.html", "Rudeus", "main"),
            ("ch04", 4, "The Superd Village", "section-0008.html", "Rudeus", "main"),
            ("ch05", 5, "Abyssal King Vita", "section-0009.html", "Rudeus", "main"),
            ("ch06", 6, "The Plague", "section-0010.html", "Rudeus", "main"),
            ("ch07", 7, "The Genius", "section-0011.html", "Rudeus", "main"),
            ("ch08", "interlude", "Interlude: Somebody to Someone", "section-0012.html", "Rudeus", "interlude"),
            ("ch09", "interlude", "Interlude: Vita and Raxos", "section-0013.html", "Vita", "interlude"),
            ("ch10", 8, "The Capital", "section-0014.html", "Rudeus", "main"),
            ("ch11", 9, "Four-Day Educational Superd Village Tour", "section-0015.html", "Rudeus", "main"),
            ("ch12", 10, "Disappearance", "section-0016.html", "Rudeus", "main"),
        ],
        "diary_ranges": {},
        "letter_ranges": {},
        "inscriptions": set(),
    },
    25: {
        "number": 25,
        "slug": "vol25",
        "epub": _epub(25),
        "title": "Mushoku Tensei: Jobless Reincarnation Vol. 25",
        "label": "The Last Battle",
        "blurb": (
            "The last battle of the war: Alexander against Rudeus, and the "
            "making of peace with the Ogre God."
        ),
        "chapters": [
            ("ch01", 1, "Someone Notices Something Amiss", "section-0005.html", "Rudeus", "main"),
            ("ch02", 2, "At the Bottom of the Ravine of the Earthwyrm", "section-0006.html", "Rudeus", "main"),
            ("ch03", 3, "A Shot at Victory", "section-0007.html", "Rudeus", "main"),
            ("ch04", 4, "The Mad Dog King vs. the Former Sword God", "section-0008.html", "Rudeus", "main"),
            ("ch05", 5, "Kalman III vs. Kalman II and Co.", "section-0009.html", "Rudeus", "main"),
            ("ch06", 6, "Kalman III vs. Dead End and Co.", "section-0010.html", "Rudeus", "main"),
            ("ch07", 7, "Alexander vs. Rudeus", "section-0011.html", "Rudeus", "main"),
            ("ch08", 8, "Rest", "section-0012.html", "Rudeus", "main"),
            ("ch09", 9, "Making Peace with the Ogre God", "section-0013.html", "Rudeus", "main"),
            ("ch10", "interlude", "Interlude: The Armor", "section-0014.html", "Rudeus", "interlude"),
            ("ch11", "interlude", "Interlude: I Wanted to Be a Hero", "section-0015.html", "Rudeus", "interlude"),
        ],
        "diary_ranges": {},
        "letter_ranges": {},
        "inscriptions": set(),
    },
    26: {
        "number": 26,
        "slug": "vol26",
        "epub": _epub(26),
        "title": "Mushoku Tensei: Jobless Reincarnation Vol. 26",
        "label": "The World After Rudeus",
        "blurb": (
            "The last volume: the threat of the Fighting God, three stories, "
            "and the world that comes after Rudeus."
        ),
        "chapters": [
            ("ch01", 1, "The Threat of the Fighting God", "section-0005.html", "Alex Rybak", "main"),
            ("ch02", 2, "The Trump Card", "section-0006.html", "Rudeus", "main"),
            ("ch03", 3, "The Fifth Turning Point", "section-0007.html", "Rudeus", "main"),
            ("ch04", 4, "The End of the Battle", "section-0008.html", "Rudeus", "main"),
            ("ch05", 1, "Story 1: The Final Dream", "section-0010.html", "Rudeus", "story"),
            ("ch06", 2, "Story 2: Thirty-Four Years Old", "section-0011.html", "Rudeus", "story"),
            ("ch07", 3, "Story 3: The World After Death", "section-0012.html", "Rudeus", "story"),
            ("ch08", "appendix", "Appendix: The Asuran Kingdom's Dossier on Rudeus Greyrat", "section-0013.html", "Rudeus", "appendix"),
            ("ch09", "afterword", "Afterword (Excerpted from The Book of Rudeus, Vol. 26)", "section-0014.html", "Rudeus", "afterword"),
            ("ch10", "epilogue", "Epilogue: Prologue Zero", "section-0015.html", "Rudeus", "epilogue"),
        ],
        "diary_ranges": {},
        "letter_ranges": {},
        "inscriptions": set(),
    },
}

POV_NAMES = {
    "Rudeus",
    "Sylphiette",
    "Eris",
    "Roxy",
    "Orsted",
    "Nanahoshi",
    "Luke",
    "Ariel",
    "Ghislaine",
    "Bartender",
    "Zanoba",
    "Therese",
    "Lilia",
    "Geese",
    "Badigadi",
}


def get_volume(number: int) -> dict:
    try:
        return VOLUMES[int(number)]
    except KeyError as exc:
        raise SystemExit(f"Unknown volume: {number}") from exc
