"""
This file works to "tag" each tweet with a sport signifier.
This signifier will tell the program whether or not the specified tweet is about
sports or not. In this program, we are specifically looking at basketball.
"""
# Max Anderson
# mtando
# EECS 486 Final Project

import sys
import os
import json


# list of all teams and team mascots
teamNames = [
    "boston celtics",
    "celtics",
    "brooklyn nets",
    "nets",
    "new york knicks",
    "knicks",
    "philadelphia 76ers",
    "76ers",
    "sixers",
    "toronto raptors",
    "raptors",
    "chicago bulls",
    "bulls",
    "cleveland cavaliers",
    "cavaliers",
    "cavs",
    "detroit pistons",
    "pistons",
    "indiana pacers",
    "pacers",
    "milwaukee bucks",
    "bucks",
    "atlanta hawks",
    "hawks",
    "charlotte hornets",
    "hornets",
    "miami heat",
    "heat",
    "orlando magic",
    "magic",
    "washington wizards",
    "wizards",
    "denver nuggets",
    "nuggets",
    "minnesota timberwolves",
    "timberwolves",
    "t-wolves",
    "oklahoma city thunder",
    "thunder",
    "portland trail blazers",
    "trail blazers",
    "blazers",
    "utah jazz",
    "jazz",
    "golden state warriors",
    "warriors",
    "gsw",
    "los angeles clippers",
    "la clippers",
    "clippers",
    "lac",
    "los angeles lakers",
    "la lakers",
    "lakers",
    "lal",
    "phoenix suns",
    "suns",
    "sacramento kings",
    "kings",
    "dallas mavericks",
    "mavericks",
    "mavs",
    "houston rockets",
    "rockets",
    "memphis grizzlies",
    "grizzlies",
    "new orleans pelicans",
    "pelicans",
    "pels",
    "san antonio spurs",
    "spurs"
    ]

# list of general basketball-related terms
basketballTerms = [
    "nba",
    "eastern conference",
    "western conference",
    "ecf",
    "wcf",
    "nba finals",
    "basketball",
    "b-ball",
    "bball",
    "three pointers",
    "three point",
    "threes",
    "free throws",
    "free throw",
    "point guard",
    "shooting guard",
    "small forward",
    "power forward",
    "dribble",
    "ankle breaker",
    "stepback",
    "floater",
    "half court",
    "full court"
    ]

