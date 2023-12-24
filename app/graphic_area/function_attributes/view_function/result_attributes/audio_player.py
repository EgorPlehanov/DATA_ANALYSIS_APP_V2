from typing import List
from enum import Enum
from pandas import DataFrame
import base64
import time
from flet import (
    Row, IconButton, icons, Text, TextButton, colors, Page,
    Slider, Icon, ControlEvent, Audio, ShadowBlurStyle, Column, 
    Container, PopupMenuButton, PopupMenuItem, Ref, BoxShadow,
    ProgressBar
)


class ResultAudioPlayer(Row):
    '''Плеер для проигрывания сигнала'''
    class TimeDisplay(Enum):
        '''Определяет отображение времени'''
        REMAINING = 0   # оставшееся до конца
        DURATION = 1    # длительность

    class State(Enum):
        '''Определяет состояние трека'''
        COMPLITED = 0
        PLAYING = 1
        PAUSED = 2

    def __init__(self, page: Page, data: DataFrame):
        super().__init__()
        self.page = page
        self.data = data

        self.disabled = True
        self.spacing = 0

        self.state = self.State.PLAYING
        self.time_display = self.TimeDisplay.REMAINING
        self.time_with_ms = False
        self.duration = 0
        self.current_position = 0
        self.is_position_changing = False
        self.current_speed = 1.0
        
        self.audio: Audio = self._create_audio_control()
        self.page.overlay.append(self.audio)
        self.page.update()

        self.controls = self.create_controls()


    def _create_audio_control(self) -> Audio:
        '''Создает плеер для проигрывания сигнала'''
        self.ref_audio = Ref[Audio]()
        return Audio(
            ref = self.ref_audio,
            src = 'D:\POLITEH\DATA_ANALYSIS_APP_V2\DATA\wav\sample-12s.wav',
            # src_base64 = self._dataframe_to_base64(self.data),
            autoplay = False,
            volume = 0.5,
            balance = 0,
            playback_rate = self.current_speed,
            on_loaded = self._on_loaded,
            on_position_changed = self._on_position_changed,
            on_state_changed = self._on_state_changed,
        )
    

    def _dataframe_to_base64(self, df: DataFrame) -> str:
        '''Конвертирует DataFrame в строку base64'''
        csv_string = df.to_csv(index=False)
        base64_string = base64.b64encode(csv_string.encode()).decode()
        return base64_string
    

    def _on_loaded(self, e: ControlEvent) -> None:
        '''Срабатывает после загрузки трека'''
        while True:
            try:
                self.duration = self.audio.get_duration()
                break
            except Exception as ex:
                print('audio_player:', ex)

        progress_track: Slider = self.ref_progress_track.current
        progress_track.max = self.duration
        progress_track.divisions = self.duration

        self._update_time(is_update=False)
        self._loading_progress_bar_change_visible()


    def _on_position_changed(self, e: ControlEvent) -> None:
        '''Обновляет текущее время трека'''
        self.current_position = int(e.data)

        self._update_time()

        if not self.is_position_changing:
            progress_track: Slider = self.ref_progress_track.current
            progress_track.value = self.current_position
            progress_track.update()

    
    def _on_state_changed(self, e: ControlEvent) -> None:
        '''Срадатывает при смене состояния трека'''
        if e.data == 'completed':
            self.state = self.State.COMPLITED
            self._update_button_play_icon()


    def create_controls(self) -> List:
        '''Создает плеер для проигрывания сигнала'''
        return [Container(
            bgcolor = colors.BLACK26,
            border_radius = 10,
            expand = True,
            content = Column(spacing=0, controls=[
                Row(spacing=0, controls=[self._create_progress_track()]),
                Row(spacing=0, controls=[
                    self._create_button_play(),
                    self._create_volume(),
                    self._create_speed_control(),
                    self._create_timer()
                ]),
                self._create_loading_progress_bar()
            ])
        )]


    def _create_progress_track(self) -> Slider:
        '''Создает полосу прокрутки трека'''
        self.ref_progress_track = Ref[Slider]()
        return Slider(
            ref = self.ref_progress_track,
            expand = True,
            active_color = colors.WHITE60,
            min = 0,
            max = 100,
            divisions = 100,
            value = 0,
            label = "{value} мс",
            on_change_start = self._change_position_start,
            on_change = self._change_position,
            on_change_end = self._change_position_end
        )
    

    def _change_position_start(self, e: ControlEvent) -> None:
        '''Устанавливает режим изменения позиции'''
        self.is_position_changing = True


    def _change_position(self, e: ControlEvent) -> None:
        '''Изменяет позицию трека'''
        ms = int(e.control.value)
        self._update_time(ms)


    def _change_position_end(self, e: ControlEvent) -> None:
        '''Устанавливает позицию трека в проигрывателе'''
        ms = int(e.control.value)
        self.audio.seek(ms)
        self.is_position_changing = False



    def _create_button_play(self) -> IconButton:
        '''Создает кнопку для запуска трека'''
        self.ref_button_play = Ref[IconButton]()
        return IconButton(
            ref = self.ref_button_play,
            icon = icons.PLAY_CIRCLE,
            icon_size = 40,
            on_click = self._play_track
        )
    

    def _play_track(self, e: ControlEvent) -> None:
        '''Запускает трек'''
        if self.state == self.State.COMPLITED:
            self.state = self.State.PLAYING
            self.audio.play()
        elif self.state == self.State.PLAYING:
            self.state = self.State.PAUSED
            self.audio.pause()
        else:
            self.state = self.State.PLAYING
            self.audio.resume()
        self._update_button_play_icon()


    def _update_button_play_icon(self) -> None:
        '''Обновляет иконку кнопки'''
        btn_play = self.ref_button_play.current
        if self.state == self.State.PLAYING:
            btn_play.icon = icons.PAUSE_CIRCLE
        else:
            btn_play.icon = icons.PLAY_CIRCLE
        btn_play.update()
        


    def _create_volume(self) -> Row:
        '''Создает кнопку для изменения громкости'''
        self.ref_volume_icon = Ref[IconButton]()
        self.ref_volume_slider = Ref[Slider]()
        return Row(
            spacing = 0,
            controls=[
                IconButton(
                    ref = self.ref_volume_icon,
                    icon = icons.VOLUME_DOWN,
                    on_click = self._toggle_sound,
                ),
                Slider(
                    ref = self.ref_volume_slider,
                    width = 150,
                    active_color = colors.WHITE60,
                    min = 0,
                    max = 100,
                    divisions = 100,
                    value = 50,
                    data = 50,
                    label = "{value}",
                    on_change = self._volume_change,
                    on_change_end = self._save_changes
                ),
            ],
        )
    

    def _toggle_sound(self, e: ControlEvent) -> None:
        '''Изменяет громкость трека'''
        volume_slider: Slider = self.ref_volume_slider.current
        
        if self.audio.volume == 0:
            if volume_slider.data == 0:
                self.audio.volume = 0.5
                volume_slider.data = 50
            else:
                self.audio.volume = 0.01 * volume_slider.data
            volume_slider.value = volume_slider.data
        else:
            self.audio.volume = 0
            volume_slider.value = 0
        
        volume_slider.update()
        self._update_volume_icon()
        self._save_changes(e)
        

    def _volume_change(self, e: ControlEvent) -> None:
        '''Изменяет громкость трека'''
        value = e.control.value
        if value > 0:
            e.control.data = value
        self.audio.volume = 0.01 * value
        self._update_volume_icon()
        

    def _save_changes(self, e: ControlEvent) -> None:
        '''Применяет изменение громкости'''
        self.page.update()


    def _update_volume_icon(self) -> None:
        '''Обновляет иконку громкости'''
        volume = int(self.audio.volume * 100)
        volume_icon = self.ref_volume_icon.current

        if volume == 0:
            volume_icon.icon = icons.VOLUME_OFF
        elif 0 < volume <= 50:
            volume_icon.icon = icons.VOLUME_DOWN
        elif 50 < volume:
            volume_icon.icon = icons.VOLUME_UP

        volume_icon.update()
    


    def _create_speed_control(self) -> PopupMenuButton:
        '''Создает кнопку изменения скорости'''
        self.speed_items = self._create_speed_items()
        return PopupMenuButton(
            tooltip = 'Изменить скорость воспроизведения',
            content = self._create_speed_menu_button(),
            items=[
                self._create_speed_slider(),
                PopupMenuItem(),
                *self.speed_items.values()
            ]
        )


    def _create_speed_items(self) -> dict[int | float, PopupMenuItem]:
        speed_to_text = {
            0.2: 'Очень медленно',
            0.5:  'Медленно',
            0.7: 'Умеренно медленно',
            1.0:  'Нормально',
            1.2: 'Умеренно быстро',
            1.5:  'Быстро',
            1.7: 'Очень быстро',
            2.0:  'Супер быстро',
        }
        return {
            speed: PopupMenuItem(
                content = Row([
                    Icon(icons.CHECK if self.current_speed == speed else None),
                    Text(f"{speed}x {text}")
                ]),
                data = speed,
                on_click = self._change_speed
            )
            for speed, text in speed_to_text.items()
        }
    

    def _create_speed_menu_button(self) -> PopupMenuButton:
        '''Создает кнопку изменения скорости'''
        self.ref_speed = Ref[Text]()
        return Container(
            border_radius = 15,
            content = Row(
                spacing = 0,
                controls = [
                    Icon(icons.SPEED, color=colors.WHITE70),
                    Text(ref=self.ref_speed, value='1.0x', color=colors.WHITE60),
                ]
            ),
            on_hover = self._on_hover_speed
        )
    

    def _on_hover_speed(self, e: ControlEvent) -> None:
        '''Устанавливает тень вокруг индикатора'''
        e.control.shadow = (
            BoxShadow(
                spread_radius = 5,
                color = colors.GREY_900,
                blur_style = ShadowBlurStyle.NORMAL,
            )
            if e.data == "true"
            else None
        )
        e.control.update()
    

    def _create_speed_slider(self) -> PopupMenuItem:
        '''Создает ползунок изменения скорости'''
        self.ref_speed_slider_text = Ref[Text]()
        self.ref_speed_slider = Ref[Slider]()
        return PopupMenuItem(
            content = Row(
                spacing = 0,
                controls = [
                    Text(
                        ref = self.ref_speed_slider_text,
                        width = 35,
                        value='1.0x'
                    ),
                    Slider(
                        ref = self.ref_speed_slider,
                        min = 0.1,
                        max = 2.5,
                        round = 1,
                        value = 1.0,
                        divisions = 24,
                        # label = "{value}x",
                        on_change = self._change_speed_slider,
                        on_change_end = self._change_speed
                    )
                ]
            )
        )


    def _change_speed_slider(self, e: ControlEvent) -> None:
        '''Изменяет скорость'''
        self._update_speed_value(e.control.value)
    

    def _change_speed(self, e: ControlEvent) -> None:
        '''Изменяет скорость'''
        if isinstance(e.control, PopupMenuItem):
            self._update_speed_value(e.control.data)

        self.audio.playback_rate = self.current_speed
        self.page.update()


    def _update_speed_value(self, value: int | float | str) -> None:
        '''Обновляет значение скорости'''
        value = round(value, 1)
        new_value = f"{value}x"

        self.ref_speed.current.value = new_value
        self.ref_speed.current.update()

        self.ref_speed_slider_text.current.value = new_value
        self.ref_speed_slider_text.current.update()

        self.ref_speed_slider.current.value = value
        self.ref_speed_slider.current.update()

        if self.current_speed != value:
            self._update_speed_item_checked(self.current_speed)
            self._update_speed_item_checked(value)
            self.current_speed = value
            
    
    def _update_speed_item_checked(self, value: int | float) -> None:
        '''Обновляет отметку выбранной скорости'''
        if value in self.speed_items.keys():
            last_speed: Icon = self.speed_items[value].content.controls[0]
            last_speed.name = None if value == self.current_speed else icons.CHECK
            last_speed.update()



    def _create_timer(self) -> Row:
        '''Создает время трека'''
        self.ref_current_time = Ref[Text]()
        self.ref_remaining_time = Ref[Text]()
        return Row(
            spacing = 0,
            controls = [
                TextButton(
                    content = Text(
                        ref = self.ref_current_time,
                        value = "0:00",
                        color = colors.WHITE60
                    ),
                    tooltip = 'Показывать миллисекунды',
                    on_click = self._toggle_time_precision
                ),
                Text('/'),
                TextButton(
                    content = Text(
                        ref = self.ref_remaining_time,
                        value = '0:00',
                        color = colors.WHITE60
                    ),
                    tooltip = 'Показывать дительность трека',
                    on_click = self._toggle_time_display
                ),
            ]
        )
    

    def _toggle_time_precision(self, e: ControlEvent) -> None:
        '''Переключает отображение миллисекунд'''
        self.time_with_ms = not self.time_with_ms
        self._update_time()
        e.control.tooltip = f"{'Не показывать' if self.time_with_ms else 'Показывать'} миллисекунды"
        e.control.update()


    def _toggle_time_display(self, e: ControlEvent) -> None:
        '''Переключает отображение времени между оставшееся до конца и длительность трека'''
        self.time_display = (
            self.TimeDisplay.DURATION
            if self.time_display == self.TimeDisplay.REMAINING
            else self.TimeDisplay.REMAINING
        )
        self._update_time()
        e.control.tooltip = (
            "Показывать длительность трека"
            if self.time_display == self.TimeDisplay.REMAINING
            else "Показывать оставшееся до конца трека время"
        )
        e.control.update()


    def _update_time(self, time: int = None, is_update: bool = True) -> None:
        '''Обновляет поля текущее время и оставшееся время до конца трека'''
        if time is None:
            time = self.current_position
        if not self.time_with_ms:
            time = int(time / 1000) * 1000

        current_time: Text = self.ref_current_time.current
        remaining_time: Text = self.ref_remaining_time.current
        
        current_time.value = self._converter_time(time)

        if self.time_display == self.TimeDisplay.REMAINING:
            remaining_value = f"-{self._converter_time(max(self.duration - time, 0))}"
        elif self.time_display == self.TimeDisplay.DURATION:
            remaining_value = self._converter_time(self.audio.get_duration())

        remaining_time.value = remaining_value

        if is_update:
            current_time.update()
            remaining_time.update()
        

    def _converter_time(self, time_ms: int) -> str:
        '''Конвертирует миллисекунды в минуты и секунды'''
        ms = time_ms % 1000
        seconds = (time_ms // 1000) % 60
        minutes = time_ms // 60000
        return f"{minutes}:{seconds:02d}" + (f".{ms:03d}" if self.time_with_ms else "")
    


    def _create_loading_progress_bar(self) -> Container:
        '''Создает индикатор загрузки аудио файла'''
        self.ref_loading_progress = Ref[Container]()
        return Container(
            ref = self.ref_loading_progress,
            visible = self.disabled,
            content = Column(
                spacing = 0,
                controls = [
                    Text("   Загрузка аудео файла..."),
                    ProgressBar()
                ]
            )
        )
        

    def _loading_progress_bar_change_visible(self) -> None:
        '''Изменяет видимость индикатора загрузки аудио файла'''
        self.disabled = not self.disabled
        self.ref_loading_progress.current.visible = self.disabled
        self.update()
