from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import io


class Creator:
    fileName = 'WH_character_sheet.pdf'
    title = 'Warhammer Helper'
    logoSrc = 'staticfiles\WH_logo.png'
    fontSrc = 'staticfiles\CaslonAntique.ttf'

    pdfmetrics.registerFont(
        TTFont('CA', fontSrc)
    )

    def reformatPrimaryStatistics(self, character):
        primary_reformated = []
        primary_names = ["WS", "BS", "S", "T", "AG", "INT", "WP", "FEL"]
        primary_result = []
        for i in range(0, 8):
            primary_reformated.append(character['primary_statistics'][i * 2] +
                                      character['primary_statistics'][(i * 2) + 1])
        for entity, name in zip(primary_reformated, primary_names):
            primary_result.append(name + ":" + entity)
        return primary_result

    def reformatSecondaryStatistics(self, character):
        secondary_reformated = []
        secondary_names = ["A", "W", "SB", "TB", "M", "MAG", "IP", "FP"]
        secondary_result = []
        for i in range(0, 8):
            secondary_reformated.append(character['secondary_statistics'][i * 2] +
                                        character['secondary_statistics'][(i * 2) + 1])
        for entity, name in zip(secondary_reformated, secondary_names):
            secondary_result.append(name + ":" + entity)
        return secondary_result

    def createPDF(self, character):
        buffer = io.BytesIO()
        print(str(character))
        self.character = character

        # Create document
        pdf = canvas.Canvas(buffer)
        pdf.setTitle(self.title)

        pdf.setFont('CA', 64)
        pdf.drawString(30, 770, "Warhammer")
        pdf.drawString(30, 700, "Helper")
        pdf.drawImage(self.logoSrc, 380, 670, 150, 150, mask='auto')
        pdf.line(0, 650, 800, 650)

        pdf.setFont('CA', 28)
        pdf.drawString(30, 600, "Name : " + character['name'])
        pdf.drawString(30, 560, "Gender : " + character['sex'])
        pdf.drawString(30, 520, "Age : " + character['age'])
        pdf.drawString(30, 480, "Weight : " + character['weight'])
        pdf.drawString(30, 440, "Eye colour : " + character['eye_colour'])

        pdf.drawString(260, 600, "Hair colour : " + character['hair_colour'])
        pdf.drawString(260, 560, "Race : " + character['race'])
        pdf.drawString(260, 520, "Star sign : " + character['star_sign'])
        pdf.drawString(260, 480, "Weapon : " + character['weapon'])
        pdf.drawString(260, 440, "Armor : " + character['armor'])

        pdf.setFont("CA", 16)
        pdf.drawString(30, 350, "Profession : " + character['profession'])
        pdf.drawString(30, 310, "Equipment : " + character['equipment'])
        pdf.drawString(30, 270, "Origin : " + character['origin'])

        index = 30
        for entity in self.reformatPrimaryStatistics(character):
            pdf.drawString(index, 180, entity)
            index += 60

        index = 30
        for entity in self.reformatSecondaryStatistics(character):
            pdf.drawString(index, 150, entity)
            index += 60

        pdf.save()
        print("Udało się")
        buffer.seek(0)
        return buffer
