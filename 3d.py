import logging
import pyperclip
from typing import List, Union

lvl = logging.DEBUG
# lvl = logging.INFO
logging.basicConfig(
    filename='3d.log', level=lvl,
    format='%(levelname)s - %(message)s', filemode='w', )


class Pararam:
    logging.info('class Pararam:')
    text: str
    code: str
    start: int
    stop: int
    _params: List['Pararam'] = []
    params: List[List[str]] = [
        ['Температура экструдера', 'M104 S'],
        ['Температура экструдера (установить и ждать)', 'M109 S'],
        ['Обдув (%)', 'M106 S'],
        ['Скорость (%)', 'M220 S'],
        ['Поток (%)', 'M221 S'],
        ['Скорость (лимит)', 'SET_VELOCITY_LIMIT VELOCITY='],
        ['Скорость про-ия угла', 'SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY='],
        ['Ускорение', 'SET_VELOCITY_LIMIT ACCEL='],
        ['Ускорения и торможения', 'SET_VELOCITY_LIMIT ACCEL_TO_DECEL='],
        ['Pressure advance', 'pressure_advance K='],
    ]
    len = len(params)

    def __init__(self, text, code, start=None, stop=None) -> None:
        self.text = text
        self.code = code
        self.start = start
        self.stop = stop
        self._params.append(self)


class Layer:
    logging.info(f'class Layer:')
    start: int
    stop: int

    def __init__(self, start, stop) -> None:
        self.start = start
        self.stop = stop


class Lines:
    logging.info(f'class Lines:')
    text: str
    code: str
    _lines: List['Lines'] = []
    lines: List[List[str]] = [
        [f'Периметры', 'Perimeter'],
        [f'Внешние периметры', 'ExternalPerimeter'],
        [f'Заполнение', 'InternalInfill'],
        [f'Сплошное заполнение', 'SolidInfill'],
        [f'Заполнение зазоров', 'GapFill'],
        [f'Тонкие линии', 'InternalInfill'],
        [f'Линии поддержки', 'SupportMaterial'],
        [f'Связующие линии поддержки', 'SupportMaterialInterface'],
    ]
    len = len(lines)

    def __init__(self, text, code) -> None:
        self.text = text
        self.code = code
        self._lines.append(self)


class Proporties:
    logging.info(f'class Proporties:')
    lines:  List[Union[Lines, Pararam]]
    parametrs: List[Union[Lines, Pararam]]

    def __init__(self) -> None:
        logging.info(f'   def __init__({self}): [Proporties]')
        self.lines = []
        self.parametrs = []
        self.lines = self.set_value(Lines._lines)
        logging.debug(f'   {self.lines = }')
        self.parametrs = self.set_value(Pararam._params)
        logging.debug(f'   {self.parametrs = }')

    def error(self, n=None) -> None:
        _error = f'фигню вводишь'
        print(f'{n}){_error}')
        logging.error(f'{n}{_error}')

    def vvod(self, txt: str, bad=None, n=None,
             wtf: Union[str, int, None] = None) -> Union[int, str]:
        logging.debug(f'                  start vvod({txt=}, {bad=}, {n=}, {wtf=}')
        wtf = input(txt)
        logging.debug(f'                     *{wtf =} ')
        logging.debug(f'                     {txt = }')
        logging.debug(f'                     {bad = }')
        logging.debug(f'                     {n = }')
        if wtf == '' and n != None:
            logging.debug("                        if n!=None and wtf==''")
            return ''
        if bad != None:
            self.error(3)
            logging.debug('                        bad!=None:')
            bad = bad
            return self.vvod(txt=txt, wtf=wtf, bad=bad)
        if wtf == '' and bad == None:
            self.error(4)
            logging.debug("                        wtf=='' and bad==None:")
            return self.vvod(txt=txt, wtf=wtf, bad=bad)
        try:
            logging.debug('                        try:')
            wtf = int(wtf)
            return wtf
        except Exception:
            logging.debug('                        except')
            self.error(1)
            logging.debug(f'                          return self.vvod({txt=}, {wtf=})')
            return self.vvod(txt=txt, wtf=wtf, )

    def set_value(self, lists) -> List[Union[Lines, Pararam]]:
        logging.info(f'         def set_value(self, lists):' )
        spisok: List[Union[Lines, Pararam]] = []
        logging.debug(f'            {spisok = }')
        logging.debug(f'            {lists = }')
        ln = [f'{n}){li.text}' for n, li in enumerate(lists)]
        logging.debug(f'               {ln = }')
        logging.debug(f'               while True:')
        while True:
            if lists[0].__class__ == Pararam:
                text_1 = f'параметра: \n   '
                ln = ln[:Pararam.len]
            else:
                text_1 = f'типа линий: \n   '
                ln = ln[:Lines.len]
            logging.debug(f'                  {lists[0].__class__ = }')
            print(f'Введите номер {text_1}' + '\n   '.join(ln))
            print(f'[Enter] - Далее')
            num = self.vvod('', n=True)
            logging.debug(f'                  {num = }')
            if num == '':
                if spisok.__len__() != 0:
                    break
                else:
                    print(f'Надо ввести хотя бы один вариант:')
                    continue
            if num < lists.__len__():
                element = lists[num]
                logging.debug(f'                  {element = } - '
                              f'list[{num}] = {lists[num]}')
                logging.debug(f'                  {element.__dict__ = }')
                selected = f'Выбран "{num}){element.text}'
                logging.debug(f'                 Выбран "{num}){element.text}')
                if lists[0].__class__ == Pararam:
                    start = self.vvod(
                        f'{element.text} - Ведите начальное значение: ')
                    stop = self.vvod(
                        f'{element.text} - Ведите конечное значение: ')
                    logging.debug(f'                     {start = }')
                    logging.debug(f'                     {stop = }')
                    value: Pararam = Pararam(element.text, element.code, start, stop)
                    print(f'{selected} - {element.start} - {element.stop}".')
                    logging.debug(f'                     {value = }')
                else:
                    print(f'{selected}.')
                    value: Lines = Lines(element.text, element.code)
                    logging.debug(f'                     {value = }')
                spisok.append(value)
            else:
                self.error(2)
                continue
        return spisok


