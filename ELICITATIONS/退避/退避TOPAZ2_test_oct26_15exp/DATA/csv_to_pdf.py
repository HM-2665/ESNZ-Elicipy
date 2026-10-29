import argparse
import csv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.lib import utils
from reportlab.lib.colors import blue, green
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName, PdfArray
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import subprocess


def find_system_font(font_pattern):
    result = subprocess.run(["fc-match", "-f", "%{file}", font_pattern],
                            capture_output=True,
                            text=True,
                            check=True)

    font_path = result.stdout.strip()

    if not font_path or not os.path.isfile(font_path):
        raise FileNotFoundError(f"Font not found: {font_pattern}")

    return font_path


REGULAR_FONT = "DejaVuSans"
BOLD_FONT = "DejaVuSans-Bold"

regular_font_path = find_system_font("DejaVu Sans")
bold_font_path = find_system_font("DejaVu Sans:style=Bold")

pdfmetrics.registerFont(TTFont(REGULAR_FONT, regular_font_path))

pdfmetrics.registerFont(TTFont(BOLD_FONT, bold_font_path))


def parse_csv(file_path, language=None):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        columns = reader.fieldnames

        label_col = next((col for col in columns if "LABEL" in col), None)
        short_q_col = next((col for col in columns if "SHORT Q" in col), None)
        long_q_cols = [col for col in columns if col.startswith("LONG Q")]
        units_col = next((col for col in columns if "UNITS" in col), None)
        quest_type_col = next((col for col in columns if "QUEST_TYPE" in col),
                              None)
        image_col = next((col for col in columns if "IMAGE" in col), None)

        # ADDITIONAL_INFO is optional so that old questionnaires remain valid.
        additional_info_col = next(
            (col
             for col in columns if col.strip().upper() == "ADDITIONAL_INFO"),
            None)

        if not all(
                   [label_col,
                    short_q_col,
                    long_q_cols,
                    units_col,
                    quest_type_col]):

            raise ValueError("Missing required columns in the CSV file")

        if len(long_q_cols) > 1:
            languages = [
                col.split("LONG Q_")[-1] for col in long_q_cols if "_" in col
            ]

            if language is None:
                print(f"Available languages: {', '.join(languages)}")
                chosen_lang = input(
                    "Enter the language code to use (e.g., ENG): ").strip(
                    ).upper()
            else:
                chosen_lang = language.strip().upper()

            long_q_col = next(
                (col
                 for col in long_q_cols if col.endswith(f"_{chosen_lang}")),
                None)

            if not long_q_col:
                raise ValueError(
                    f"Selected language '{chosen_lang}' not found in the CSV "
                    f"file. Available languages: {', '.join(languages)}")
        else:
            long_q_col = long_q_cols[0]

        questions = []

        for row in reader:
            additional_info = None
            if additional_info_col:
                value = row.get(additional_info_col)
                if value is not None and value.strip():
                    additional_info = value.strip()

            question = {
                "label":
                row[label_col],
                "short_q":
                row[short_q_col],
                "long_q":
                row[long_q_col],
                "units":
                row[units_col],
                "quest_type":
                row[quest_type_col],
                "image":
                row[image_col]
                if image_col and row[image_col].strip() else None,
                "additional_info":
                additional_info
            }
            questions.append(question)

        return questions


