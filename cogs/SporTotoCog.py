import nextcord
from nextcord.ext import commands
from bs4 import BeautifulSoup
import requests


bot = commands.Bot(command_prefix='-', intents=nextcord.Intents.all())

async def get_tff_data():
    try:
        url = "https://www.tff.org/default.aspx?pageID=198"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", {"class": "s-table"})

        teams = []

        rows = table.findAll("tr")[1:]

        for row in rows:
            cells = row.findAll("td")
            team_data = {
                "name": cells[0].text.strip().split(".", 1)[-1].strip(),
                "played": int(cells[1].text.strip()),
                "wins": int(cells[2].text.strip()),
                "draws": int(cells[3].text.strip()),
                "losses": int(cells[4].text.strip()),
                "goals_for": int(cells[5].text.strip()),
                "goals_against": int(cells[6].text.strip()),
                "average": int(cells[7].text.strip()),
                "points": int(cells[8].text.strip())
            }
            teams.append(team_data)

        return teams
    except Exception as e:
        raise commands.CommandError(f"Veri alınırken bir hata oluştu: {e}")

class SporTotoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(name="puan_durumu", description="Sport Toto Super Lig Puan Tablosu")
    async def puan_durumu(self, interaction: nextcord.Interaction):
        try:
            teams = await get_tff_data()

            # İstenmeyen kelimeler
            unwanted_words = ["FUTBOL A.Ş.", "SİLTAŞ YAPI", "TÜMOSAN", "A.Ş.", "VAVACARS", "CORENDON", "ATAKAŞ", "MKE", "YILPORT", "MONDİHOME", "YUKATEL", "RAMS", "FUTBOL KULÜBÜ", "EMS YAPI", "BITEXEN", "ÇAYKUR"]

        
            team_names = [team['name'] for team in teams]

    
            cleaned_team_names = []
            for name in team_names:
                cleaned_name = name
                for word in unwanted_words:
                    cleaned_name = cleaned_name.replace(word, "").strip()
                cleaned_team_names.append(cleaned_name)
                
            
            # max_length = max(len(cleaned_name) for cleaned_name in cleaned_team_names)
           
            embed = nextcord.Embed(title="Süper Lig Puan Durumu ",color=nextcord.Color.brand_red())

        
            embed.add_field(name="", value="**Takım-- | OM | G | B | M | AG | YG | A | P | 📜**", inline=False)


            
            emojis = {
                "GALATASARAY": ":lion_face:",
                "FENERBAHÇE": ":bird:",
                "TRABZONSPOR": "🐟",
                "BEŞİKTAŞ":"🦅",
                "KASIMPAŞA":":goose:",
                "RİZESPOR":":teapot:",
                "ANTALYASPOR":"🌞",
                "SİVASSPOR":":dog:",
                "BAŞAKŞEHİR":":owl:",
                "ADANA DEMİRSPOR":":zap:",
                "KAYSERİSPOR":":wolf:",
                "SAMSUNSPOR":":horse_racing:",
                "ANKARAGÜCÜ":":person_in_manual_wheelchair:",
                "HATAYSPOR":":evergreen_tree:",
                "ALANYASPOR":":dove:",
                "FATİH KARAGÜMRÜK":":four_leaf_clover:",
                "GAZİANTEP":":black_bird: ",
                "PENDİKSPOR":":money_with_wings:",
                "KONYASPOR":":man_genie: ",
                "İSTANBULSPOR":":crescent_moon:"
    
            }

            
            for cleaned_name, original_name, team in zip(cleaned_team_names, team_names, teams):
                row = f"**{cleaned_name}--| {team['played']:<3} | {team['wins']:<3} | {team['draws']:<3} | {team['losses']:<3} | {team['goals_for']:<3} | {team['goals_against']:<3} | {team['average']:<3} | {team['points']:<3} |**"
                embed.add_field(name="\n", value=f"{emojis.get(cleaned_name,'')} - {row}", inline=False)
                embed.set_footer(text="🤜 Made in Savitar")
            await interaction.response.send_message(embed=embed)
        except commands.CommandError as e:
            await interaction.response.send_message(f"Bir hata oluştu: {e}")

    @puan_durumu.error
    async def puan_durumu_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, commands.CommandError):
            await interaction.response.send_message("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")

