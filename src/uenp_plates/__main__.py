import click
import enum
from pathlib import Path
from pprint import pp

from munch import Munch

from . import FindPlates, ReadPlates


class ModuleEnum(str, enum.Enum):
    FIND_PLATES = 'find_plates'
    READ_PLATES = 'read_plates'


@click.command()
@click.option(
        '--module',
        type=click.Choice([e.value for e in ModuleEnum]),
        required=True,
        )
@click.option('--filepath', type=str, required=True)
@click.option('--debug', is_flag=True, help="Show images results.")
@click.option('--export', is_flag=True, help="Export results.")
@click.option('-l', '--language', type=str, default='por',
              help="Pass this info like pytesseract format")
def main(module, filepath, debug, export, language):
    filepath = Path(filepath)
    if not filepath.is_file():
        raise ValueError(f"Invalid file: '{filepath}'")

    if module == ModuleEnum.FIND_PLATES:
        instance = FindPlates(filepath.__str__())
        instance.process()
        message = ('Total plates counted = '
                   f'{instance.metadata.interpretation.plates_number}')
    elif module == ModuleEnum.READ_PLATES:
        instance = ReadPlates(filepath.__str__())
        instance.process()
        plates_info = instance.metadata.interpretation.plates_info
        total_letters = 0
        total_blocks_of_text_number = 0
        data_per_plate = {}
        for label, plate_info in plates_info.items():
            data_per_plate[label] = Munch(
                    letters_number=plate_info.letters_number,
                    blocks_of_text_number=plate_info.blocks_of_text_number)
            total_letters += plate_info.letters_number
            total_blocks_of_text_number += plate_info.blocks_of_text_number

        message = (f'Total letters counted from plates = {total_letters}, and '
                   f'the total block of text= {total_blocks_of_text_number}.\n'
                   f'Data per plates = {data_per_plate}')

    if debug:
        instance.display()
    if export:
        instance.export()

    pp(message)


if __name__ == '__main__':
    main()