def create_pdf(questions, output_pdf, input_dir):
    tmp_pdf = output_pdf + "_temp.pdf"
    c = canvas.Canvas(tmp_pdf, pagesize=letter)
    form = c.acroForm

    width, height = letter

    y_position = height - 50

    field_names = []

    page = 1

    current_category = None
    for question in questions:
        if question['quest_type'] != current_category:

            if question['quest_type'] == 'target':

                c.showPage()
                y_position = height - 50
                firstPage_target = page
                page += 1

            current_category = question['quest_type']
            c.setFont(BOLD_FONT, 16)
            c.drawCentredString(width / 2, y_position,
                                current_category.upper())
            y_position -= 35

            c.setFont(REGULAR_FONT, 10)
            x_start = 100
            labels = ["First Name", "Last Name", "email"]
            rects = []
            for i, label in enumerate(labels):
                rect_x = x_start + i * 170

                form.textfield(name=label,
                               x=rect_x,
                               y=y_position,
                               borderStyle='inset',
                               borderColor=green,
                               fillColor=None,
                               width=100,
                               height=25,
                               textColor=blue,
                               forceBorder=True)

            y_position -= 15
            for i, label in enumerate(labels):
                c.drawString(x_start + i * 170 + 25, y_position, label)
            y_position -= 15

        if y_position < 100:
            c.showPage()
            y_position = height - 50
            page += 1

        # Add image if available
        if question['image']:
            image_path = os.path.join(input_dir, "images", question['image'])
            if os.path.exists(image_path):
                img = utils.ImageReader(image_path)
                iw, ih = img.getSize()
                aspect = iw / ih
                new_width = 400
                new_height = new_width / aspect
                c.drawImage(image_path,
                            70,
                            y_position - new_height - 10,
                            width=new_width,
                            height=new_height)
                y_position -= new_height + 20

        y_position -= 20

        if y_position < 100:
            c.showPage()
            y_position = height - 50
            page += 1

        title = f"{question['label']}. {question['short_q']}"
        c.setFont(BOLD_FONT, 12)
        c.drawString(50, y_position, title)
        y_position -= 20

        c.setFont(REGULAR_FONT, 10)
        lines = simpleSplit(f"{question['long_q']} ({question['units']})",
                            REGULAR_FONT, 10, width - 100)
        for line in lines:
            c.drawString(70, y_position, line)
            y_position -= 15

        # Prepare the optional additional-information prompt in advance.
        # When present, keep the percentile fields and the additional box
        # together on the same page whenever possible.
        additional_lines = []
        additional_box_height = 70

        if question['additional_info']:
            additional_lines = simpleSplit(question['additional_info'],
                                           REGULAR_FONT, 10, width - 140)

            response_block_height = (55 + len(additional_lines) * 15 + 10 +
                                     additional_box_height + 20)

            if y_position - response_block_height < 50:
                c.showPage()
                y_position = height - 50
                page += 1
        else:
            if y_position < 100:
                c.showPage()
                y_position = height - 50
                page += 1

        y_position -= 25
        c.setFont(REGULAR_FONT, 10)
        x_start = 100
        labels = ["5%ile", "50%ile", "95%ile"]
        rects = []
        for i, perc in enumerate(labels):
            field_name = f"{question['label']}_{perc}"
            rect_x = x_start + i * 170

            form.textfield(name=field_name,
                           tooltip=perc,
                           x=rect_x,
                           y=y_position,
                           borderStyle='inset',
                           borderColor=green,
                           fillColor=None,
                           width=100,
                           height=25,
                           textColor=blue,
                           forceBorder=True)

        y_position -= 15
        for i, perc in enumerate(labels):
            c.drawString(x_start + i * 170 + 35, y_position, perc)
        y_position -= 15

        # Add a large multiline field only for questions whose
        # ADDITIONAL_INFO cell contains text. The CSV text itself is used as
        # the prompt; no extra "Additional information" label is printed.
        if additional_lines:
            y_position -= 10
            c.setFont(BOLD_FONT, 10)

            for line in additional_lines:
                c.drawString(70, y_position, line)
                y_position -= 15

            y_position -= 5

            additional_field_name = (f"{question['label']}_additional_info")

            form.textfield(name=additional_field_name,
                           tooltip=question['additional_info'],
                           x=70,
                           y=y_position - additional_box_height,
                           borderStyle='inset',
                           borderColor=green,
                           fillColor=None,
                           width=width - 140,
                           height=additional_box_height,
                           textColor=blue,
                           fieldFlags='multiline',
                           maxlen=4000,
                           forceBorder=True)

            y_position -= additional_box_height + 20

        field_names.extend(rects)

    c.save()

    # Add fillable fields
    writer_seed = PdfWriter()
    writer_target = PdfWriter()
    reader = PdfReader(tmp_pdf)
    for i, page in enumerate(reader.pages):
        annotations = []
        for field_name, rect in field_names:
            annotation = PdfDict(Subtype=PdfName.Widget,
                                 T=field_name,
                                 Rect=rect,
                                 FT=PdfName.Tx,
                                 Ff=1,
                                 DA="/Helv 0 Tf 0 g")
            annotations.append(annotation)

        if annotations:
            page.Annots = PdfArray(annotations)

        if i < firstPage_target:

            writer_seed.addpage(page)

        else:

            writer_target.addpage(page)

    writer_seed.write(output_pdf + '_seed.pdf')
    writer_target.write(output_pdf + '_target.pdf')
    os.remove(tmp_pdf)


def main():
    parser = argparse.ArgumentParser(description=(
        "Create fillable seed and target PDF forms from an ELICIPY "
        "questionnaire CSV file."))

    parser.add_argument("questionnaire", help="Path to questionnaire.csv")

    parser.add_argument(
        "-l",
        "--language",
        help=("Language code to use when the questionnaire contains multiple "
              "LONG Q_<LANG> columns, e.g. ENG, ITA, FRA. If omitted, the "
              "script asks interactively."))

    parser.add_argument(
        "-o",
        "--output",
        help=("Output file base name, without _seed.pdf or _target.pdf. "
              "Default: questionnaire_form in the same directory as the CSV."))

    args = parser.parse_args()

    csv_file = os.path.abspath(os.path.expanduser(args.questionnaire))

    if not os.path.isfile(csv_file):
        parser.error(f"Questionnaire file not found: {csv_file}")

    input_dir = os.path.dirname(csv_file)

    if args.output:
        output_pdf = os.path.abspath(os.path.expanduser(args.output))
    else:
        output_pdf = os.path.join(input_dir, "questionnaire_form")

    output_dir = os.path.dirname(output_pdf)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    questions = parse_csv(csv_file, language=args.language)
    create_pdf(questions, output_pdf, input_dir)

    print(f"Seed PDF created:   {output_pdf}_seed.pdf")
    print(f"Target PDF created: {output_pdf}_target.pdf")


if __name__ == "__main__":
    main()