# list of all NBA player names
playerNames = [
    "Precious Achiuwa",
    "Steven Adams",
    "Bam Adebayo",
    "Santi Aldama",
    "LaMarcus Aldridge",
    "Nickeil Alexander-Walker",
    "Grayson Allen",
    "Jarrett Allen",
    "Jose Alvarado",
    "Kyle Anderson",
    "Giannis Antetokounmpo",
    "Giannis",
    "Thanasis Antetokounmpo",
    "Carmelo Anthony",
    "Cole Anthony",
    "OG Anunoby",
    "Ryan Arcidiacono",
    "D.J. Augustin",
    "DJ Augustin",
    "Deni Avdija",
    "Deandre Ayton",
    "Udoka Azubuike",
    "Marvin Bagley III",
    "Marvin Bagley",
    "LaMelo Ball",
    "Lonzo Ball",
    "Mo Bamba",
    "Desmond Bane",
    "Dalano Banton",
    "Harrison Barnes",
    "Scottie Barnes",
    "R.J. Barrett",
    "RJ Barrett",
    "Will Barton",
    "Charles Bassey",
    "Keita Bates-Diop",
    "Nicolas Batum",
    "Kent Bazemore",
    "Darius Bazley",
    "Bradley Beal",
    "Malik Beasley",
    "Davis Bertans",
    "Patrick Beverley",
    "Pat Bev",
    "Saddiq Bey",
    "Khem Birch",
    "Goga Bitadze",
    "Bismack Biyombo",
    "Nemanja Bjelica",
    "Eric Bledsoe",
    "Keljin Blevins",
    "Bogdan Bogdanovic",
    "Bojan Bogdanovic",
    "Bol Bol",
    "Leandro Bolmaro",
    "Isaac Bonga",
    "Devin Booker",
    "D Book",
    "DBook",
    "B.J. Boston Jr",
    "BJ Boston Jr",
    "BJ Boston",
    "Chris Boucher",
    "James Bouknight",
    "Avery Bradley",
    "Tony Bradley",
    "Ignas Brazdeikis",
    "Mikal Bridges",
    "Miles Bridges",
    "OShae Brissett",
    "Malcolm Brogdon",
    "Armoni Brooks",
    "Dillon Brooks",
    "Greg Brown III",
    "Greg Brown",
    "Charlie Brown",
    "Jaylen Brown",
    "Bruce Brown Jr",
    "Bruce Brown",
    "Troy Brown Jr",
    "Troy Brown",
    "Moses Brown",
    "Sterling Brown",
    "Jalen Brunson",
    "Thomas Bryant",
    "Reggie Bullock",
    "Trey Burke",
    "Alec Burks",
    "Jared Butler",
    "Jimmy Butler",
    "Devontae Cacok",
    "Kentavious Caldwell-Pope",
    "KCP",
    "Facundo Campazzo",
    "Vlatko Cancar",
    "Clint Capela",
    "Vernon Carey Jr",
    "Jevon Carter",
    "Wendell Carter Jr",
    "Alex Caruso",
    "Justin Champagnie",
    "Chris Chiozza",
    "Marquese Chriss",
    "Josh Christopher",
    "Gary Clark",
    "Brandon Clarke",
    "Jordan Clarkson",
    "Nicolas Claxton",
    "Amir Coffey",
    "John Collins",
    "Zach Collins",
    "Mike Conley",
    "Pat Connaughton",
    "Tyler Cook",
    "Sharife Cooper",
    "DeMarcus Cousins",
    "Robert Covington",
    "Rob Covington",
    "Torrey Craig",
    "Jae Crowder",
    "Jarrett Culver",
    "Cade Cunningham",
    "Seth Curry",
    "Stephen Curry",
    "Steph Curry",
    "Anthony Davis",
    "Ed Davis",
    "Terence Davis",
    "DeMar DeRozan",
    "Dewayne Dedmon",
    "Donte DiVincenzo",
    "Hamidou Diallo",
    "Gorgui Dieng",
    "Spencer Dinwiddie",
    "Luka Doncic",
    "Luguentz Dort",
    "Ayo Dosunmu",
    "Goran Dragic",
    "Andre Drummond",
    "Chris Duarte",
    "David Duke",
    "Kris Dunn",
    "Kevin Durant",
    "KD",
    "Anthony Edwards",
    "Carsen Edwards",
    "Kessler Edwards",
    "C.J. Elleby",
    "CJ Elleby",
    "Wayne Ellington",
    "Joel Embiid",
    "Drew Eubanks",
    "Derrick Favors",
    "Bruno Fernando",
    "Dorian Finney-Smith",
    "Malik Fitts",
    "Malachi Flynn",
    "Bryn Forbes",
    "Trent Forrest",
    "Evan Fournier",
    "De'Aaron Fox",
    "DeAaron Fox",
    "Melvin Frazier Jr",
    "Markelle Fultz",
    "Wenyen Gabriel",
    "Daniel Gafford",
    "Danilo Gallinari",
    "Darius Garland",
    "Usman Garuba",
    "Luka Garza",
    "Rudy Gay",
    "Paul George",
    "PG13",
    "Taj Gibson",
    "Josh Giddey",
    "Shai Gilgeous-Alexander",
    "SGA",
    "Anthony Gill",
    "Rudy Gobert",
    "Brandon Goodwin",
    "Aaron Gordon",
    "Eric Gordon",
    "Devonte' Graham",
    "Devonte Graham",
    "Jerami Grant",
    "Danny Green",
    "Draymond Green",
    "JaMychal Green",
    "Jalen Green",
    "Javonte Green",
    "Jeff Green",
    "Josh Green",
    "Blake Griffin",
    "Quentin Grimes",
    "Rui Hachimura",
    "Tyrese Haliburton",
    "R.J. Hampton",
    "RJ Hampton",
    "Tim Hardaway Jr",
    "James Harden",
    "Harden",
    "Maurice Harkless",
    "Jared Harper",
    "Montrezl Harrell",
    "Gary Harris",
    "Joe Harris",
    "Tobias Harris",
    "Josh Hart",
    "Isaiah Hartenstein",
    "Udonis Haslem",
    "Sam Hauser",
    "Jaxson Hayes",
    "Killian Hayes",
    "Gordon Hayward",
    "Juancho Hernangomez",
    "Willy Hernangomez",
    "Tyler Herro",
    "Buddy Hield",
    "Haywood Highsmith",
    "George Hill",
    "Malcolm Hill",
    "Nate Hinton",
    "Jaylen Hoard",
    "Aaron Holiday",
    "Jrue Holiday",
    "Justin Holiday",
    "Richaun Holmes",
    "Rodney Hood",
    "Al Horford",
    "Talen Horton-Tucker",
    "THT",
    "Danuel House",
    "Dwight Howard",
    "Markus Howard",
    "Kevin Huerter",
    "Elijah Hughes",
    "Feron Hunt",
    "De'Andre Hunter",
    "DeAndre Hunter",
    "Bones Hyland",
    "Serge Ibaka",
    "Andre Iguodala",
    "Joe Ingles",
    "Brandon Ingram",
    "Kyrie Irving",
    "Jonathan Isaac",
    "Frank Jackson",
    "Isaiah Jackson",
    "Josh Jackson",
    "Jaren Jackson Jr",
    "Reggie Jackson",
    "LeBron James",
    "LBJ",
    "Bron",
    "KingJames",
    "King James",
    "Ty Jerome",
    "Isaiah Joe",
    "Cameron Johnson",
    "Cam Johnson",
    "David Johnson",
    "Jalen Johnson",
    "Keldon Johnson",
    "Keon Johnson",
    "Stanley Johnson",
    "Nikola Jokic",
    "Jokic",
    "Damian Jones",
    "Derrick Jones",
    "Herb Jones",
    "Kai Jones",
    "Mason Jones",
    "Tre Jones",
    "Tyus Jones",
    "DeAndre Jordan",
    "Cory Joseph",
    "Georgios Kalaitzakis",
    "Luke Kennard",
    "Braxton Key",
    "Corey Kispert",
    "Maxi Kleber",
    "Nathan Knight",
    "Kevin Knox",
    "John Konchar",
    "Furkan Korkmaz",
    "Luke Kornet",
    "Vit Krejci",
    "Arnoldas Kulboka",
    "Jonathan Kuminga",
    "Kyle Kuzma",
    "Zach LaVine",
    "Anthony Lamb",
    "Jeremy Lamb",
    "Jock Landale",
    "Romeo Langford",
    "Jake Layman",
    "Caris LeVert",
    "Damion Lee",
    "Saben Lee",
    "Alex Len",
    "Kawhi Leonard",
    "Kawhi",
    "Kira Lewis Jr",
    "Scottie Lewis",
    "Damian Lillard",
    "Nassir Little",
    "Isaiah Livers",
    "Kevon Looney",
    "Brook Lopez",
    "Robin Lopez",
    "Didi Louzada",
    "Kevin Love",
    "K Love",
    "Kyle Lowry",
    "Gabriel Lundberg",
    "Timothe Luwawu-Cabarrot",
    "Trey Lyles",
    "Theo Maledon",
    "Sandro Mamukelashvili",
    "Terance Mann",
    "Tre Mann",
    "Boban Marjanovic",
    "Lauri Markkanen",
    "Naji Marshall",
    "Caleb Martin",
    "Cody Martin",
    "K.J. Martin",
    "KJ Martin",
    "Garrison Mathews",
    "Wesley Matthews",
    "Tyrese Maxey",
    "Skylar Mays",
    "Miles McBride",
    "C.J. McCollum",
    "CJ McCollum",
    "T.J. McConnell",
    "TJ McConnell",
    "Jaden McDaniels",
    "Jalen McDaniels",
    "Doug McDermott",
    "JaVale McGee",
    "Rodney McGruder",
    "Jordan McLaughlin",
    "Ben McLemore",
    "De'Anthony Melton",
    "DeAnthony Melton",
    "Chimezie Metu",
    "Khris Middleton",
    "Patty Mills",
    "Paul Millsap",
    "Shake Milton",
    "Davion Mitchell",
    "Donovan Mitchell",
    "Spida",
    "Evan Mobley",
    "Malik Monk",
    "Greg Monroe",
    "Moses Moody",
    "Xavier Moon",
    "Ja Morant",
    "Marcus Morris",
    "Markieff Morris",
    "Monte Morris",
    "Mychal Mulder",
    "Trey Murphy III",
    "Trey Murphy",
    "Dejounte Murray"
    "Jamal Murray",
    "Mike Muscala",
    "Svi Mykhailiuk",
    "Larry Nance Jr",
    "Aaron Nesmith",
    "Raulzinho Neto",
    "Georges Niang",
    "Daishen Nix",
    "Zeke Nnaji",
    "Nerlens Noel",
    "Jaylen Nowell",
    "Frank Ntilikina",
    "Kendrick Nunn",
    "Jusuf Nurkic",
    "David Nwaba",
    "Jordan Nwora",
    "Royce O'Neale",
    "Royce ONeale",
    "Chuma Okeke",
    "Josh Okogie",
    "Onyeka Okongwu",
    "Isaac Okoro",
    "Victor Oladipo",
    "Kelly Olynyk",
    "Cedi Osman",
    "Kelly Oubre Jr",
    "Eric Paschall",
    "Chris Paul",
    "CP3",
    "Cameron Payne",
    "Cam Payne",
    "Gary Payton II",
    "Gary Payton",
    "Elfrid Payton",
    "Jamorko Pickett",
    "Theo Pinson",
    "Mason Plumlee",
    "Jakob Poeltl",
    "Aleksej Pokusevski",
    "Yves Pons",
    "Jordan Poole",
    "Kevin Porter Jr",
    "KPJ",
    "Michael Porter Jr",
    "MPJ",
    "Otto Porter",
    "Bobby Portis",
    "Kristaps Porzingis",
    "Porzingis",
    "Dwight Powell",
    "Myles Powell",
    "Norman Powell",
    "Jason Preston",
    "Joshua Primo",
    "Taurean Prince",
    "Payton Pritchard",
    "Trevelin Queen",
    "Neemias Queta",
    "Immanuel Quickley",
    "Julius Randle",
    "Austin Reaves",
    "Cam Reddish",
    "Davon Reed",
    "Paul Reed Jr",
    "Naz Reid",
    "Nick Richards",
    "Josh Richardson",
    "Austin Rivers",
    "Duncan Robinson",
    "Mitchell Robinson",
    "Jeremiah Robinson-Earl",
    "Isaiah Roby",
    "Rajon Rondo",
    "Derrick Rose",
    "D Rose",
    "Terrence Ross",
    "Terry Rozier",
    "Ricky Rubio",
    "D'Angelo Russell",
    "DAngelo Russell",
    "Matt Ryan",
    "Domantas Sabonis",
    "Dario Saric",
    "Tomas Satoransky",
    "Jordan Schakel",
    "Admiral Schofield",
    "Dennis Schroder",
    "Jayden Scrubb",
    "Alperen Sengun",
    "Collin Sexton",
    "Landry Shamet",
    "Day'Ron Sharpe",
    "DayRon Sharpe",
    "Pascal Siakam",
    "Ben Simmons",
    "Marko Simonovic",
    "Anfernee Simons",
    "Zavier Simpson",
    "Jericho Sims",
    "Ja'Vonte Smart",
    "JaVonte Smart",
    "Marcus Smart",
    "Ish Smith",
    "Jalen Smith",
    "Xavier Sneed",
    "Tony Snell",
    "Jaden Springer",
    "Nik Stauskas",
    "Lance Stephenson",
    "Lamar Stevens",
    "Isaiah Stewart II",
    "Isaiah Stewart",
    "D.J. Stewart Jr",
    "DJ Stewart Jr",
    "Max Strus",
    "Jalen Suggs",
    "Jae'sean Tate",
    "Jaesean Tate",
    "Jayson Tatum",
    "Terry Taylor",
    "Garrett Temple",
    "Tyrell Terry",
    "Daniel Theis",
    "Brodric Thomas",
    "Cam Thomas",
    "Isaiah Thomas",
    "Matt Thomas",
    "Klay Thompson",
    "Tristan Thompson",
    "J.T. Thor",
    "JT Thor",
    "Matisse Thybulle",
    "Killian Tillie",
    "Xavier Tillman Sr",
    "Xavier Tillman",
    "Isaiah Todd",
    "Obi Toppin",
    "Juan Toscano-Anderson",
    "JTA",
    "Karl-Anthony Towns",
    "KAT",
    "Gary Trent Jr",
    "Gary Trent",
    "P.J. Tucker",
    "PJ Tucker",
    "Myles Turner",
    "Jonas Valanciunas",
    "Fred VanVleet",
    "Jarred Vanderbilt",
    "Devin Vassell",
    "Luca Vildoza",
    "Gabe Vincent",
    "Nikola Vucevic",
    "Dean Wade",
    "Franz Wagner",
    "Moe Wagner",
    "Ishmail Wainright",
    "Kemba Walker",
    "Lonnie Walker",
    "John Wall",
    "T.J. Warren",
    "TJ Warren",
    "Duane Washington Jr",
    "Duane Washington",
    "P.J. Washington",
    "PJ Washington",
    "Yuta Watanabe",
    "Lindy Waters III",
    "Lindy Waters",
    "Trendon Watford",
    "Quinndary Weatherspoon",
    "Russell Westbrook",
    "Westbrick",
    "Coby White",
    "Derrick White",
    "Hassan Whiteside",
    "Joe Wieskamp",
    "Aaron Wiggins",
    "Andrew Wiggins",
    "Lindell Wigginton",
    "Brandon Williams",
    "Grant Williams",
    "Kenrich Williams",
    "Lou Williams",
    "Lou Will",
    "Patrick Williams",
    "Robert Williams",
    "Ziaire Williams",
    "Zion Williamson",
    "Dylan Windler",
    "Justise Winslow",
    "Cassius Winston",
    "James Wiseman",
    "Christian Wood",
    "Robert Woodard II",
    "Robert Woodard",
    "Delon Wright",
    "McKinley Wright",
    "Moses Wright",
    "Gabe York",
    "Thaddeus Young",
    "Trae Young",
    "Trae",
    "Omer Yurtseven",
    "Ivica Zubac"
    ]


