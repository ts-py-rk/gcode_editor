import pyperclip
from typing import List, Union


class Pararam:
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
        # ['Pressure advance', 'pressure_advance K='], # пока не работает
    ]
    len = len(params)

    def __init__(self, text, code, start=None, stop=None) -> None:
        self.text = text
        self.code = code
        self.start = start
        self.stop = stop
        self._params.append(self)


class Layer:
    start: int
    stop: int

    def __init__(self, start, stop) -> None:
        self.start = start
        self.stop = stop


class Lines:
    text: str
    code: str
    _lines: List['Lines'] = []
    lines: List[List[str]] = [
        [f'Периметры', 'Perimeter'],
        [f'Внешние периметры', 'ExternalPerimeter'],
        [f'Свисающие периметры', 'OverhangPerimeter'],
        [f'Заполнение', 'InternalInfill'],
        [f'Сплошное заполнение', 'SolidInfill'],
        [f'Заполнение зазоров', 'GapFill'],
        [f'Верхнее сплошное заполнение', 'TopSolidInfill'],
        [f'Внутреннее заполнение моста', 'BridgeInfill'],
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
    lines:  List[Union[Lines, Pararam]]
    parametrs: List[Union[Lines, Pararam]]

    def __init__(self) -> None:
        self.lines = []
        self.parametrs = []
        self.lines = self.set_value(Lines._lines)
        self.parametrs = self.set_value(Pararam._params)

    def error(self) -> None:
        _error = f'Введены некорректные данные'
        print(f'{_error}')

    def vvod(self, txt: str, bad=None, n=None,
             wtf: Union[str, int, None] = None) -> Union[int, str]:
        wtf = input(txt)
        if wtf == '' and n != None:
            return ''
        if bad != None:
            self.error()
            bad = bad
            return self.vvod(txt=txt, wtf=wtf, bad=bad)
        if wtf == '' and bad == None:
            self.error()
            return self.vvod(txt=txt, wtf=wtf, bad=bad)
        try:
            wtf = int(wtf)
            return wtf
        except Exception:
            self.error()
            return self.vvod(txt=txt, wtf=wtf, )

    def set_value(self, lists) -> List[Union[Lines, Pararam]]:
        spisok: List[Union[Lines, Pararam]] = []
        ln = [f'{n}){li.text}' for n, li in enumerate(lists)]
        while True:
            if lists[0].__class__ == Pararam:
                text_1 = f'параметра: \n   '
                ln = ln[:Pararam.len]
            else:
                text_1 = f'типа линий: \n   '
                ln = ln[:Lines.len]
            print(f'Введите номер {text_1}' + '\n   '.join(ln))
            print(f'[Enter] - Далее')
            num = self.vvod('', n=True)
            if num == '':
                if spisok.__len__() != 0:
                    break
                else:
                    print(f'Надо ввести хотя бы один вариант:')
                    continue
            if num < lists.__len__():
                element = lists[num]
                selected = f'Выбран "{num}){element.text}'
                if lists[0].__class__ == Pararam:
                    start = self.vvod(
                        f'{element.text} - Ведите начальное значение: ')
                    stop = self.vvod(
                        f'{element.text} - Ведите конечное значение: ')
                    value: Pararam = Pararam(
                        element.text, element.code, start, stop)
                    print(f'{selected} - {element.start} - {element.stop}".')
                else:
                    print(f'{selected}.')
                    value: Lines = Lines(element.text, element.code)
                spisok.append(value)
            else:
                self.error()
                continue
        return spisok


class Diapasons:
    layers: Layer
    proporties: Proporties

    def __init__(self) -> None:
        self.layers = self.input_layers()
        self.proporties = Proporties()

    def error(self) -> None:
        _error = f'неверный ввод'
        print(f'{_error}')

    def input_layers(self) -> Layer:
        print(f'Введите цифрами через тире диапазон слоев, например:\n'
              f'1-20[Enter]')
        first, last = 0, 0
        while True:
            layers: str = input()
            if layers == '':
                print('Введите хотя бы диапазон слоев')
                continue
            if '-' in layers:
                layer = layers.split('-')
                l_0 = layer[0]
                l_1 = layer[1]
                if len(layer) == 2:
                    try:
                        first = int(l_0)
                        last = int(l_1)
                    except:
                        self.error()
                        continue
                else:
                    self.error()
                    continue
                if type(first) and type(last) == int and last > first:
                    break
                else:
                    self.error()
                    continue
            else:
                self.error()
        return Layer(first, last)


class Model:
    macros: List[str] = []
    diapasons: List[Diapasons]

    def __init__(self) -> None:
        [Lines(li[0], li[1]) for li in Lines.lines]
        [Pararam(pa[0], pa[1]) for pa in Pararam.params]
        self.diapasons = []
        while True:
            self.diapasons.append(Diapasons())
            stop = input('Еще диапазон? 1-да. 0-нет\n')
            if stop == '0':
                break

    def info(self) -> None:
        print(f'')
        len_d = self.diapasons.__len__()
        if len_d == 1:
            print(f'Введен 1 диапазон.')
        elif len_d < 5:
            print(f'Введено {len_d} диапазона.')
        else:
            print(f'Введено {len_d} диапазонов.')
        for n, d in enumerate(self.diapasons, start=1):
            lines: List[str] = []
            for i, li in enumerate(d.proporties.lines):
                lines.append(li.text)
            line: str = ', '.join(lines)
            line = '"' + line + '" '
            parametrs: List[str] = []
            params: List[Pararam] = d.proporties.parametrs
            for i, p in enumerate(params):
                if p.start < p.stop:
                    delta = 'увеличивается'
                elif p.start == p.stop:
                    delta = 'ни как не изменяется'
                else:
                    delta = 'уменьшается'
                parametrs.append(f'{p.text} {delta} c {p.start} до {p.stop}')
            param = ', '.join(parametrs)
            print(
                f'В {n} диапазоне на слоях с "{d.layers.start}" '
                f'по "{d.layers.stop}" у {line} \n        {param}.\n')

    def gradient(self) -> None:
        for d in self.diapasons:
            layers = d.layers
            type_lines: List[Lines] = d.proporties.lines
            parametrs: List[Pararam] = d.proporties.parametrs
            for layer in range(layers.start, layers.stop + 1):
                Model.macros.append(f'{{ if layer_num == {layer} }}')
                t_lines: List[str] = []
                for type_line in type_lines:
                    t_lines.append(type_line.code)
                t_lines = [f' extrusion_role == "{tl}" ' for tl in t_lines]
                t_line: str = 'or'.join(t_lines)
                Model.macros.append(f'   {{ if {t_line}}}')
                for parametr in parametrs:
                    layers_len = layers.stop - layers.start
                    delta = parametr.stop - parametr.start
                    step = delta / layers_len
                    value = parametr.start + step * (layer - layers.start)
                    if parametr.code == 'M106 S':
                        value = 2.55 * value
                    value = round(value)
                    Model.macros.append(
                        f'      {parametr.code}{value} ;macros')
                Model.macros.append(f'   {{ endif }}')
                Model.macros.append(f'{{ endif }}')
        print(f'\nМакрос скопирован в буфер обмена')


    def macros_print(self) -> None:
        for line in self.macros:
            print(line)

    def bufer(self) -> None:
        macros: str = '\n'.join(self.macros)
        pyperclip.copy(macros)


model = Model()
model.gradient()
model.macros_print()
model.info()
model.bufer()