class Diapasons:
    logging.info(f'class Diapasons:')
    layers: Layer
    proporties: Proporties

    def __init__(self) -> None:
        logging.info(f'   def __init__({self}) [Diapasons]')
        self.layers = self.input_layers()
        logging.debug(f'      {self.layers = }  [Diapasons]')
        self.proporties = Proporties()
        logging.debug(f'      {self.proporties = }  [Diapasons]')
        logging.debug(f'      {self.proporties.parametrs = }    [Diapasons]')

    def error(self, n=None) -> None:
        _error = f'фигню вводишь'
        print(f'{n}){_error}')
        logging.error(f'{n}{_error}')

    def input_layers(self) -> Layer:
        logging.info(f'   input_layers(self): [Diapasons]')
        print(f'Введите цифрами через тире диапазон слоев, например:\n'
              f'1-20[Enter]')
        first, last = 0, 0
        while True:
            layers: str = input()
            logging.debug(f'   {layers = }')
            if layers == '':
                print('Введите хотя бы диапазон слоев')
                continue
            if '-' in layers:
                layer = layers.split('-')
                logging.debug(f'   {layer = }')
                l_0 = layer[0]
                l_1 = layer[1]
                if len(layer) == 2:
                    try:
                        first = int(l_0)
                        last = int(l_1)
                        logging.debug(f'   {first = }')
                        logging.debug(f'   {last = }')
                    except:
                        self.error(1)
                        continue
                else:
                    self.error(2)
                    continue
                if type(first) and type(last) == int and last > first:
                    break
                else:
                    self.error(3)
                    continue
            else:
                self.error(4)
        logging.info(f'      return { Layer(first, last) = }')
        return Layer(first, last)