def main():
    data = sys.argv[1]
    curr_file = open(data, "r")

    # load json data into list of tweets
    tweet_dict = json.loads(curr_file.read())
    curr_file.close()
    # attach a sportScore to each tweet
    scoreTotal = 0
    for t in tweet_dict:
        tweet = tweet_dict[t]["text"].lower()
        sportScore = 0

        for tn in teamNames:
            if tn in tweet:
                sportScore = 1
        for bt in basketballTerms:
            if bt in tweet:
                sportScore = 1
        for pn in playerNames:
            if pn.lower() in tweet:
                sportScore = 1

        scoreTotal += sportScore
        tweet_dict[t]["sportScore"] = sportScore

    # for testing
    # print(scoreTotal)

    # split full dictionary into sports related and non sports related tweets
    tweet_dict_sport = {}
    tweet_dict_nonsport = {}
    for i in tweet_dict:
        if tweet_dict[i]["sportScore"] == 1:
            tweet_dict_sport[i] = tweet_dict[i]
        else:
            tweet_dict_nonsport[i] = tweet_dict[i]

    # write json output for sports related tweets
    filename1 = data[:-5] + "_tagged_sport.json"
    output1 = open(filename1, "w")
    json.dump(tweet_dict_sport, output1, indent=2)
    output1.close()

    # write json output for non sports related tweets
    filename2 = data[:-5] + "_tagged_nonsport.json"
    output2 = open(filename2, "w")
    json.dump(tweet_dict_nonsport, output2, indent=2)
    output2.close()

    return

if __name__ == "__main__":
    main()
