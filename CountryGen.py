### tombricks
### [TAG, country name (generic), adjective, ideology, capital, rrr ggg bbb, common/countries file]

countries = [
	{
		"tag":				"USA",
		"name":				"United States of America",
		"adj":				"American",
		"ideology":			"Western_Outlook",
		"capital":			"361",
		"colour":			"20 85 146",
		"culture":			"Western_European",
		"long_names":		{
		},
		"parties":			{
			"Eastern_Outlook": [ "CPUSA", "Communist Party of the United States of America" ],
			"Western_Outlook": [ "GOP", "Republican Party" ],
			"Non_Aligned_Outlook": [ "GOP", "Republican Party" ]
		},
		"characters":		{
		}
	}
]

from shutil import copyfile
import os.path
import codecs
FileTags  = open("common/country_tags/00_countries.txt", "a+", encoding="utf8")
FileColor = open("common/countries/colors.txt", "a+", encoding="utf8")

for country in countries:
	if "long_name" not in country:
		country["long_name"] = country["name"]
	if "long_name_def" not in country:
		country["long_name_def"] = "the " + country["long_name"]

	FileTags.write(F'\n{country["tag"]} = "countries/{country["culture"]}.txt" ')
	FileLoc   = open("localisation/english/Country_"+country["tag"]+"_l_english.yml", "w", encoding="utf8")

	long_names = {
		"Eastern_Outlook": country["name"],
		"Eastern_Outlook_DEF": country["name"],
		"Western_Outlook": country["name"],
		"Western_Outlook_DEF": country["name"],
		"Non_Aligned_Outlook": country["name"],
		"Non_Aligned_Outlook_DEF": country["name"],
	}

	for party in country["long_names"]:
		long_names[party] = country["long_names"][party][0]
		long_names[party+"_DEF"] = country["long_names"][party][1]


	FileLoc.write('\ufeff')
	FileLoc.write(F"""l_english:
### Country Names and Cosmetics
 {country["tag"]}: "{country["name"]}"
 {country["tag"]}_DEF: "{country["name"]}"
 {country["tag"]}_ADJ: "{country["adj"]}" 
 {country["tag"]}_Eastern_Outlook: "{long_names["Eastern_Outlook"]}"
 {country["tag"]}_Eastern_Outlook_DEF: "{long_names["Eastern_Outlook_DEF"]}"
 {country["tag"]}_Western_Outlook: "{long_names["Western_Outlook"]}"
 {country["tag"]}_Western_Outlook_DEF: "{long_names["Western_Outlook_DEF"]}"
 {country["tag"]}_Non_Aligned_Outlook: "{long_names["Non_Aligned_Outlook"]}"
 {country["tag"]}_Non_Aligned_Outlook_DEF: "{long_names["Non_Aligned_Outlook_DEF"]}"

 """)
	
	parties = {
		"Eastern_Outlook_party": "$Eastern_Outlook_party$",
		"Eastern_Outlook_party_long": "$Eastern_Outlook_party_long$",
		"Western_Outlook_party": "$Western_Outlook_party$",
		"Western_Outlook_party_long": "$Western_Outlook_party_long$",
		"Non_Aligned_Outlook_party": "$Non_Aligned_Outlook_party$",
		"Non_Aligned_Outlook_party_long": "$Non_Aligned_Outlook_party_long$",
	}

	for party in country["parties"]:
		parties[party+"_party"] = country["parties"][party][0]
		parties[party+"_party_long"] = country["parties"][party][1]
	
	for party in parties:
		FileLoc.write(F'{country["tag"]}_{party}: "{parties[party]}"\n ')

	FileColor.write(F"""
{country["tag"]} = {{
	color = rgb {{ {country["colour"]} }}
	color_ui = rgb {{ {country["colour"]} }}
}}""")

	path = F'history/countries/{country["tag"]} - {country["name"]}.txt'
	with open(path, "w", encoding="utf8") as FileHistory:
		FileHistory.write(F"""capital = {country["capital"]}
set_stability = 0.6
set_war_support = 0.6

# Starting tech
tech_setup_generic = yes

set_politics = {{
	ruling_party = {country["ideology"]}
	last_election = "1978.1.1"
	election_frequency = 48
	elections_allowed = no
}}

set_popularities = {{
	{country["ideology"]} = 100
}}

""")
		for character in country["characters"]:
			FileHistory.write(F'recruit_character = {country["tag"]}_{character}\n')
			FileLoc.write(F'\n {country["tag"]}_{character}: "{country["characters"][character]["name"]}"\n {country["tag"]}_{character}_desc: ""')

	path = F'common/characters/{country["tag"]}.txt'
	with open(path, "w", encoding="utf8") as FileCharacters:
		FileCharacters.write("characters = {")
		for character in country["characters"]:
			FileCharacters.write(F"""
	{country["tag"]}_{character} = {{
		name = {country["tag"]}_{character}

		allowed_civil_war = {{
		}}

		portraits = {{
			civilian = {{
				large = "GFX_Portrait_Generic_Leader"
			}}
			army = {{
				small = "GFX_Minister_Generic_Leader"
			}}
		}}
		
		""")
			for ideology in country["characters"][character]["ideologies"]:
				FileCharacters.write(F"""
		country_leader = {{
			ideology = {ideology}_ideology
			traits = {{ TITLE_{country["characters"][character]["title"]} IDEOLOGY_{country["characters"][character]["subideology"]} }}
			desc = {country["tag"]}_{character}_desc
		}}
""")
			FileCharacters.write("\n	}")
		FileCharacters.write("\n}")

	if not os.path.isfile(F'gfx/flags/{["tag"]}.tga'):
		copyfile("gfx/flags/ZZZ.tga", F'gfx/flags/{country["tag"]}.tga')
		copyfile("gfx/flags/medium/ZZZ.tga", F'gfx/flags/medium/{country["tag"]}.tga')
		copyfile("gfx/flags/small/ZZZ.tga", F'gfx/flags/small/{country["tag"]}.tga')

FileTags.seek(0)
print(FileTags.read())
FileColor.seek(0)
print(FileColor.read())