class Model:
    logging.info(f'class Model:')
    macros: List[str] = []
    diapasons: List[Diapasons]

    def __init__(self) -> None:
        [Lines(li[0], li[1]) for li in Lines.lines]
        [Pararam(pa[0], pa[1]) for pa in Pararam.params]
        self.diapasons = []
        logging.debug(f'   def __init__({self}) [Model]')
        logging.debug(f'      {self.diapasons = }  [Model]')
        logging.debug(f'   While True  [Model]')
        while True:
            self.diapasons.append(Diapasons())
            logging.debug(f'      {self.diapasons = } [Model]')
            stop = input('Еще диапазон? 1-да. 0-нет\n')
            if stop == '0':
                break

    def info(self) -> None:
        logging.info(f'\n start def info(self) -> None:')
        print(f'')
        len_d = self.diapasons.__len__()
        logging.debug(f'   {len_d = }')
        if len_d == 1:
            print(f'Введен 1 диапазон.')
        elif len_d < 5:
            print(f'Введено {len_d} диапазона.')
        else:
            print(f'Введено {len_d} диапазонов.')
        logging.debug(f'   for n, d in enumerate({self.diapasons=}, start=1):')
        for n, d in enumerate(self.diapasons, start=1):
            logging.debug(f'      {d = }')
            lines: List[str] = []
            for i, li in enumerate(d.proporties.lines):
                lines.append(li.text)
            logging.debug(f'      {lines = }')
            line: str = ', '.join(lines)
            line = '"' + line + '" '
            logging.debug(f'      {line = }')
            parametrs: List[str] = []
            logging.debug(f'      {parametrs = }')
            params: List[Pararam] = d.proporties.parametrs
            logging.debug(f'      {params = } ')
            for i, p in enumerate(params):
                if p.start < p.stop:
                    delta = 'увеличивается'
                elif p.start == p.stop:
                    delta = 'ни как не изменяется'
                else:
                    delta = 'уменьшается'
                parametrs.append(f'{p.text} {delta} c {p.start} до {p.stop}')
            param = ', '.join(parametrs)
            logging.debug(
                f'В {n} диапазоне на слоях с "{d.layers.start}" '
                f'по "{d.layers.stop}" у {line} \n        {param}.\n')
            print(
                f'В {n} диапазоне на слоях с "{d.layers.start}" '
                f'по "{d.layers.stop}" у {line} \n        {param}.\n')

    def gradient(self) -> None:
        logging.info(f'def gradient({self}):')
        logging.info(
            f'for n, diapason in enumerate({self.diapasons=}, start=1):')
        for d in self.diapasons:
            layers = d.layers
            type_lines: List[Lines] = d.proporties.lines
            parametrs: List[Pararam] = d.proporties.parametrs
            logging.debug(f'      '
                          f'for layer in range({layers.start=},{layers.stop=}')
            for layer in range(layers.start, layers.stop + 1):
                Model.macros.append(f'{{ if layer_num == {layer} }}')
                logging.debug(f'            '
                              f'for type_line in {type_lines=}')
                t_lines: List[str] = []
                logging.debug(f'   {t_lines = }')
                for type_line in type_lines:
                    t_lines.append(type_line.code)
                t_lines = [f' extrusion_role == "{tl}" ' for tl in t_lines]
                logging.debug(f'   {t_lines = }')
                t_line: str = 'or'.join(t_lines)
                logging.debug(f'   {t_line = }')
                Model.macros.append(f'   {{ if {t_line}}}')
                logging.debug(f'      {{ if {t_line}}}')
                logging.debug(f'                  '
                              f'for parametr in {parametrs=}:)')
                for parametr in parametrs:
                    logging.debug(f'                     '
                                  f'{parametr}')
                    layers_len = layers.stop - layers.start
                    logging.debug(f'                     '
                                  f'{layers_len=} = '
                                  f'{layers.stop=} - {layers.start=}')
                    logging.debug(f'                     '
                                  f'{parametr=}')
                    delta = parametr.stop - parametr.start
                    logging.debug(f'                     '
                                  f'{delta=} = '
                                  f'{parametr.stop=} - {parametr.start=}')
                    step = delta / layers_len
                    logging.debug(f'                     '
                                  f'{step=} = {delta=} / {layers_len=}')
                    logging.debug(f'                     '
                                  f'{parametr.start=}')
                    value = parametr.start + step * (layer - layers.start)
                    if parametr.code == 'M106 S':
                        value = 2.55 * value
                    value = round(value)
                    logging.debug(f'                     '
                                  f'{value=}')
                    logging.debug(f'                      '
                                  f'{parametr.code}{value})')
                    Model.macros.append(
                        f'      {parametr.code}{value} ;macros')
                Model.macros.append(f'   {{ endif }}')
                Model.macros.append(f'{{ endif }}')
        print(f'\nМакрос скопирован в буфер обмена')

    def logs(self) -> None:
        logging.info(f' ')
        logging.info(f' ')
        logging.info(f' ')
        logging.info(f'{self.diapasons = }\n')
        for diapason in self.diapasons:
            logging.info(f'   {diapason = }')
            logging.info(f'   {diapason.layers = }')
            logging.info(f'      {diapason.layers.start = }')
            logging.info(f'      {diapason.layers.stop = }')
            logging.debug(f'     {diapason.proporties = }')
            for i, li in enumerate(diapason.proporties.lines):
                logging.info(f'      {diapason.proporties.lines = }\n')
                logging.debug(f'        diapason.proporties.lines[{i}] - {li}')
                logging.info(f'                        '
                             f'              - {li.text} - {li.code}')
            logging.info(f'      {diapason.proporties.parametrs = }')
            for i, p in enumerate(diapason.proporties.parametrs):
                logging.debug(f'     diapason.proporties.parametrs[{i}] - {p}')

    def macros_print(self) -> None:
        for line in self.macros:
            print(line)

    def bufer(self) -> None:
        macros: str = '\n'.join(self.macros)
        pyperclip.copy(macros)


model = Model()
model.logs()
model.gradient()
model.macros_print()
model.info()
model.bufer()